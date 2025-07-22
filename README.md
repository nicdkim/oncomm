# AI 이커머스 경영 경리 프로그램

FastAPI 기반 자동 거래내역 분류/조회 시스템 (실무테스트 과제)

---

## A. 시스템 아키텍처

### ◾ 기술 스택 및 선정 이유

- **언어/프레임워크:** Python 3.12, FastAPI  
  → 개발 생산성과 빠른 API 설계, Python 생태계 활용  
- **DB:** SQLite  
  → 가볍고 설정이 필요 없어 과제/테스트에 최적  
- **ORM:** SQLAlchemy  
  → 유지보수성과 DB 추상화  
- **ETL/분류:** Pandas  
  → 대용량 CSV, 데이터 가공 처리  
- **서버:** Uvicorn (ASGI)

### ◾ 설치 라이브러리 (`requirements.txt`)
```txt
fastapi==0.111.0
uvicorn==0.29.0
sqlalchemy==2.0.30
pandas==2.2.2
pydantic==2.7.1
python-multipart==0.0.9

설치 방법:
pip install -r requirements.txt
◾ DB 스키마 및 구조
여러 사업체(회사)와 계정과목, 거래내역을 유연하게 저장

회사별 계정과목/분류 결과를 관계형 구조로 표현

ERD 요약

회사(Company)

계정과목(Category, 회사별 소속)

거래내역(Transaction, 회사/카테고리별 귀속 + 원본데이터)

SQL 테이블

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

## B. 핵심 자동 분류 로직
rules.json 파일에 회사/카테고리/키워드 기반 규칙을 정의

거래내역의 "적요"에 키워드가 포함되면 해당 회사/계정과목에 자동 분류

어떤 규칙과도 일치하지 않으면 "미분류" 처리

예시

적요: 스타벅스 강남2호점 → company_id=com_2, category_id=cat_204, category_name=복리후생비

규칙 미일치 시 company_id/category_id 없음, category_name="미분류"

로직 확장 방안

금액 구간: rules.json에 amount_min, amount_max 추가 → 로직에서 조건 분기

제외 키워드: 각 규칙에 exclude_keywords 필드 → 포함 시 분류 제외

복합/우선순위: rules.json 규칙 dict 확장, 분기문 추가

## C. 보안 강화 방안
민감 정보 저장

DB/파일 모두 AES256 등 강력한 암호화 적용

인증서/비밀번호 등은 환경변수 또는 키관리시스템(KMS)로 분리

접근 제어

사용자 인증(JWT 등), 회사별 접근 권한 분리

감사 로그

모든 데이터 접근/다운로드/변경 이력 남김

네트워크

무조건 HTTPS(SSL) 사용, 백업도 암호화

DB 권한

쿼리 시 항상 company_id 필터 필수 적용

## D. 문제상황 해결책
시나리오: 한 고객사의 거래 데이터가 다른 고객사 대시보드에 노출됨

즉시조치

서비스 일시 중지, 노출 범위 및 피해고객 파악, 관리자/고객 공지

원인분석

API/ORM 쿼리에서 company_id 필터링 누락/오류 확인

로그/DB 이력, 배포/코드 변경내역 점검

재발방지

회사별 쿼리/테스트케이스 의무화, 권한분리 로직 추가

배포 전 자동화테스트, 정기 보안 점검

실행 및 테스트 가이드
1) 패키지 설치
pip install -r requirements.txt
2) DB 초기화
python init_db.py
3) 서버 실행
uvicorn app.main:app --reload
4) API 테스트 (Swagger UI)
http://127.0.0.1:8000/docs 접속

POST /api/v1/accounting/process
: bank_transactions.csv + rules.json 파일 업로드

GET /api/v1/accounting/records?companyId=com_1
: companyId에 rules.json에 등록된 값 입력(com_1, com_2 등)

5) 예시 cURL
curl -X GET "http://127.0.0.1:8000/api/v1/accounting/records?companyId=com_1" -H "accept: applicatio
