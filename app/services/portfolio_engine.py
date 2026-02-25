"""
AlphaRisk 포트폴리오 리스크 분석 엔진
기관 회의주의자를 위한 블룸버그 터미널
"""

import numpy as np
import pandas as pd
from typing import Dict, List
from datetime import datetime

class PortfolioRiskEngine:
    """포트폴리오 리스크 분석 엔진"""
    
    def __init__(self):
        """기본 자산 상관관계 및 위험도 초기화"""
        self.assets = {
            "US Stock": {"vol": 0.18, "color": "#3b82f6"},
            "Bonds": {"vol": 0.06, "color": "#10b981"},
            "Real Estate": {"vol": 0.12, "color": "#f59e0b"},
            "Commodities": {"vol": 0.20, "color": "#ef4444"},
            "Cash": {"vol": 0.01, "color": "#8b5cf6"},
        }
    
    def analyze_portfolio(
        self,
        weights: Dict[str, float],
        returns: Dict[str, float],
    ) -> Dict:
        """
        포트폴리오 리스크 분석
        
        Args:
            weights: 자산별 가중치 (합 = 1.0)
            returns: 자산별 예상 수익률
        
        Returns:
            포트폴리오 리스크 분석 결과
        """
        assets_list = list(weights.keys())
        w = np.array(list(weights.values()))
        
        # 예상 수익률
        r = np.array([returns.get(asset, 0.05) for asset in assets_list])
        expected_return = float(np.dot(w, r))
        
        # 상관관계 행렬 (간단한 버전)
        n = len(assets_list)
        cov_matrix = np.zeros((n, n))
        
        for i, asset1 in enumerate(assets_list):
            for j, asset2 in enumerate(assets_list):
                vol1 = self.assets[asset1]["vol"]
                vol2 = self.assets[asset2]["vol"]
                
                if i == j:
                    cov_matrix[i, j] = vol1 * vol2
                else:
                    # 상관도 0.3 ~ 0.6
                    correlation = 0.4
                    cov_matrix[i, j] = correlation * vol1 * vol2
        
        # 포트폴리오 분산 및 표준편차
        portfolio_var = float(np.dot(w, np.dot(cov_matrix, w)))
        portfolio_vol = float(np.sqrt(portfolio_var))
        
        # Sharpe 비율 (무위험 이율 2%)
        risk_free_rate = 0.02
        sharpe_ratio = float((expected_return - risk_free_rate) / max(portfolio_vol, 0.001))
        
        # VaR (95% 신뢰도, 1일)
        z_score = 1.645
        var_95 = float(z_score * portfolio_vol)
        
        # 자산별 리스크 기여도
        risk_contribution = {}
        for i, asset in enumerate(assets_list):
            marginal_contrib = float(cov_matrix[i, i] * w[i] / max(portfolio_vol, 0.001))
            risk_contribution[asset] = marginal_contrib
        
        return {
            "portfolio": {
                "expected_return": expected_return,
                "volatility": portfolio_vol,
                "sharpe_ratio": sharpe_ratio,
                "var_95": var_95,
            },
            "assets": {
                asset: {
                    "weight": float(weights[asset]),
                    "volatility": self.assets[asset]["vol"],
                    "expected_return": returns.get(asset, 0.05),
                    "risk_contribution": risk_contribution.get(asset, 0),
                }
                for asset in assets_list
            },
            "timestamp": datetime.now().isoformat(),
        }
    
    def efficient_frontier(
        self,
        num_portfolios: int = 50,
    ) -> Dict:
        """
        효율적 프론티어 계산 (50개 포트폴리오)
        """
        assets_list = list(self.assets.keys())
        frontier_portfolios = []
        
        for _ in range(num_portfolios):
            # 랜덤 가중치
            weights = np.random.random(len(assets_list))
            weights /= weights.sum()
            
            weight_dict = {asset: float(w) for asset, w in zip(assets_list, weights)}
            
            # 수익률 분포
            returns = {
                "US Stock": 0.10,
                "Bonds": 0.04,
                "Real Estate": 0.07,
                "Commodities": 0.05,
                "Cash": 0.02,
            }
            
            result = self.analyze_portfolio(weight_dict, returns)
            
            frontier_portfolios.append({
                "volatility": result["portfolio"]["volatility"],
                "return": result["portfolio"]["expected_return"],
                "sharpe": result["portfolio"]["sharpe_ratio"],
            })
        
        return {
            "frontier": frontier_portfolios,
            "timestamp": datetime.now().isoformat(),
        }
    
    def risk_heatmap(self, weights: Dict[str, float]) -> Dict:
        """
        리스크 열량도 (자산 간 상관도)
        """
        assets_list = list(weights.keys())
        n = len(assets_list)
        
        heatmap = []
        for i, asset1 in enumerate(assets_list):
            row = []
            for j, asset2 in enumerate(assets_list):
                if i == j:
                    correlation = 1.0
                else:
                    correlation = 0.4  # 기본 상관도
                
                row.append({
                    "asset1": asset1,
                    "asset2": asset2,
                    "correlation": correlation,
                    "color": self._correlation_to_color(correlation),
                })
            heatmap.append(row)
        
        return {
            "heatmap": heatmap,
            "assets": assets_list,
            "timestamp": datetime.now().isoformat(),
        }
    
    def _correlation_to_color(self, correlation: float) -> str:
        """상관도를 색상으로 변환 (1.0=빨강, 0.0=파랑, -1.0=초록)"""
        if correlation > 0:
            intensity = int(255 * correlation)
            return f"#ff{165-intensity:02x}{165-intensity:02x}"
        else:
            intensity = int(255 * abs(correlation))
            return f"#{165-intensity:02x}ff{165-intensity:02x}"


# 싱글톤 인스턴스
_portfolio_engine: PortfolioRiskEngine = PortfolioRiskEngine()

def get_portfolio_engine() -> PortfolioRiskEngine:
    """포트폴리오 엔진 싱글톤"""
    return _portfolio_engine
