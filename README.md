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

## Run

```bash
uvicorn app.main:app --reload
```

## ORM 설치

> TIP
>
> SQL database CRUD 예제를 참고합니다.

```bash
pip install sqlalchemy
```

[How to SQL databases?](https://fastapi.tiangolo.com/ko/tutorial/sql-databases)

## DB 마이그레이션

> TIP
>
> alembic 을 사용하여 데이터베이스 스키마를 관리합니다.

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
   `alembic.ini`의 내용을 수정합니다.

`file_template` 의 주석을 제거
`output_encoding = utf-8` 의 주석을 제거
`sqlalchemy.url = sqlite:///./sql_app.db` 커넥션 설정

```bash
Valid SQLite URL forms are:
 sqlite:///:memory: (or, sqlite://)
 sqlite:///relative/path/to/file.db
 sqlite:////absolute/path/to/file.db
```

2. 마이그레이션 스크립트 생성하기

```bash
alembic revision -m "create account table"

```

3. 생성된 파일에 스크립트를 작성

```python

def upgrade() -> None:
    op.create_table(
        'account',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Unicode(200)),
    )


def downgrade() -> None:
    op.drop_table('account')

```

4. 첫번째 마이그레이션 실행하기

```bash
alembic upgrade head
```

5. 컬럼 추가하기

```bash
alembic revision -m "Add a column"
```

```python
def upgrade() -> None:
    op.add_column('account', sa.Column('insert_at', sa.DateTime))


def downgrade() -> None:
    op.drop_column('account', 'insert_at')
```

```bash
alembic upgrade +1
```

6. Log 확인하기
   현재 개정을 확인

```bash
alembic current
```

마이그레이션 이력 보기

```bash
alembic history --verbose
```

마이그레이션 이력 범위 지정해서 보기

```bash
#-r[start]:[end]
alembic history -r-3:current
```

> TIP
>
> 만약, 불필요한 마이그레이션 파일이 있다면 삭제하고
> script 파일 내부에 `Revises` 항목과 `down_revision` 항목을 직접 수정하면 된다.

```python
"""create users table

Revision ID: d3f816667971
Revises: fdb8b7947edb
Create Date: 2022-10-02 19:40:44.482390

"""
from email.policy import default
from enum import unique
from operator import index
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3f816667971'
down_revision = 'fdb8b7947edb'

```

> TIP
>
> Default 설정하기

```python
# Boolean
op.add_column('users', sa.Column('is_active', sa.Boolean(), server_default=sa.schema.DefaultClause("0"), nullable=False))

# DateTime
op.add_column('users', sa.Column('insert_at', sa.DateTime(), server_default=sa.func.current_timestamp(), nullable=False))
```

### 암호화(Crypto) 사용

```bash
pip install bcrypt
```

### db mysql 사용

```bash
pip install pymysql
```

### poetry 사용법

> requirements.txt 대신 사용이 가능한 dependency management

[poetry](https://python-poetry.org/docs)

## 파일 업로드

```bash
pip install python-multipart
```

## Security

https://fastapi.tiangolo.com/tutorial/security/first-steps/

### jwt

```bash
pip install "python-jose[cryptography]"
pip install "passlib[bcrypt]"
```
