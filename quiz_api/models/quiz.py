from sqlmodel import Field, SQLModel


class QuizBase(SQLModel):
    title: str | None = Field(default=None)
    is_draft: bool = Field(default=True)


class Quiz(QuizBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class QuizCreate(QuizBase):
    pass


class QuizRead(QuizBase):
    id: int
