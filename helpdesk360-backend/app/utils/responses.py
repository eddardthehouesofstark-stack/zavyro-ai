from typing import Any, Generic, Optional, TypeVar
from pydantic import BaseModel
from fastapi.responses import JSONResponse

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str = "Operation successful"
    data: Optional[T] = None


class ApiErrorResponse(BaseModel):
    success: bool = False
    message: str = "An error occurred"
    error: Optional[Any] = None


def success_response(
    data: Any = None,
    message: str = "Operation successful",
    status_code: int = 200,
) -> JSONResponse:
    content = {
        "success": True,
        "message": message,
        "data": data,
    }
    return JSONResponse(status_code=status_code, content=content)


def error_response(
    message: str = "An error occurred",
    error: Any = None,
    status_code: int = 400,
) -> JSONResponse:
    content = {
        "success": False,
        "message": message,
        "error": error,
    }
    return JSONResponse(status_code=status_code, content=content)
