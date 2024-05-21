from sqlmodel import Field, SQLModel


class SingleChoiceOptionBase(SQLModel):
    question_id: int | None = Field(
        default=None, foreign_key="single_choice_question.id"
    )
    text: str | None = Field(default=None)


class SingleChoiceOption(SingleChoiceOptionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class SingleChoiceOptionCreate(SingleChoiceOptionBase):
    pass


class SingleChoiceOptionRead(SingleChoiceOptionBase):
    id: int
