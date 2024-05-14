from sqlmodel import Field, SQLModel


class QuizBase(SQLModel):
    pass


class Quiz(QuizBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class QuizCreate(QuizBase):
    pass


class QuizRead(QuizBase):
    id: int
