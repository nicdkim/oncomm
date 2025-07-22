# AI 이커머스 경영 경리 프로그램

FastAPI 기반 자동 거래내역 분류/조회 시스템 (실무테스트 과제)

---

## 1. 시스템 아키텍처

### ◾ 기술 스택

- **언어/프레임워크:** Python 3.12, FastAPI
- **DB:** SQLite (개발/테스트 환경에서 빠르고 간단하게 사용)
- **ORM:** SQLAlchemy
- **ETL/분류:** Pandas
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

bash
복사
편집
pip install -r requirements.txt
2. DB 스키마
[ERD 구조 요약]
회사(Company)

계정과목(Category, 회사별 소속)

거래내역(Transaction, 회사/카테고리별 귀속 + 원본데이터)

[CREATE TABLE 구문]
sql
복사
편집
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
컬럼명은 실제 CSV 포맷(한글 컬럼)과 일치하도록 구현함

3. 핵심 자동 분류 로직
rules.json 파일에 회사별/카테고리별 키워드 규칙이 정의됨

거래내역의 적요(설명)에 키워드가 포함된 경우 해당 회사/계정과목으로 귀속

일치하는 규칙이 없으면 "미분류" 처리

[예시]
적요: "스타벅스 강남2호점" → company_id=com_2, category_id=cat_204, category_name=복리후생비

규칙 미일치 시 company_id/category_id 없음, category_name="미분류"

[로직 확장 예시]
금액 구간:

rules.json에서 금액범위(amount_min, amount_max) 조건을 추가할 수 있음

제외 키워드:

규칙별로 exclude_keywords 설정 후, 해당 키워드가 있으면 분류 제외

우선순위/복합조건:

규칙 dict구조 확장 및 분기 추가로 쉽게 대응 가능

4. 보안 설계
민감 정보 저장:

반드시 암호화 파일 저장(ex. AES256),
비밀번호/키 등은 환경변수 또는 외부 키관리(KMS)로 분리 관리

접근 제어:

인증/인가 및 회사별 접근 제한 필수 (예: JWT, OAuth2 적용)

감사 로그:

모든 데이터 접근/변경/다운로드 이력 기록

네트워크:

무조건 HTTPS(SSL), 백업도 암호화 저장

DB 권한:

회사별 데이터 쿼리에서 항상 company_id 조건 필수 적용

5. 문제 상황 대응책
즉시조치:

서비스 중단, 노출 범위 파악/안내, 서버 및 감사 로그 확인

원인분석:

API/ORM 코드에서 company_id 필터/권한 미적용 등 점검

DB 로그/쿼리 감사, 배포 이력 체크

재발방지:

쿼리/API 테스트에 회사별 필터 케이스 추가

권한 분리/테스트 자동화, 정기 보안점검

6. 실행 및 테스트 가이드
◾ 1) 패키지 설치
bash
복사
편집
pip install -r requirements.txt
◾ 2) DB 초기화
bash
복사
편집
python init_db.py
◾ 3) 서버 실행
bash
복사
편집
uvicorn app.main:app --reload
◾ 4) API 테스트 (Swagger UI)
http://127.0.0.1:8000/docs 접속

▶ POST /api/v1/accounting/process
bank_transactions.csv + rules.json 파일 업로드

▶ GET /api/v1/accounting/records?companyId=com_1
companyId: rules.json에 지정된 값 입력(com_1, com_2 등)

거래내역 분류 결과 리스트 확인

◾ 5) 예시 cURL
curl -X GET "http://127.0.0.1:8000/api/v1/accounting/records?companyId=com_1" -H "accept: application/json"

