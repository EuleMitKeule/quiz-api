from sqlmodel import Field, SQLModel


class MultipleChoiceQuestionBase(SQLModel):
    quiz_id: int | None = Field(default=None, foreign_key="quiz.id")
    text: str | None = Field(default=None)


class MultipleChoiceQuestion(MultipleChoiceQuestionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class MultipleChoiceQuestionCreate(MultipleChoiceQuestionBase):
    pass


class MultipleChoiceQuestionRead(MultipleChoiceQuestionBase):
    id: int
