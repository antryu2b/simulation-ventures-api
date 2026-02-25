"""Data models for SimVentures"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime


class SimulationRequest(BaseModel):
    """시뮬레이션 요청"""
    start_date: str = Field(default="2020-01-01", description="시작 날짜 (YYYY-MM-DD)")
    end_date: str = Field(default=None, description="종료 날짜 (YYYY-MM-DD)")
    scenarios: List[str] = Field(
        default=["baseline", "dovish", "hawkish"],
        description="분석 시나리오"
    )


class TimeSeriesData(BaseModel):
    """시계열 데이터"""
    date: str
    value: float


class SimulationResult(BaseModel):
    """시뮬레이션 결과"""
    timeline: List[Dict]
    summary: Dict
    timestamp: str


class ScenarioResult(BaseModel):
    """시나리오 분석 결과"""
    scenarios: Dict[str, Dict]
    timestamp: str


class HealthResponse(BaseModel):
    """헬스 체크"""
    status: str
    version: str


class APIResponse(BaseModel):
    """API 기본 응답"""
    message: str
    version: str
    tools: List[str]
