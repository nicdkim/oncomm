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
---

## B. 핵심 자동 분류 로직
rules.json 파일 사용  
거래내역의 적요에 키워드가 포함되면 해당 회사/계정과목에 자동 분류  
어던 규칙과도 일치하지 않으면 미분류로 처리   

예시   
적요: 스타벅스 강남2호점 -> company_id=com_2, category_id=cat_204, category_name=복리후생비  
규칙 불일치시 company_id/category_id 없음, category_name="미분류"

로직 확장 방안
금액 구간: rules.json에 amount_min, amount_max 추가 → 로직에서 조건 분기  
제외 키워드: 각 규칙에 exclude_keywords 필드 → 포함 시 분류 제외  
복합/우선순위: rules.json 규칙 dict 확장, 분기문 추가

## C. 보안 강화 방안
- 민감 정보 저장:  
DB/파일 모두 AES256 등 강력한 암호화 적용  
인증서/비밀번호 등은 환경변수 또는 키관리시스템으로 분리  
- 접근 제어:
JWT로 회사별 접근 권한 분리
- 감사로그
모든 데이터 접근, 다운, 변경 이력 생성
- 네트워크:
HTTPS(SSL) 사용
- DB 권한: 
쿼리 시 항상 company_id 필터 적용

## D. 문제 상황 해결책
시나리오: 한 고객사의 거래 데이터가 다른 고객사 대시보드에 노출됨  
1. 즉시 조치
서비스 일시 중지, 노출 범위 및 피해고객 파악, 관리자/고객 공지  
2. 원인분석  
API/ORM 쿼리에서 company_id 필터링 누락/오류 확인  
로그/DB 이력, 배포/코드 변경내역 점검  
3. 재발방지  
회사별 쿼리/테스트케이스 의무화, 권한분리 로직 추가  
배포 전 자동화테스트, 정기 보안 점검  

## 실행 및 테스트
1) 패키지 설치  
pip install -r requirements.txt   
2) DB 초기화  
python init_db.py  
3) 서버 실행  
uvicorn app.mainLapp --reload  
4) API 테스트 (swagger)  
http://127.0.0.1:8000/docs 접속  
POST /api/v1/accounting/process  
: bank_transactions.csv + rules.json 파일 업로드  
GET /api/v1/accounting/records?companyId=com_1  
: companyId에 rules.json에 등록된 값 입력(com_1, com_2 등)  
거래내역 분류 결과 리스트 확인

AI을 활용한 점
- AI 활용 방식  
: SQLAlchemy 활용 예지 및 마크다운 포맷 작성을 AI의 답변을 참고 하였습니다.  
- AI가 제안한 결과물과 실제 수정/결정한 부분  
: DB 한글 컬럼명에서 AI는 처음에 테이블 컬럼명을 영문으로 제안 했으나, 실제 CSV의 맞게 한글로 수정 하였습니다.  
- README 문서 작성  
: AI가 마크다운 구조, 큰 제목, 코드 블록을 일관되게 내주지 않아, 실제 결과물은 직접 포맷/구조/줄바꿈을 조정하여 제출물에 맞게 맞췄습니다.  
- 감사 로그는 실제 구현 경험은 없으며, 경험과 실무 사례를 바탕으로 이상적으로 작성 하였습니다.