#!/usr/bin/env python3
"""
SimVentures API 테스트 스크립트
"""

import asyncio
import httpx
import json
from datetime import datetime

async def test_api():
    """API 엔드포인트 테스트"""
    
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        print("🚀 SimVentures API 테스트 시작\n")
        print("=" * 60)
        
        # 1. 헬스 체크
        print("\n1️⃣ 헬스 체크 (/health)")
        try:
            response = await client.get(f"{base_url}/health")
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except Exception as e:
            print(f"❌ 오류: {e}")
        
        # 2. Root 엔드포인트
        print("\n2️⃣ API 정보 (/)")
        try:
            response = await client.get(f"{base_url}/")
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except Exception as e:
            print(f"❌ 오류: {e}")
        
        # 3. SimShield 헬스 체크
        print("\n3️⃣ SimShield 헬스 체크 (/api/simshield/health)")
        try:
            response = await client.get(f"{base_url}/api/simshield/health")
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except Exception as e:
            print(f"❌ 오류: {e}")
        
        # 4. 경제 데이터 조회
        print("\n4️⃣ 경제 데이터 조회 (/api/simshield/data)")
        print("   (FRED API 호출 - demo key로 제한됨)")
        try:
            response = await client.get(
                f"{base_url}/api/simshield/data",
                params={"start_date": "2020-01-01"}
            )
            print(f"Status: {response.status_code}")
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)[:500]}...")  # 처음 500글자만
        except Exception as e:
            print(f"❌ 오류: {e}")
        
        # 5. 시나리오 분석
        print("\n5️⃣ 정책 시나리오 분석 (/api/simshield/scenarios)")
        try:
            response = await client.get(f"{base_url}/api/simshield/scenarios")
            print(f"Status: {response.status_code}")
            data = response.json()
            if "analysis" in data:
                print(f"시나리오: {list(data['analysis']['scenarios'].keys())}")
                for scenario, result in data['analysis']['scenarios'].items():
                    print(f"\n  📊 {scenario}:")
                    print(f"     12개월 M2 변화: {result.get('12month_m2_change', 0):.2f}%")
                    print(f"     구매력 손실: {result.get('12month_pp_loss', 0):.2f}%")
        except Exception as e:
            print(f"❌ 오류: {e}")
        
        # 6. 구매력 변화
        print("\n6️⃣ 구매력 변화 (/api/simshield/purchasing-power)")
        try:
            response = await client.get(
                f"{base_url}/api/simshield/purchasing-power",
                params={"years": 5}
            )
            print(f"Status: {response.status_code}")
            data = response.json()
            if "data" in data:
                print(f"조회된 데이터: {len(data['data'])} 개월")
                if data['data']:
                    print(f"최근: {data['data'][-1]}")
        except Exception as e:
            print(f"❌ 오류: {e}")
        
        print("\n" + "=" * 60)
        print("✅ 테스트 완료!")

if __name__ == "__main__":
    asyncio.run(test_api())
