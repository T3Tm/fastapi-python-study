from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship, func, Column, AutoString
from pydantic import EmailStr
from sqlalchemy import UniqueConstraint
from pydantic import AwareDatetime
from sqlalchemy_utc import UtcDateTime

class User(SQLModel, table=True):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("email", name="uq_email"),
    )
    #lazy evaluation (지연 평가)
    #OAuthAccount 객체가 User보다 하위에 존재하기 때문
    oauth_accounts: list["OAuthAccount"] = Relationship(back_populates="user")

    id: int = Field(default=None, primary_key=True)
    username: str = Field(unique=True, max_length=40, description="사용자 계정 ID")
    email: EmailStr = Field(max_length=128, description="사용자 이메일")
    display_name: str = Field(max_length=40, description="사용자 표시 이름")
    password: str = Field(unique=True, max_length=128, description="사용자 비밀번호")
    is_host: bool = Field(default=False, description="사용자 호스트 여부")

    created_at: AwareDatetime = Field(
        default = None,
        nullable=False,
        sa_type=UtcDateTime,
        sa_column_kwargs={
            "server_default" : func.now(),
        },
    )
    updated_at: AwareDatetime = Field(
        default = None,
        nullable=False,
        sa_type=UtcDateTime,
        sa_column_kwargs={
            "server_default" : func.now(),
            "onupdate": lambda: datetime.now(timezone.utc)
        },
    )

class OAuthAccount(SQLModel, table=True):
    __tablename__ = "oauth_accounts"
    __table_args__ = (
        UniqueConstraint(
            "provider",
            "provider_account_id",
            name="uq_provider_provider_account_id",
        ),
    )
    id: int = Field(default=None, primary_key=True)
    
    provider: str = Field(max_length=10, description="OAuth 제공자")
    provider_account_id: str = Field(max_length=128, description="OAuth 제공자 계정 ID")

    user_id: int = Field(foreign_key="users.id")
    user: User = Relationship(back_populates="oauth_accounts")

    created_at: AwareDatetime = Field(
        default=None,
        nullable=False,
        sa_type=UtcDateTime,
        sa_column_kwargs={
            "server_default": func.now(),
        },
    )
    updated_at: AwareDatetime = Field(
        default=None,
        nullable=False,
        sa_type=UtcDateTime,
        sa_column_kwargs={
            "server_default": func.now(),
            "onupdate": lambda: datetime.now(timezone.utc),
        },
    )