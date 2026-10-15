from math import ceil
from typing import Any, Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field
from fastapi import Query

T = TypeVar("T")


class PaginationParams:
    def __init__(
        self,
        page: int = Query(1, ge=1, description="Page number, 1-indexed"),
        page_size: int = Query(10, ge=1, le=100, description="Items per page"),
        sort_by: Optional[str] = Query(None, description="Field to sort by"),
        order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    ):
        self.page = page
        self.page_size = page_size
        self.sort_by = sort_by
        self.order = order.lower()

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        return self.page_size


class PaginatedData(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    pages: int


def paginate_data(items: List[Any], total: int, params: PaginationParams) -> dict:
    pages = ceil(total / params.page_size) if total > 0 else 1
    return {
        "items": items,
        "total": total,
        "page": params.page,
        "page_size": params.page_size,
        "pages": pages,
    }
