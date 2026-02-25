"""
SimShield + AlphaRisk + PowerGraph 통합 API
Shared simulation engine for 3 products
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

# 라우터
from app.routes import simshield, alpharisk

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Simulation Ventures API",
    description="SimShield + AlphaRisk + PowerGraph 통합 API",
    version="0.1.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(simshield.router)
app.include_router(alpharisk.router)

@app.get("/health")
async def health_check():
    """헬스 체크"""
    logger.info("Health check requested")
    return JSONResponse({"status": "healthy", "version": "0.1.0"})

@app.get("/")
async def root():
    """API 정보"""
    logger.info("Root endpoint accessed")
    return {
        "message": "SimVentures API is running",
        "version": "0.1.0",
        "tools": ["SimShield", "AlphaRisk", "PowerGraph"],
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "simshield": "/api/simshield/health"
        }
    }

@app.on_event("startup")
async def startup_event():
    """앱 시작"""
    logger.info("🚀 SimVentures API Starting...")
    logger.info("📊 Products: SimShield | AlphaRisk | PowerGraph")
    logger.info("📖 Swagger Docs: http://localhost:8000/docs")
    
    # FRED API 키 확인
    fred_key = os.getenv("FRED_API_KEY", "demo")
    if fred_key != "demo":
        logger.info(f"✅ FRED API 키 설정: {fred_key[:8]}...")
    else:
        logger.warning("⚠️ FRED API 데모 키 사용 (제한됨)")

@app.on_event("shutdown")
async def shutdown_event():
    """앱 종료"""
    logger.info("🛑 SimVentures API Shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
