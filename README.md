# AI 이커머스 경영 경리 프로그램

FastAPI 기반 자동 거래내역 분류/조회 시스템 (실무테스트 과제)

---

## A. 시스템 아키텍처

### 기술 스택 및 선정 이유

- **언어/프레임워크:** Python 3.12, FastAPI  
  → 개발 생산성과 빠른 API 설계, Python 생태계 활용  
- **DB:** SQLite  
  → 가볍고 설정이 필요 없어 과제/테스트에 최적  
- **ORM:** SQLAlchemy  
  → 유지보수성과 DB 추상화  
- **ETL/분류:** Pandas  
  → 대용량 CSV, 데이터 가공 처리  
- **서버:** Uvicorn (ASGI)

---

### 설치 라이브러리 (`requirements.txt`)

```txt
fastapi==0.111.0
uvicorn==0.29.0
sqlalchemy==2.0.30
pandas==2.2.2
pydantic==2.7.1
python-multipart==0.0.9

### 설치 방법
```txt
pip install -r requirements.txt
