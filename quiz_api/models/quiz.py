from sqlmodel import Field, SQLModel


class QuizBase(SQLModel):
    name: str | None = Field(default=None)
    isDraft: bool = Field(default=True)


class Quiz(QuizBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class QuizCreate(QuizBase):
    pass


class QuizRead(QuizBase):
    id: int
