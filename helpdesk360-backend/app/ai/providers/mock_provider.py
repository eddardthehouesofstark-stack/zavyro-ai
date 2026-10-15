import json
import re
from typing import List, Dict
from app.ai.base import AIProvider


class MockAIProvider(AIProvider):
    def complete(
        self,
        system_prompt: str,
        messages: List[Dict[str, str]],
        json_mode: bool = False,
        timeout_seconds: int = 15,
    ) -> str:
        last_message = messages[-1]["content"] if messages else ""
        text = last_message.lower()

        # 1. TICKET ANALYSIS
        if "expert it triage ai" in system_prompt.lower() or "triage" in system_prompt.lower():
            category = "SOFTWARE"
            priority = "MEDIUM"
            summary = "Employee support request requiring technician triage."
            suggested_action = "Review system logs and perform initial diagnostic."

            if any(w in text for w in ["vpn", "wifi", "wi-fi", "network", "dns", "gateway", "internet", "ethernet"]):
                category = "NETWORK"
                priority = "HIGH" if any(w in text for w in ["drop", "disconnect", "down", "fail"]) else "MEDIUM"
                summary = "Network or VPN connection dropouts impacting remote connectivity."
                suggested_action = "Check local adapter MTU, flush DNS cache, and verify VPN gateway status."
            elif any(w in text for w in ["laptop", "monitor", "screen", "dock", "battery", "charger", "hardware", "power", "turn on", "turning on"]):
                category = "HARDWARE"
                priority = "HIGH" if any(w in text for w in ["battery", "power", "dead", "smoke"]) else "MEDIUM"
                summary = "Hardware peripheral or workstation power failure."
                suggested_action = "Check charger and battery health; perform hard reset and test with secondary power cable."
            elif any(w in text for w in ["access", "permission", "password", "login", "iam", "aws", "mfa", "token", "sso"]):
                category = "ACCESS"
                priority = "CRITICAL" if any(w in text for w in ["prod", "production", "blocked", "urgent"]) else "HIGH"
                summary = "Account authentication or IAM access elevation request."
                suggested_action = "Verify requester authorization and provision temporary access credentials."
            elif any(w in text for w in ["email", "outlook", "mailbox", "spam", "smtp"]):
                category = "EMAIL"
                priority = "MEDIUM"
                summary = "Corporate email routing or mailbox configuration problem."
                suggested_action = "Verify email client sync settings and check exchange server health."
            elif any(w in text for w in ["phishing", "malware", "virus", "hacked", "security", "compromised"]):
                category = "SECURITY"
                priority = "CRITICAL"
                summary = "Potential security incident or compromised endpoint reported."
                suggested_action = "Isolate machine from network and perform automated security scan."
            elif any(w in text for w in ["crash", "figma", "slack", "software", "bug", "freeze", "error"]):
                category = "SOFTWARE"
                priority = "HIGH" if "crash" in text else "MEDIUM"
                summary = "Software application crash or runtime error."
                suggested_action = "Clear app cache, restart background services, and verify latest patch installation."

            if any(w in text for w in ["critical", "emergency", "production down", "urgent blocker"]):
                priority = "CRITICAL"

            return json.dumps({
                "category": category,
                "priority": priority,
                "summary": summary,
                "suggested_action": suggested_action,
            })

        # 2. TECHNICIAN TROUBLESHOOT
        if "senior systems engineer" in system_prompt.lower() or "troubleshoot" in system_prompt.lower():
            return json.dumps({
                "steps": [
                    "Inspect device diagnostics log and recent OS updates.",
                    "Verify connectivity and authentication status with central directory.",
                    "Execute safe mode restart or cache purge.",
                    "Perform remote diagnostic probe and confirm telemetry values.",
                ]
            })

        # 3. TECHNICIAN RESOLUTION
        if "it architect resolving" in system_prompt.lower() or "resolution" in system_prompt.lower():
            return json.dumps({
                "summary": "Root cause identified as configuration mismatch on client endpoint.",
                "solution": "Applied standard configuration profile and flushed local application cache.",
                "steps": [
                    "Isolated failing module or corrupted cache.",
                    "Pushed updated corporate configuration payload.",
                    "Verified service recovery and confirmed with employee.",
                ],
            })

        # 4. IT CHAT ASSISTANT
        if "it virtual assistant" in system_prompt.lower() or "knowledge base context" in system_prompt.lower():
            # Check for non-IT topics
            if any(w in text for w in ["weather", "recipe", "poem", "sports", "movie", "president", "politics"]):
                return json.dumps({
                    "reply": "I am the HelpDesk-360 IT assistant. I can only assist with IT, enterprise tech, and workplace productivity questions.",
                    "suggest_ticket": False,
                    "ticket_draft": None,
                })

            if any(w in text for w in ["broken", "cannot fix", "replace", "hardware failure", "smoke", "spill", "water", "stolen", "lost"]):
                return json.dumps({
                    "reply": "This issue requires physical technician intervention. I have prepared a ticket draft for you. Would you like me to submit it?",
                    "suggest_ticket": True,
                    "ticket_draft": {
                        "title": "Hardware service request: Physical equipment incident",
                        "description": last_message,
                        "category": "HARDWARE",
                        "priority": "HIGH",
                    },
                })

            if any(w in text for w in ["wifi", "wi-fi", "internet"]):
                return json.dumps({
                    "reply": "For WiFi connectivity issues: 1) Toggle WiFi off and on. 2) Ensure you are connecting to 'Company-Secure'. 3) If issues persist, forget the network and reconnect with your domain credentials.",
                    "suggest_ticket": False,
                    "ticket_draft": None,
                })

            if any(w in text for w in ["vpn"]):
                return json.dumps({
                    "reply": "To connect to the corporate VPN: 1) Open Cisco AnyConnect. 2) Target 'vpn.company.com'. 3) Approve the MFA push on your phone. If drops continue, lower MTU to 1350.",
                    "suggest_ticket": False,
                    "ticket_draft": None,
                })

            if any(w in text for w in ["password", "reset", "forgot"]):
                return json.dumps({
                    "reply": "To reset your corporate password, visit https://auth.company.com/recover from any browser or contact your manager to approve an identity reset.",
                    "suggest_ticket": False,
                    "ticket_draft": None,
                })

            return json.dumps({
                "reply": "I can help you troubleshoot IT issues! You can ask me about VPN setup, WiFi, password resets, hardware troubleshooting, or software installation.",
                "suggest_ticket": False,
                "ticket_draft": None,
            })

        # Default fallback
        if json_mode:
            return json.dumps({"result": "Analysis completed successfully."})
        return "HelpDesk-360 AI Assistant: Issue analyzed and processed successfully."
