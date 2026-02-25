# 🚀 SimVentures API

**SimShield + AlphaRisk + PowerGraph 통합 백엔드**

통화정책 → 실물경제 영향을 시뮬레이션하는 AI 기반 경제 분석 엔진

---

## 📊 제품 (3개)

### 1. 🛡️ **SimShield** - 개인 재정 방어 시뮬레이터
- M2 (통화량) → 자산가격 → 구매력 침식 분석
- FRED API 기반 실시간 경제 데이터
- 12개월 정책 시나리오 (Baseline, Dovish, Hawkish)

### 2. 📊 **AlphaRisk** - 기관 회의주의자 블룸버그 터미널
- 리스크 프리미엄 분석
- 포트폴리오 최적화 (Quant)
- 실시간 시장 신호

### 3. 🕸️ **PowerGraph** - 네트워크 인텔리전스
- 금융 네트워크 전염 분석
- B2B 인프라 평가
- 리스크 전파 감지

---

## 🛠️ 기술 스택

- **Framework**: FastAPI 0.133.0
- **Server**: Uvicorn 0.41.0
- **Data**: Pandas, NumPy, DuckDB
- **API**: FRED (Federal Reserve Economic Data)
- **Language**: Python 3.14 (M4 Max native)

---

## 📦 설치

### 요구사항
- Python 3.10+
- venv

### 설치 단계

```bash
# 저장소 클론
cd simulation-ventures-api

# 가상환경 생성
python3 -m venv venv
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일에서 FRED_API_KEY 추가 (옵션)
```

---

## 🚀 실행

### 개발 환경 (자동 리로드)
```bash
source venv/bin/activate
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 프로덕션 환경
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### API 문서
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 📡 API 엔드포인트

### 헬스 체크
```
GET /health
GET /api/simshield/health
```

### SimShield - 경제 데이터
```
GET /api/simshield/data?start_date=2010-01-01
```

### SimShield - 시나리오 분석
```
GET /api/simshield/scenarios?m2=21500&cpi=308.417
```

응답:
```json
{
  "scenarios": {
    "baseline": {
      "12month_m2_change": 3.66,
      "12month_pp_loss": 2.37
    },
    "dovish": {
      "12month_m2_change": 6.17,
      "12month_pp_loss": 3.53
    },
    "hawkish": {
      "12month_m2_change": 1.21,
      "12month_pp_loss": 1.19
    }
  }
}
```

### SimShield - 구매력 변화
```
GET /api/simshield/purchasing-power?years=5
```

---

## 📚 주요 모듈

### `app/services/fred_client.py`
FRED API 클라이언트 - M2, CPI 등 경제 지표 조회

### `app/services/simulation_engine.py`
통화정책 → 실물경제 시뮬레이션 엔진

### `app/routes/simshield.py`
SimShield 제품 API 엔드포인트

---

## 🔧 설정

### 환경 변수 (`.env`)
```
DEBUG=True
LOG_LEVEL=DEBUG
FRED_API_KEY=your_api_key_here
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=development
```

**FRED API 키 획득**:
1. https://fred.stlouisfed.org/api/fred/series/data 에서 가입
2. 개인 API 키 생성
3. `.env` 파일에 추가

---

## 📈 성능

### 목표 (Year 1)
- **5월**: $13.8K MRR (SimShield MVP)
- **6월**: $40K+ MRR (3개 제품 병렬)
- **Year 1**: $200K-500K ARR

### 시스템 요구사항
- MacBook Pro 16" (M4 Max, 128GB RAM)
- 로컬 개발: 1초 이내 응답
- 프로덕션: Vercel (Frontend) + Railway/Render (Backend)

---

## 🧪 테스트

```bash
# 모든 엔드포인트 테스트
source venv/bin/activate
python test_api.py
```

결과 예시:
```
✅ 1️⃣ 헬스 체크: 200 OK
✅ 2️⃣ API 정보: 200 OK
✅ 3️⃣ SimShield 헬스: 200 OK
✅ 4️⃣ 경제 데이터: 200 OK
✅ 5️⃣ 시나리오 분석: 200 OK
```

---

## 📝 라이선스

Private / Not yet published

---

## 👨‍💻 개발자

**Andrew Antru**
- Control Systems PhD
- Quant Trading Background
- Gov Procurement Experience

---

## 🗺️ 로드맵

| 주차 | 목표 | 상태 |
|------|------|------|
| Week 1-2 | SimShield MVP | 🟢 진행중 |
| Week 3-4 | AlphaRisk 초기화 | 🔵 예정 |
| Week 5-8 | PowerGraph MVP | 🔵 예정 |
| Week 9-12 | 배포 + 마케팅 | 🔵 예정 |

---

**Created**: 2026-02-25  
**Last Updated**: 2026-02-25
