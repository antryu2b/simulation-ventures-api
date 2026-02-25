"""
PowerGraph 네트워크 인텔리전스 엔진
금융 네트워크 + 리스크 전파 분석
"""

import numpy as np
from typing import Dict, List
from datetime import datetime
import random

class NetworkEngine:
    """금융 네트워크 분석 엔진"""
    
    def __init__(self):
        """금융기관 네트워크 초기화"""
        self.institutions = {
            "JPMorgan": {"type": "Bank", "risk": 0.3, "color": "#3b82f6"},
            "Goldman Sachs": {"type": "Investment Bank", "risk": 0.5, "color": "#8b5cf6"},
            "BlackRock": {"type": "Asset Manager", "risk": 0.2, "color": "#10b981"},
            "Vanguard": {"type": "Asset Manager", "risk": 0.15, "color": "#06b6d4"},
            "Morgan Stanley": {"type": "Investment Bank", "risk": 0.45, "color": "#f59e0b"},
            "Bank of America": {"type": "Bank", "risk": 0.35, "color": "#ef4444"},
            "Citadel": {"type": "Hedge Fund", "risk": 0.6, "color": "#ec4899"},
            "Berkshire": {"type": "Conglomerate", "risk": 0.1, "color": "#14b8a6"},
        }
    
    def generate_network(self) -> Dict:
        """
        금융 네트워크 생성
        
        Returns:
            노드(기관) + 엣지(거래) 데이터
        """
        # 노드 (금융기관)
        nodes = []
        for name, data in self.institutions.items():
            nodes.append({
                "id": name,
                "name": name,
                "type": data["type"],
                "risk": data["risk"],
                "size": random.randint(30, 80),
                "color": data["color"],
            })
        
        # 엣지 (거래 관계)
        edges = []
        institution_names = list(self.institutions.keys())
        
        for i, source in enumerate(institution_names):
            # 각 기관은 2-5개의 다른 기관과 거래
            num_connections = random.randint(2, 5)
            targets = random.sample(
                [n for j, n in enumerate(institution_names) if j != i],
                min(num_connections, len(institution_names) - 1)
            )
            
            for target in targets:
                exposure = random.uniform(0.5, 1.0)
                risk_level = (self.institutions[source]["risk"] + 
                             self.institutions[target]["risk"]) / 2
                
                edges.append({
                    "source": source,
                    "target": target,
                    "exposure": float(exposure),
                    "risk": float(risk_level),
                    "width": int(exposure * 10),
                    "color": self._risk_to_color(risk_level),
                })
        
        return {
            "nodes": nodes,
            "edges": edges,
            "timestamp": datetime.now().isoformat(),
        }
    
    def analyze_contagion(self, failing_institution: str) -> Dict:
        """
        리스크 전염 분석
        
        Args:
            failing_institution: 실패한 기관명
        
        Returns:
            전염 시뮬레이션 결과
        """
        network = self.generate_network()
        
        # 감염된 노드 추적
        infected = {failing_institution}
        contagion_path = [{
            "institution": failing_institution,
            "stage": 0,
            "risk": self.institutions[failing_institution]["risk"],
        }]
        
        # 3단계 전염 시뮬레이션
        for stage in range(1, 4):
            new_infected = set()
            
            for edge in network["edges"]:
                if edge["source"] in infected and edge["target"] not in infected:
                    # 전염 확률 = exposure * risk
                    contagion_prob = edge["exposure"] * edge["risk"]
                    if random.random() < contagion_prob:
                        new_infected.add(edge["target"])
                        contagion_path.append({
                            "institution": edge["target"],
                            "stage": stage,
                            "risk": edge["risk"],
                            "source": edge["source"],
                        })
            
            infected.update(new_infected)
            if not new_infected:
                break
        
        return {
            "initial_failure": failing_institution,
            "contagion_path": contagion_path,
            "total_infected": len(infected),
            "infection_rate": float(len(infected) / len(network["nodes"])),
            "timeline": {
                f"Stage {i}": len([x for x in contagion_path if x["stage"] == i])
                for i in range(4)
            },
            "timestamp": datetime.now().isoformat(),
        }
    
    def calculate_systemic_risk(self) -> Dict:
        """
        시스템 리스크 계산
        """
        network = self.generate_network()
        
        # 각 노드의 중요도 (연결도 + 리스크)
        node_importance = {}
        for node in network["nodes"]:
            connections = len([e for e in network["edges"] 
                              if e["source"] == node["id"] or e["target"] == node["id"]])
            importance = connections * node["risk"]
            node_importance[node["id"]] = {
                "connections": connections,
                "risk": node["risk"],
                "importance": float(importance),
            }
        
        # 시스템 리스크 = 전체 네트워크 리스크
        total_risk = sum(n["risk"] for n in network["nodes"])
        systemic_risk = total_risk / len(network["nodes"])
        
        # 상위 위험 기관
        top_risks = sorted(
            node_importance.items(),
            key=lambda x: x[1]["importance"],
            reverse=True
        )[:3]
        
        return {
            "systemic_risk_score": float(systemic_risk),
            "network_density": float(len(network["edges"]) / (len(network["nodes"]) * (len(network["nodes"]) - 1) / 2)),
            "top_risk_nodes": [
                {
                    "institution": name,
                    "importance": data["importance"],
                    "connections": data["connections"],
                    "risk": data["risk"],
                }
                for name, data in top_risks
            ],
            "timestamp": datetime.now().isoformat(),
        }
    
    def _risk_to_color(self, risk: float) -> str:
        """리스크를 색상으로 변환 (0=초록, 1=빨강)"""
        if risk < 0.3:
            return "#10b981"  # 초록
        elif risk < 0.6:
            return "#f59e0b"  # 주황
        else:
            return "#ef4444"  # 빨강


# 싱글톤 인스턴스
_network_engine: NetworkEngine = NetworkEngine()

def get_network_engine() -> NetworkEngine:
    """네트워크 엔진 싱글톤"""
    return _network_engine
