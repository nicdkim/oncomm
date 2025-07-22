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
```txt
pip install -r requirements.txt
```

DB 스키마 및 구조
여러 사업체와 계정 과목, 거래내역을 저장
회사별 계정과목/분류 결과를 관계형 구조로 표현

ERD 요약
회사(Company)
계정과목(Category, 회사별 소속)
거래내역(Transaction, 회사/카테고리별 귀속 + 원본 데이터)

SQL 테이블
```txt
CREATE TABLE companies (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE categories (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  company_id TEXT NOT NULL,
  FOREIGN KEY(company_id) REFERENCES companies(id)
);

CREATE TABLE transactions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  거래일시 TEXT NOT NULL,
  적요 TEXT NOT NULL,
  입금액 REAL,
  출금액 REAL,
  금액 REAL,
  company_id TEXT,
  category_id TEXT,
  category_name TEXT,
  raw_data TEXT,
  classified BOOLEAN,
  FOREIGN KEY(company_id) REFERENCES companies(id),
  FOREIGN KEY(category_id) REFERENCES categories(id)
);
CREATE TABLE companies (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE categories (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  company_id TEXT NOT NULL,
  FOREIGN KEY(company_id) REFERENCES companies(id)
);

CREATE TABLE transactions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  거래일시 TEXT NOT NULL,
  적요 TEXT NOT NULL,
  입금액 REAL,
  출금액 REAL,
  금액 REAL,
  company_id TEXT,
  category_id TEXT,
  category_name TEXT,
  raw_data TEXT,
  classified BOOLEAN,
  FOREIGN KEY(company_id) REFERENCES companies(id),
  FOREIGN KEY(category_id) REFERENCES categories(id)
);
```