from sqlmodel import Field, SQLModel


class SingleChoiceOptionBase(SQLModel):
    questionId: int | None = Field(
        default=None, foreign_key="single_choice_question.id"
    )
    optionText: str | None = Field(default=None)


class SingleChoiceOption(SingleChoiceOptionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class SingleChoiceOptionCreate(SingleChoiceOptionBase):
    pass


class SingleChoiceOptionRead(SingleChoiceOptionBase):
    id: int
