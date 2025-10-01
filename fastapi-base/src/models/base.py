from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, Column, BigInteger, Boolean, Text, String
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy import DateTime

# utcnow() and BaseModel adjusted for int PKs (bigint)

class utcnow(expression.FunctionElement):  # type: ignore
    type = DateTime()
    inherit_cache = True

@compiles(utcnow, "postgresql")
def pg_utcnow(element, compiler, **kw) -> str:  # type: ignore
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"

class BaseModel(SQLModel):
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        index=True,
    )
    # created_at: Optional[datetime] = Field(
    #     sa_column=Column(
    #         DateTime(timezone=True),
    #         server_default=utcnow(),
    #         nullable=True,
    #     ),
    # )
    # updated_at: Optional[datetime] = Field(
    #     sa_column=Column(
    #         DateTime(timezone=True),
    #         onupdate=utcnow(),
    #         nullable=True,
    #     ),
    # )