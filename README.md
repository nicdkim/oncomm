# AI 이커머스 경영 경리 프로그램

FastAPI 기반 자동 거래내역 분류/조회 시스템

---

## A. 시스템 아키텍쳐

### 기술 스택 및 선정 이유

- 언어/프레임워크: python=3.12, FastAPI
: 빠른 개발 및 API 설계 가능, pip 활용
- DB: SQLite
: 가볍고 설정이 필요 없어서 적합하다고 판단
- ORM: SQLAlchemy
: DB 추상화가 가능하기에 적용
- ETL/분류: Pandas
: CSV, 데이터 가공 처리
- 서버: Uvicorn

---

### 설치 라이브러리 (requirements.txt)
```txt
fastapi==0.111.0
uvicorn==0.29.0
sqlalchemy==2.0.30
pandas==2.2.2
pydantic==2.7.1
python-multipart==0.0.9
```

설치 방법
=======

