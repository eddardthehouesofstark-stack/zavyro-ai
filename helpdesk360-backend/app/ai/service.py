import json
import re
from typing import List, Optional, Dict, Any
from app.core.config import settings
from app.core.logging import logger
from app.models.enums import TicketCategory, TicketPriority
from app.schemas.ai import (
    AiAnalysisResult,
    AiSummarizeResponse,
    AiTroubleshootResponse,
    AiDraftReplyResponse,
    AiResolutionResponse,
    AiArticleReference,
    AiChatResponse,
    TicketDraft,
)
from app.ai.base import AIProvider
from app.ai.providers.mock_provider import MockAIProvider
from app.ai.providers.openai_provider import OpenAIProvider
from app.ai.providers.anthropic_provider import AnthropicProvider
from app.ai.prompts import (
    TICKET_ANALYSIS_PROMPT,
    TECHNICIAN_SUMMARIZE_PROMPT,
    TECHNICIAN_TROUBLESHOOT_PROMPT,
    TECHNICIAN_DRAFT_REPLY_PROMPT,
    TECHNICIAN_RESOLUTION_PROMPT,
    IT_CHAT_PROMPT,
)
from app.cache import get_cache


def _extract_json(text: str) -> Dict[str, Any]:
    text = text.strip()
    # Try direct parse
    try:
        return json.loads(text)
    except Exception:
        pass
    # Try finding markdown ```json ... ```
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if match:
        try:
            return json.loads(match.group(1))
        except Exception:
            pass
    # Try finding first { and last }
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start : end + 1])
        except Exception:
            pass
    raise ValueError(f"Could not parse JSON from AI response: {text[:200]}")


class AIService:
    def __init__(self, provider: Optional[AIProvider] = None):
        if provider:
            self.provider = provider
        else:
            p_name = settings.AI_PROVIDER.lower()
            if p_name == "openai" and settings.AI_API_KEY:
                self.provider = OpenAIProvider()
            elif p_name == "anthropic" and settings.AI_API_KEY:
                self.provider = AnthropicProvider()
            else:
                self.provider = MockAIProvider()

        self.cache = get_cache()

    def analyze_ticket(self, title: str, description: str) -> AiAnalysisResult:
        content = f"Title: {title}\nDescription: {description}"
        try:
            raw = self.provider.complete(
                system_prompt=TICKET_ANALYSIS_PROMPT,
                messages=[{"role": "user", "content": content}],
                json_mode=True,
            )
            parsed = _extract_json(raw)

            # Validate enum values
            cat_str = str(parsed.get("category", "OTHER")).upper()
            try:
                category = TicketCategory(cat_str)
            except Exception:
                category = TicketCategory.OTHER

            pri_str = str(parsed.get("priority", "MEDIUM")).upper()
            try:
                priority = TicketPriority(pri_str)
            except Exception:
                priority = TicketPriority.MEDIUM

            return AiAnalysisResult(
                category=category,
                priority=priority,
                summary=str(parsed.get("summary", "Automated ticket triage")),
                suggested_action=str(parsed.get("suggested_action", "Investigate issue details")),
            )
        except Exception as e:
            logger.warning(f"AI ticket analysis failed: {e}. Using deterministic fallback.")
            # Safe deterministic fallback
            return AiAnalysisResult(
                category=TicketCategory.OTHER,
                priority=TicketPriority.MEDIUM,
                summary="Standard support ticket requiring initial triage.",
                suggested_action="Review description and contact employee for diagnostic details.",
            )

    def summarize_ticket(self, ticket_id: int, title: str, description: str, comments: List[str] = None) -> str:
        ctx = f"Ticket #{ticket_id}: {title}\nDescription: {description}"
        if comments:
            ctx += "\nRecent Comments:\n" + "\n".join(comments[-3:])
        try:
            raw = self.provider.complete(
                system_prompt=TECHNICIAN_SUMMARIZE_PROMPT,
                messages=[{"role": "user", "content": ctx}],
            )
            return raw.strip()
        except Exception as e:
            logger.warning(f"AI summarize failed: {e}")
            return f"Ticket #{ticket_id} ({title}): Employee reports {description[:120]}..."

    def troubleshoot_ticket(self, ticket_id: int, title: str, description: str) -> List[str]:
        ctx = f"Ticket #{ticket_id}: {title}\nDescription: {description}"
        try:
            raw = self.provider.complete(
                system_prompt=TECHNICIAN_TROUBLESHOOT_PROMPT,
                messages=[{"role": "user", "content": ctx}],
                json_mode=True,
            )
            parsed = _extract_json(raw)
            steps = parsed.get("steps", [])
            if isinstance(steps, list) and len(steps) > 0:
                return [str(s) for s in steps]
        except Exception as e:
            logger.warning(f"AI troubleshoot failed: {e}")

        return [
            "Check client device connectivity and local network adapter settings.",
            "Verify service status and corporate gateway reachability.",
            "Review diagnostic logs and restart application services.",
            "Confirm resolution with employee.",
        ]

    def draft_reply(self, ticket_id: int, title: str, description: str, employee_name: Optional[str] = None) -> str:
        ctx = f"Ticket #{ticket_id}: {title}\nEmployee: {employee_name or 'User'}\nDescription: {description}"
        try:
            raw = self.provider.complete(
                system_prompt=TECHNICIAN_DRAFT_REPLY_PROMPT,
                messages=[{"role": "user", "content": ctx}],
            )
            return raw.strip()
        except Exception as e:
            logger.warning(f"AI draft reply failed: {e}")
            name = employee_name or "there"
            return (
                f"Hello {name},\n\n"
                f"Thank you for contacting IT Support regarding '{title}'. We have started investigating your ticket "
                f"and are reviewing the diagnostic details. We will update you shortly with next steps."
            )

    def recommend_resolution(
        self,
        ticket_id: int,
        title: str,
        description: str,
        kb_articles: List[Dict[str, Any]] = None,
    ) -> AiResolutionResponse:
        kb_text = "\n".join([f"- {a['id']}: {a['title']}" for a in (kb_articles or [])[:5]])
        ctx = f"Ticket #{ticket_id}: {title}\nDescription: {description}\n\nAvailable KB:\n{kb_text}"
        try:
            raw = self.provider.complete(
                system_prompt=TECHNICIAN_RESOLUTION_PROMPT,
                messages=[{"role": "user", "content": ctx}],
                json_mode=True,
            )
            parsed = _extract_json(raw)
            return AiResolutionResponse(
                ticket_id=ticket_id,
                summary=str(parsed.get("summary", "Resolution verified")),
                solution=str(parsed.get("solution", "Applied recommended standard remediation steps.")),
                steps=parsed.get("steps", ["Diagnostic confirmed", "Remediation applied"]),
                articles=[AiArticleReference(id=a["id"], title=a["title"]) for a in (kb_articles or [])[:3]],
            )
        except Exception as e:
            logger.warning(f"AI resolution failed: {e}")
            return AiResolutionResponse(
                ticket_id=ticket_id,
                summary=f"Resolved issue regarding {title}.",
                solution="Applied standard configuration adjustment and verified connectivity.",
                steps=["Investigated issue", "Applied fix", "Verified recovery"],
                articles=[AiArticleReference(id=a["id"], title=a["title"]) for a in (kb_articles or [])[:3]],
            )

    def chat(
        self,
        user_id: int,
        message: str,
        conversation_id: Optional[str] = None,
        kb_articles: List[Dict[str, Any]] = None,
    ) -> AiChatResponse:
        # Retrieve short history from cache
        conv_key = f"ai_chat:{user_id}:{conversation_id or 'default'}"
        history: List[Dict[str, str]] = self.cache.get(conv_key) or []

        # Prepare KB context
        kb_str = "\n".join([f"[{a['category']}] {a['title']}: {a.get('content', '')[:120]}..." for a in (kb_articles or [])[:5]])
        sys_prompt = IT_CHAT_PROMPT.format(kb_context=kb_str or "No matching KB articles found.")

        history.append({"role": "user", "content": message})
        # Keep last 6 messages
        trimmed_history = history[-6:]

        try:
            raw = self.provider.complete(
                system_prompt=sys_prompt,
                messages=trimmed_history,
                json_mode=True,
            )
            parsed = _extract_json(raw)
            reply = str(parsed.get("reply", "I am here to help with your IT inquiries."))
            suggest_ticket = bool(parsed.get("suggest_ticket", False))

            ticket_draft = None
            if suggest_ticket and "ticket_draft" in parsed and isinstance(parsed["ticket_draft"], dict):
                td = parsed["ticket_draft"]
                cat_val = str(td.get("category", "OTHER")).upper()
                try:
                    category = TicketCategory(cat_val)
                except Exception:
                    category = TicketCategory.OTHER

                pri_val = str(td.get("priority", "MEDIUM")).upper()
                try:
                    priority = TicketPriority(pri_val)
                except Exception:
                    priority = TicketPriority.MEDIUM

                ticket_draft = TicketDraft(
                    title=str(td.get("title", message[:50])),
                    description=str(td.get("description", message)),
                    category=category,
                    priority=priority,
                )

            # Save updated history
            history.append({"role": "assistant", "content": reply})
            self.cache.set(conv_key, history[-8:], ttl_seconds=3600)

            return AiChatResponse(
                reply=reply,
                suggest_ticket=suggest_ticket,
                ticket_draft=ticket_draft,
                conversation_id=conversation_id,
            )
        except Exception as e:
            logger.warning(f"AI chat completion failed: {e}")
            fallback_reply = (
                "I am your HelpDesk-360 assistant. I can help answer common questions regarding WiFi, VPN, passwords, "
                "or assist you in creating a support ticket for our technicians."
            )
            return AiChatResponse(
                reply=fallback_reply,
                suggest_ticket=False,
                ticket_draft=None,
                conversation_id=conversation_id,
            )


_ai_service: Optional[AIService] = None


def get_ai_service() -> AIService:
    global _ai_service
    if _ai_service is None:
        _ai_service = AIService()
    return _ai_service
