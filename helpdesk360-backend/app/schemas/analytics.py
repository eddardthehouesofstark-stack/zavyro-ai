from typing import List, Dict, Any
from pydantic import BaseModel


class AnalyticsTotals(BaseModel):
    total: int
    open: int
    resolved: int
    pending: int
    unassigned: int


class TrendItem(BaseModel):
    date: str
    count: int


class DistributionItem(BaseModel):
    name: str
    value: int


class WorkloadItem(BaseModel):
    technician_id: int
    name: str
    open: int
    resolved: int


class AnalyticsDashboardResponse(BaseModel):
    totals: AnalyticsTotals
    avg_resolution_hours: float
    avg_first_response_hours: float
    sla_compliance_rate: float
    volume: List[TrendItem]
    categories: List[DistributionItem]
    priorities: List[DistributionItem]
    workload: List[WorkloadItem]
