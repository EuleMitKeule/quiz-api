from sqlmodel import Field, SQLModel


class MultipleChoiceOptionBase(SQLModel):
    question_id: int | None = Field(default=None)
    correct_question_id: int | None = Field(default=None)
    selected_question_id: int | None = Field(default=None)
    text: str | None = Field(default=None)


class MultipleChoiceOption(MultipleChoiceOptionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class MultipleChoiceOptionCreate(MultipleChoiceOptionBase):
    pass


class MultipleChoiceOptionRead(MultipleChoiceOptionBase):
    id: int
