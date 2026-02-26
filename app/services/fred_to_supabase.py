"""FRED API 데이터를 Supabase에 저장"""
import asyncio
import httpx
import os
from datetime import datetime, timedelta
from app.services.supabase_client import save_simshield_data, get_simshield_data

FRED_API_KEY = os.getenv("FRED_API_KEY", "5a82455c443b8dc10407b5651bda8f46")
FRED_BASE_URL = "https://api.stlouisfed.org/fred"


async def fetch_fred_data(series_id: str, start_date: str = None) -> list:
    """FRED에서 경제 데이터 조회"""
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json"
    }
    
    if start_date:
        params["observation_start"] = start_date
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{FRED_BASE_URL}/series/observations", params=params)
        data = response.json()
        return data.get("observations", [])


async def populate_simshield_data():
    """SimShield 데이터 Supabase에 저장"""
    print("🔄 SimShield 데이터 FRED에서 조회 중...")
    
    # FRED 시리즈
    m2_series = "M2SL"  # 통화량 (M2)
    cpi_series = "CPIAUCSL"  # 소비자 물가지수 (CPI)
    
    # 데이터 조회 (2020년부터)
    start_date = "2020-01-01"
    
    m2_data = await fetch_fred_data(m2_series, start_date)
    cpi_data = await fetch_fred_data(cpi_series, start_date)
    
    # 날짜별로 M2, CPI 매칭
    m2_dict = {obs["date"]: float(obs["value"]) for obs in m2_data if obs["value"] != "."}
    cpi_dict = {obs["date"]: float(obs["value"]) for obs in cpi_data if obs["value"] != "."}
    
    # 3개 시나리오 생성
    scenarios = ["baseline", "dovish", "hawkish"]
    
    # 기존 데이터 확인
    existing = await get_simshield_data()
    existing_dates = {item["date"] for item in existing}
    
    saved_count = 0
    
    for date_str in sorted(m2_dict.keys()):
        if date_str in cpi_dict and date_str not in existing_dates:
            m2 = m2_dict[date_str]
            cpi = cpi_dict[date_str]
            
            for scenario in scenarios:
                # 시나리오별 변수 추가 (간단히 M2 변동 반영)
                scenario_multiplier = {
                    "baseline": 1.0,
                    "dovish": 1.02,  # M2 +2%
                    "hawkish": 0.98  # M2 -2%
                }
                
                m2_adjusted = m2 * scenario_multiplier[scenario]
                
                await save_simshield_data(date_str, m2_adjusted, cpi, scenario)
                saved_count += 1
    
    print(f"✅ {saved_count}개 데이터 저장 완료!")
    return saved_count


if __name__ == "__main__":
    # 테스트 실행
    asyncio.run(populate_simshield_data())
