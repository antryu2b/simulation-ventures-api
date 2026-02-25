"""
SimShield 시뮬레이션 엔진
M2 (통화량) → 자산가격 → 구매력 침식 모델
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from datetime import datetime

class SimulationEngine:
    """통화정책 → 실물경제 영향 시뮬레이션"""
    
    def __init__(self):
        """상수 초기화"""
        # 경제 파라미터
        self.m2_elasticity = 0.85  # M2 증가량의 85%가 자산가격에 반영
        self.inflation_lag = 3  # 인플레이션 효과 3개월 후 나타남
        self.asset_price_elasticity = 1.2  # M2 1% 증가 → 자산가격 1.2% 증가
        self.purchasing_power_decay = -1.0  # M2 1% 증가 → 구매력 1% 감소
    
    def simulate_currency_erosion(
        self,
        m2_data: List[Dict],
        cpi_data: List[Dict],
        asset_prices: List[float],
    ) -> Dict:
        """
        통화 가치 침식 시뮬레이션
        
        Args:
            m2_data: FRED M2 데이터
            cpi_data: FRED CPI 데이터
            asset_prices: 자산가격 (S&P500, 주택, 등)
        
        Returns:
            시뮬레이션 결과 (m2, cpi, real_purchasing_power, asset_impact)
        """
        try:
            # DataFrame 변환
            m2_df = pd.DataFrame(m2_data).sort_values("date")
            cpi_df = pd.DataFrame(cpi_data).sort_values("date")
            
            # 월별 변화율 계산
            m2_df["m2_growth"] = m2_df["value"].pct_change() * 100
            cpi_df["cpi_growth"] = cpi_df["value"].pct_change() * 100
            
            # 병합
            merged = m2_df[["date", "value", "m2_growth"]].merge(
                cpi_df[["date", "value", "cpi_growth"]],
                on="date",
                suffixes=("_m2", "_cpi"),
                how="inner"
            )
            
            # 실질 구매력 (CPI 역수)
            merged["real_purchasing_power"] = (
                100 / merged["value_cpi"] * (merged["value_cpi"].iloc[0] / 100)
            )
            
            # 자산가격 영향 (M2 → 자산 인플레이션)
            merged["asset_impact"] = (
                merged["m2_growth"].fillna(0) * self.asset_price_elasticity
            )
            
            # 결과
            result = {
                "timeline": merged[["date", "value_m2", "value_cpi", "real_purchasing_power", "asset_impact"]].to_dict(orient="records"),
                "summary": {
                    "avg_m2_growth": merged["m2_growth"].mean(),
                    "avg_cpi_growth": merged["cpi_growth"].mean(),
                    "total_purchasing_power_loss": 100 - merged["real_purchasing_power"].iloc[-1],
                    "avg_asset_impact": merged["asset_impact"].mean(),
                },
                "timestamp": datetime.now().isoformat(),
            }
            
            return result
        
        except Exception as e:
            return {"error": str(e)}
    
    def scenario_analysis(
        self,
        current_m2: float,
        current_cpi: float,
        scenarios: List[str] = ["baseline", "dovish", "hawkish"]
    ) -> Dict:
        """
        통화정책 시나리오 분석
        
        Args:
            current_m2: 현재 M2 (조 달러)
            current_cpi: 현재 CPI
            scenarios: 시나리오 ("baseline": 현재 추세, "dovish": 금리 인하, "hawkish": 금리 인상)
        
        Returns:
            시나리오별 12개월 예측
        """
        results = {}
        
        for scenario in scenarios:
            if scenario == "baseline":
                m2_growth_rate = 0.003  # 월 0.3%
                inflation_rate = 0.002  # 월 0.2%
            elif scenario == "dovish":
                m2_growth_rate = 0.005  # 월 0.5%
                inflation_rate = 0.003  # 월 0.3%
            else:  # hawkish
                m2_growth_rate = 0.001  # 월 0.1%
                inflation_rate = 0.001  # 월 0.1%
            
            # 12개월 예측
            m2_values = []
            cpi_values = []
            purchasing_power = []
            
            m2 = current_m2
            cpi = current_cpi
            
            for month in range(1, 13):
                m2 *= (1 + m2_growth_rate)
                cpi *= (1 + inflation_rate)
                
                m2_values.append(float(m2))
                cpi_values.append(float(cpi))
                
                # 구매력 = 초기 구매력 / CPI 지수화
                pp = 100 / (cpi / current_cpi)
                purchasing_power.append(float(pp))
            
            results[scenario] = {
                "m2": m2_values,
                "cpi": cpi_values,
                "purchasing_power": purchasing_power,
                "12month_m2_change": ((m2_values[-1] / current_m2) - 1) * 100,
                "12month_pp_loss": 100 - purchasing_power[-1],
            }
        
        return {
            "scenarios": results,
            "timestamp": datetime.now().isoformat(),
        }


# 싱글톤 인스턴스
_engine: SimulationEngine = SimulationEngine()

def get_simulation_engine() -> SimulationEngine:
    """시뮬레이션 엔진 싱글톤"""
    return _engine
