from sqlmodel import Field, SQLModel


class SingleChoiceQuestionBase(SQLModel):
    quiz_id: int | None = Field(default=None, foreign_key="quiz.id")
    corrent_option_id: int | None = Field(default=None)
    selected_option_id: int | None = Field(default=None)
    text: str | None = Field(default=None)
    index: int


class SingleChoiceQuestion(SingleChoiceQuestionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class SingleChoiceQuestionCreate(SingleChoiceQuestionBase):
    pass


class SingleChoiceQuestionRead(SingleChoiceQuestionBase):
    id: int
