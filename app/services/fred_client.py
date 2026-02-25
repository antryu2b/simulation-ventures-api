"""
FRED API 클라이언트
Federal Reserve Economic Data (https://fred.stlouisfed.org/)
"""

import os
import httpx
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional
import asyncio

class FREDClient:
    """FRED API 클라이언트 - 경제 데이터 조회"""
    
    BASE_URL = "https://api.stlouisfed.org/fred"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        FRED API 초기화
        
        Args:
            api_key: FRED API 키 (환경변수에서 자동 로드)
        """
        self.api_key = api_key or os.getenv("FRED_API_KEY", "demo")
        self.client = httpx.AsyncClient(timeout=10.0)
    
    async def get_series(
        self,
        series_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        FRED 데이터 계열 조회
        
        Args:
            series_id: FRED 계열 ID (예: "M2", "CPIAUCSL")
            start_date: 시작 날짜 (YYYY-MM-DD)
            end_date: 종료 날짜 (YYYY-MM-DD)
        
        Returns:
            pandas DataFrame
        """
        try:
            # 기본값 설정
            if not end_date:
                end_date = datetime.now().strftime("%Y-%m-%d")
            if not start_date:
                # 기본: 5년 전
                start_date = (datetime.now() - timedelta(days=365*5)).strftime("%Y-%m-%d")
            
            url = f"{self.BASE_URL}/series/observations"
            params = {
                "series_id": series_id,
                "api_key": self.api_key,
                "file_type": "json",
                "observation_start": start_date,
                "observation_end": end_date,
            }
            
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # DataFrame 변환
            observations = data.get("observations", [])
            df = pd.DataFrame(observations)
            df["date"] = pd.to_datetime(df["date"])
            df["value"] = pd.to_numeric(df["value"], errors="coerce")
            df = df.dropna(subset=["value"])
            
            return df
        
        except Exception as e:
            print(f"❌ FRED API 오류 ({series_id}): {e}")
            return pd.DataFrame()
    
    async def get_m2_inflation_cpi(self) -> dict:
        """
        SimShield용 핵심 데이터:
        M2 (통화량) + CPI (인플레이션) 조회
        """
        try:
            # 병렬 요청
            m2_task = self.get_series("M2", start_date="2010-01-01")
            cpi_task = self.get_series("CPIAUCSL", start_date="2010-01-01")
            
            m2_df, cpi_df = await asyncio.gather(m2_task, cpi_task)
            
            return {
                "m2": m2_df.to_dict(orient="records") if not m2_df.empty else [],
                "cpi": cpi_df.to_dict(orient="records") if not cpi_df.empty else [],
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            print(f"❌ 데이터 조회 오류: {e}")
            return {"error": str(e)}
    
    async def close(self):
        """클라이언트 종료"""
        await self.client.aclose()


# 싱글톤 인스턴스
_fred_client: Optional[FREDClient] = None

async def get_fred_client() -> FREDClient:
    """FRED 클라이언트 싱글톤"""
    global _fred_client
    if _fred_client is None:
        _fred_client = FREDClient()
    return _fred_client
