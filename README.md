# fast-api

## Getting Started

1. http://www.python.org/downloads 다운로드
2. Install Python
3. Install Python Extension for Visual Studio Code

## About

https://fastapi.tiangolo.com/ko/

## Build

```bash
pip install fastapi
pip install "uvicorn[standard]"
```

## ORM 설치

```bash
pip install sqlalchemy
```

## database.py 추가.

## DB 마이그레이션

> alembic 을 사용

### Installation

https://alembic.sqlalchemy.org/en/latest/front.html#installation

```bash
cd /path/to/your/project
pip install alembic
alembic init alembic
```

여러 템플릿을 사용하려면 ?

```bash
alembic list_templates
```

1. 마이그레이션 스크립트 생성 옵션 설정

`file_template` 의 주석을 제거

2. 마이그레이션 스크립트 생성하기

```bash
alembic revision -m "create account table"

```
