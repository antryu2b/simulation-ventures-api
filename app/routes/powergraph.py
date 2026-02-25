"""
PowerGraph 라우터
네트워크 인텔리전스 + 리스크 전파
엔드포인트: /api/powergraph/*
"""

from fastapi import APIRouter, HTTPException
import logging

from app.services.network_engine import get_network_engine

router = APIRouter(prefix="/api/powergraph", tags=["PowerGraph"])
logger = logging.getLogger(__name__)

@router.get("/health")
async def powergraph_health():
    """PowerGraph 헬스 체크"""
    return {
        "status": "healthy",
        "product": "PowerGraph",
        "version": "0.1.0",
        "description": "네트워크 인텔리전스 + 리스크 전파"
    }

@router.get("/network")
async def get_network():
    """
    금융 네트워크 조회
    (D3.js 시각화용)
    """
    try:
        engine = get_network_engine()
        network = engine.generate_network()
        
        return {
            "status": "success",
            "network": network,
        }
    except Exception as e:
        logger.error(f"네트워크 조회 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/contagion/{institution}")
async def analyze_contagion(institution: str):
    """
    리스크 전염 분석
    
    Query Parameters:
    - institution: 실패한 기관명
    """
    try:
        engine = get_network_engine()
        result = engine.analyze_contagion(institution)
        
        return {
            "status": "success",
            "contagion": result,
        }
    except Exception as e:
        logger.error(f"전염 분석 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/systemic-risk")
async def get_systemic_risk():
    """
    시스템 리스크 계산
    """
    try:
        engine = get_network_engine()
        risk = engine.calculate_systemic_risk()
        
        return {
            "status": "success",
            "risk": risk,
        }
    except Exception as e:
        logger.error(f"시스템 리스크 계산 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/institutions")
async def list_institutions():
    """금융기관 목록"""
    try:
        engine = get_network_engine()
        institutions = []
        
        for name, data in engine.institutions.items():
            institutions.append({
                "name": name,
                "type": data["type"],
                "risk": data["risk"],
                "color": data["color"],
            })
        
        return {
            "status": "success",
            "institutions": institutions,
        }
    except Exception as e:
        logger.error(f"기관 목록 조회 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))
