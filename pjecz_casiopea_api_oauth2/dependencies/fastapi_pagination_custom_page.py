"""
FastAPI Pagination Custom Page
"""

from abc import ABC
from typing import Any, Generic, Optional, Sequence, TypeVar

from fastapi import Query
from fastapi_pagination.bases import AbstractPage, AbstractParams
from fastapi_pagination.limit_offset import LimitOffsetParams
from fastapi_pagination.types import GreaterEqualOne, GreaterEqualZero
from typing_extensions import Self


class CustomPageParams(LimitOffsetParams):
    """
    Custom Page Params
    """

    offset: int = Query(0, ge=0, description="Page offset")
    limit: int = Query(10, ge=1, le=100, description="Page size limit")


T = TypeVar("T")


class CustomPage(AbstractPage[T], Generic[T], ABC):
    """
    Custom Page
    """

    success: bool
    message: str
    data: Sequence[T]

    total: Optional[GreaterEqualZero]
    limit: Optional[GreaterEqualOne]
    offset: Optional[GreaterEqualZero]

    __params_type__ = CustomPageParams

    @classmethod
    def create(
        cls,
        items: Sequence[T],
        params: AbstractParams,
        total: Optional[int] = None,
        **kwargs: Any,
    ) -> Self:
        """
        Create Custom Page
        """
        raw_params = params.to_raw_params().as_limit_offset()

        if total is None or total == 0:
            return cls(
                success=False,
                message="No se encontraron registros",
                data=[],
                total=0,
                limit=raw_params.limit,
                offset=raw_params.offset,
            )

        return cls(
            success=True,
            message="Success",
            data=items,
            total=total,
            limit=raw_params.limit,
            offset=raw_params.offset,
            **kwargs,
        )
