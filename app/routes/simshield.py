"""
SimShield 라우터
개인 재정 방어 시뮬레이터
엔드포인트: /api/simshield/*
"""

from fastapi import APIRouter, HTTPException
from typing import Optional
import logging

from app.models import SimulationRequest, SimulationResult, ScenarioResult
from app.services.fred_client import get_fred_client
from app.services.simulation_engine import get_simulation_engine
from app.services.supabase_client import get_simshield_data, save_simshield_data
from app.services.fred_to_supabase import populate_simshield_data

router = APIRouter(prefix="/api/simshield", tags=["SimShield"])
logger = logging.getLogger(__name__)

@router.get("/health")
async def simshield_health():
    """SimShield 헬스 체크"""
    return {
        "status": "healthy",
        "product": "SimShield",
        "version": "0.1.0",
        "description": "개인 재정 방어 시뮬레이터"
    }

@router.get("/data")
async def get_economic_data(
    scenario: Optional[str] = "baseline",
    refresh: bool = False,
):
    """
    경제 데이터 조회 (M2 + CPI) - Supabase 저장 데이터 사용
    
    Query Parameters:
    - scenario: 시나리오 (baseline, dovish, hawkish)
    - refresh: FRED에서 새로 조회 (True일 때)
    """
    try:
        # 새로고침 요청 시 FRED에서 데이터 가져오기
        if refresh:
            await populate_simshield_data()
        
        # Supabase에서 데이터 조회
        data = await get_simshield_data(scenario=scenario)
        
        if not data:
            return {
                "status": "no_data",
                "message": f"{scenario} 시나리오 데이터가 없습니다.",
                "data": []
            }
        
        return {
            "status": "success",
            "scenario": scenario,
            "count": len(data),
            "data": data,
            "note": "M2 = 통화량, CPI = 소비자물가지수"
        }
    except Exception as e:
        logger.error(f"경제 데이터 조회 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/simulate")
async def run_simulation(request: SimulationRequest):
    """
    통화 가치 침식 시뮬레이션 실행
    
    Body:
    - start_date: 시작 날짜
    - end_date: 종료 날짜
    - scenarios: 분석 시나리오
    """
    try:
        fred = await get_fred_client()
        engine = get_simulation_engine()
        
        # FRED 데이터 조회
        m2_data = await fred.get_series("M2", start_date=request.start_date, end_date=request.end_date)
        cpi_data = await fred.get_series("CPIAUCSL", start_date=request.start_date, end_date=request.end_date)
        
        if m2_data.empty or cpi_data.empty:
            raise HTTPException(status_code=400, detail="데이터 조회 실패")
        
        # 시뮬레이션 실행
        m2_list = m2_data[["date", "value"]].to_dict(orient="records")
        cpi_list = cpi_data[["date", "value"]].to_dict(orient="records")
        asset_prices = [100] * len(m2_list)  # 기본값
        
        result = engine.simulate_currency_erosion(m2_list, cpi_list, asset_prices)
        
        return {
            "status": "success",
            "result": result
        }
    except Exception as e:
        logger.error(f"시뮬레이션 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/scenarios")
async def analyze_scenarios(
    m2: float = 21_500.0,  # 2024년 1월 기준 (십억 달러)
    cpi: float = 308.417,  # 2024년 1월 기준
):
    """
    정책 시나리오 분석 (12개월 예측)
    
    Baseline: 현재 추세 유지
    Dovish: 금리 인하 시나리오
    Hawkish: 금리 인상 시나리오
    """
    try:
        engine = get_simulation_engine()
        result = engine.scenario_analysis(m2, cpi)
        
        return {
            "status": "success",
            "analysis": result,
            "description": {
                "baseline": "중립적 금리 추세",
                "dovish": "금리 인하 → 통화 확대",
                "hawkish": "금리 인상 → 통화 긴축"
            }
        }
    except Exception as e:
        logger.error(f"시나리오 분석 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/purchasing-power")
async def get_purchasing_power(
    years: int = 5,
):
    """
    구매력 변화 추이 (최근 N년)
    
    Query Parameters:
    - years: 조회 기간 (년)
    """
    try:
        fred = await get_fred_client()
        
        # CPI 조회
        cpi_data = await fred.get_series("CPIAUCSL", start_date=f"{2024-years}-01-01")
        
        if cpi_data.empty:
            raise HTTPException(status_code=400, detail="CPI 데이터 조회 실패")
        
        # 구매력 계산 (기준: 2024년 1월)
        base_cpi = cpi_data.iloc[-1]["value"]  # 최신 CPI
        cpi_data["purchasing_power"] = (base_cpi / cpi_data["value"]) * 100
        
        result = cpi_data[["date", "value", "purchasing_power"]].to_dict(orient="records")
        
        return {
            "status": "success",
            "data": result,
            "note": "구매력 = 100 / (CPI / 기준CPI), 기준 = 2024년 1월"
        }
    except Exception as e:
        logger.error(f"구매력 조회 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))
