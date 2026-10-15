from typing import List, Optional, Any, Dict
from pydantic import BaseModel


class SearchResultItem(BaseModel):
    type: str  # ticket | user | knowledge
    id: int
    title: str
    subtitle: Optional[str] = None
    extra: Optional[Dict[str, Any]] = None


class SearchResponse(BaseModel):
    query: str
    type_filter: str
    total: int
    results: List[SearchResultItem]
