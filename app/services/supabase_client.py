"""Supabase 클라이언트"""
import os
from supabase import create_client, Client
from datetime import datetime
import json

# Supabase 초기화
url = os.getenv("SUPABASE_URL", "https://akojqymimzxkqtfwryel.supabase.co")
key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not key:
    raise ValueError("SUPABASE_SERVICE_ROLE_KEY is not set in .env")

supabase: Client = create_client(url, key)


async def save_simshield_data(date: str, m2: float, cpi: float, scenario: str) -> dict:
    """SimShield 데이터 저장"""
    try:
        response = supabase.table("simshield_data").insert({
            "date": date,
            "m2": m2,
            "cpi": cpi,
            "scenario": scenario
        }).execute()
        return response.data[0] if response.data else {}
    except Exception as e:
        print(f"Error saving simshield data: {e}")
        return {}


async def get_simshield_data(scenario: str = None) -> list:
    """SimShield 데이터 조회"""
    try:
        query = supabase.table("simshield_data")
        
        if scenario:
            response = query.select("*").eq("scenario", scenario).order("date", desc=False).execute()
        else:
            response = query.select("*").order("date", desc=False).execute()
        
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching simshield data: {e}")
        return []


async def save_alpharisk_portfolio(portfolio_name: str, assets: dict, 
                                   sharpe_ratio: float, volatility: float, 
                                   var_value: float) -> dict:
    """AlphaRisk 포트폴리오 저장"""
    try:
        response = supabase.table("alpharisk_portfolio").insert({
            "portfolio_name": portfolio_name,
            "assets": assets,
            "sharpe_ratio": sharpe_ratio,
            "volatility": volatility,
            "var_value": var_value
        }).execute()
        return response.data[0] if response.data else {}
    except Exception as e:
        print(f"Error saving portfolio: {e}")
        return {}


async def get_alpharisk_portfolios() -> list:
    """AlphaRisk 포트폴리오 조회"""
    try:
        response = supabase.table("alpharisk_portfolio").select("*").execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching portfolios: {e}")
        return []


async def update_alpharisk_portfolio(portfolio_id: int, **kwargs) -> dict:
    """AlphaRisk 포트폴리오 업데이트"""
    try:
        response = supabase.table("alpharisk_portfolio").update(kwargs).eq("id", portfolio_id).execute()
        return response.data[0] if response.data else {}
    except Exception as e:
        print(f"Error updating portfolio: {e}")
        return {}
