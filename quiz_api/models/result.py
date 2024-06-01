from sqlmodel import Field, SQLModel


class ResultBase(SQLModel):
    quiz_id: int | None = Field(default=None)
    score: int | None = Field(default=None)
    total: int | None = Field(default=None)


class Result(ResultBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None)


class ResultCreate(ResultBase):
    pass


class ResultRead(ResultBase):
    id: int
    user_id: int | None
