from sqlmodel import Field, SQLModel


class SingleChoiceQuestionBase(SQLModel):
    quizId: int | None = Field(default=None, foreign_key="quiz.id")
    correctOptionId: int | None = Field(
        default=None, foreign_key="single_choice_option.id"
    )
    selectedOptionId: int | None = Field(
        default=None, foreign_key="single_choice_option.id"
    )
    questionText: str | None = Field(default=None)


class SingleChoiceQuestion(SingleChoiceQuestionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class SingleChoiceQuestionCreate(SingleChoiceQuestionBase):
    pass


class SingleChoiceQuestionRead(SingleChoiceQuestionBase):
    id: int
