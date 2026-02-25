"""
AlphaRisk 라우터
기관 회의주의자 블룸버그 터미널
엔드포인트: /api/alpharisk/*
"""

from fastapi import APIRouter, HTTPException
from typing import Dict
import logging

from app.services.portfolio_engine import get_portfolio_engine

router = APIRouter(prefix="/api/alpharisk", tags=["AlphaRisk"])
logger = logging.getLogger(__name__)

@router.get("/health")
async def alpharisk_health():
    """AlphaRisk 헬스 체크"""
    return {
        "status": "healthy",
        "product": "AlphaRisk",
        "version": "0.1.0",
        "description": "기관 회의주의자 블룸버그 터미널"
    }

@router.post("/analyze")
async def analyze_portfolio(
    weights: Dict[str, float],
    returns: Dict[str, float],
):
    """
    포트폴리오 리스크 분석
    
    Body:
    {
        "weights": {"US Stock": 0.4, "Bonds": 0.3, ...},
        "returns": {"US Stock": 0.10, "Bonds": 0.04, ...}
    }
    """
    try:
        # 검증
        if not weights or sum(weights.values()) == 0:
            raise HTTPException(status_code=400, detail="가중치 합이 1.0이어야 합니다")
        
        # 가중치 정규화
        total = sum(weights.values())
        weights = {k: v / total for k, v in weights.items()}
        
        engine = get_portfolio_engine()
        result = engine.analyze_portfolio(weights, returns)
        
        return {
            "status": "success",
            "analysis": result,
        }
    except Exception as e:
        logger.error(f"분석 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/frontier")
async def efficient_frontier(num_portfolios: int = 50):
    """
    효율적 프론티어 계산
    (위험 vs 수익률 그래프용)
    """
    try:
        engine = get_portfolio_engine()
        result = engine.efficient_frontier(num_portfolios)
        
        return {
            "status": "success",
            "frontier": result,
        }
    except Exception as e:
        logger.error(f"프론티어 계산 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/heatmap")
async def risk_heatmap(weights: Dict[str, float]):
    """
    리스크 상관도 열량도
    (자산 간 상관관계 시각화)
    """
    try:
        engine = get_portfolio_engine()
        result = engine.risk_heatmap(weights)
        
        return {
            "status": "success",
            "heatmap": result,
        }
    except Exception as e:
        logger.error(f"열량도 생성 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/default-portfolio")
async def get_default_portfolio():
    """기본 포트폴리오 설정"""
    return {
        "weights": {
            "US Stock": 0.40,
            "Bonds": 0.30,
            "Real Estate": 0.15,
            "Commodities": 0.10,
            "Cash": 0.05,
        },
        "returns": {
            "US Stock": 0.10,
            "Bonds": 0.04,
            "Real Estate": 0.07,
            "Commodities": 0.05,
            "Cash": 0.02,
        },
    }
