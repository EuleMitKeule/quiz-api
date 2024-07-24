from datetime import datetime, timezone
from typing import List

from pydantic import BaseModel
from sqlalchemy import JSON, Column
from sqlmodel import Field, Relationship, SQLModel

from quiz_api.const import QuestionDifficulty


class HasTitle(SQLModel):
    title: str


class HasText(SQLModel):
    text: str


class HasIndex(SQLModel):
    index: int


class QuizBase(HasTitle):
    is_practice: bool = Field(default=False)


class ResultBase(SQLModel):
    quiz_id: int | None = Field(default=None, foreign_key="quiz.id")
    user_id: int | None = Field(default=None, foreign_key="user.id")
    score: int = Field(default=0)
    max_score: int = Field(default=0)


class QuestionBase(HasTitle, HasText, HasIndex):
    quiz_id: int | None = Field(default=None, foreign_key="quiz.id")
    difficulty: QuestionDifficulty = Field(default=QuestionDifficulty.EASY)


class AnswerBase(SQLModel):
    result_id: int | None = Field(default=None, foreign_key="result.id")


class SingleChoiceQuestionBase(QuestionBase):
    correct_index: int


class MultipleChoiceQuestionBase(QuestionBase):
    correct_indices: List[int]


class OpenQuestionBase(QuestionBase):
    pass


class AssignmentQuestionBase(QuestionBase):
    correct_indices: List[int]


class GapTextQuestionBase(QuestionBase):
    correct_indices: List[int]


class GapTextSubQuestionBase(HasIndex):
    question_id: int | None = Field(default=None, foreign_key="gap_text_question.id")


class SingleChoiceOptionBase(HasText, HasIndex):
    question_id: int | None = Field(
        default=None, foreign_key="single_choice_question.id"
    )


class MultipleChoiceOptionBase(HasText, HasIndex):
    question_id: int | None = Field(
        default=None, foreign_key="multiple_choice_question.id"
    )


class OpenOptionBase(HasText, HasIndex):
    question_id: int | None = Field(default=None, foreign_key="open_question.id")


class AssignmentOptionBase(HasText, HasIndex):
    question_id: int | None = Field(default=None, foreign_key="assignment_question.id")
    correct_index: int


class GapTextOptionBase(HasText, HasIndex):
    sub_question_id: int | None = Field(
        default=None, foreign_key="gap_text_sub_question.id"
    )


class SingleChoiceAnswerBase(AnswerBase):
    question_id: int | None = Field(
        default=None, foreign_key="single_choice_question.id"
    )
    selected_index: int


class MultipleChoiceAnswerBase(AnswerBase):
    question_id: int | None = Field(
        default=None, foreign_key="multiple_choice_question.id"
    )
    selected_indices: List[int]


class OpenAnswerBase(AnswerBase):
    question_id: int | None = Field(default=None, foreign_key="open_question.id")
    text: str


class AssignmentAnswerBase(AnswerBase):
    question_id: int | None = Field(default=None, foreign_key="assignment_question.id")
    selected_indices: List[int] = Field(sa_column=Column(JSON))


class GapTextAnswerBase(AnswerBase):
    question_id: int | None = Field(default=None, foreign_key="gap_text_question.id")
    selected_indices: List[int] = Field(sa_column=Column(JSON))


class UserBase(SQLModel):
    username: str = Field(index=True, nullable=False)
    is_admin: bool


class LabelBase(SQLModel):
    text: str = Field(index=True, unique=True)


class QuizLabelRelation(SQLModel, table=True):
    __tablename__ = "quiz_label_relation"

    quiz_id: int | None = Field(default=None, foreign_key="quiz.id", primary_key=True)
    label_id: int | None = Field(default=None, foreign_key="label.id", primary_key=True)


class Quiz(QuizBase, table=True):
    __tablename__ = "quiz"

    id: int | None = Field(default=None, primary_key=True)
    single_choice_questions: List["SingleChoiceQuestion"] = Relationship(
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    multiple_choice_questions: List["MultipleChoiceQuestion"] = Relationship(
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    open_questions: List["OpenQuestion"] = Relationship(
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    assignment_questions: List["AssignmentQuestion"] = Relationship(
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    gap_text_questions: List["GapTextQuestion"] = Relationship(
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    labels: List["Label"] = Relationship(
        back_populates="quizzes",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=QuizLabelRelation,
    )


class Result(ResultBase, table=True):
    __tablename__ = "result"

    id: int | None = Field(default=None, primary_key=True)
    user: "User" = Relationship(sa_relationship_kwargs={"lazy": "selectin"})
    single_choice_answers: List["SingleChoiceAnswer"] = Relationship(
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    multiple_choice_answers: List["MultipleChoiceAnswer"] = Relationship(
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    open_answers: List["OpenAnswer"] = Relationship(
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    assignment_answers: List["AssignmentAnswer"] = Relationship(
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    gap_text_answers: List["GapTextAnswer"] = Relationship(
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    created_at: datetime = Field(default=datetime.now(timezone.utc))


class SingleChoiceQuestion(SingleChoiceQuestionBase, table=True):
    __tablename__ = "single_choice_question"

    id: int | None = Field(default=None, primary_key=True)
    single_choice_options: List["SingleChoiceOption"] = Relationship(
        sa_relationship_kwargs={"lazy": "selectin"}
    )


class MultipleChoiceQuestion(MultipleChoiceQuestionBase, table=True):
    __tablename__ = "multiple_choice_question"

    id: int | None = Field(default=None, primary_key=True)
    multiple_choice_options: List["MultipleChoiceOption"] = Relationship(
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    correct_indices: List[int] = Field(sa_column=Column(JSON))


class OpenQuestion(OpenQuestionBase, table=True):
    __tablename__ = "open_question"

    id: int | None = Field(default=None, primary_key=True)
    open_options: List["OpenOption"] = Relationship(
        sa_relationship_kwargs={"lazy": "selectin"}
    )


class AssignmentQuestion(AssignmentQuestionBase, table=True):
    __tablename__ = "assignment_question"

    id: int | None = Field(default=None, primary_key=True)
    assignment_options: List["AssignmentOption"] = Relationship(
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    correct_indices: List[int] = Field(sa_column=Column(JSON))


class GapTextQuestion(GapTextQuestionBase, table=True):
    __tablename__ = "gap_text_question"

    id: int | None = Field(default=None, primary_key=True)
    gap_text_sub_questions: List["GapTextSubQuestion"] = Relationship(
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    correct_indices: List[int] = Field(sa_column=Column(JSON))


class GapTextSubQuestion(GapTextSubQuestionBase, table=True):
    __tablename__ = "gap_text_sub_question"

    id: int | None = Field(default=None, primary_key=True)
    gap_text_options: List["GapTextOption"] = Relationship(
        sa_relationship_kwargs={"lazy": "selectin"}
    )


class SingleChoiceOption(SingleChoiceOptionBase, table=True):
    __tablename__ = "single_choice_option"

    id: int | None = Field(default=None, primary_key=True)


class MultipleChoiceOption(MultipleChoiceOptionBase, table=True):
    __tablename__ = "multiple_choice_option"

    id: int | None = Field(default=None, primary_key=True)


class OpenOption(OpenOptionBase, table=True):
    __tablename__ = "open_option"

    id: int | None = Field(default=None, primary_key=True)


class AssignmentOption(AssignmentOptionBase, table=True):
    __tablename__ = "assignment_option"

    id: int | None = Field(default=None, primary_key=True)


class GapTextOption(GapTextOptionBase, table=True):
    __tablename__ = "gap_text_option"

    id: int | None = Field(default=None, primary_key=True)


class Answer(AnswerBase):
    id: int | None = Field(default=None, primary_key=True)
    score: int = Field(default=0)
    max_score: int = Field(default=1)


class SingleChoiceAnswer(Answer, SingleChoiceAnswerBase, table=True):
    __tablename__ = "single_choice_answer"

    question: "SingleChoiceQuestion" = Relationship(
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    result: "Result" = Relationship(
        back_populates="single_choice_answers",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class MultipleChoiceAnswer(Answer, MultipleChoiceAnswerBase, table=True):
    __tablename__ = "multiple_choice_answer"

    selected_indices: List[int] = Field(sa_column=Column(JSON))
    result: "Result" = Relationship(
        back_populates="multiple_choice_answers",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class OpenAnswer(Answer, OpenAnswerBase, table=True):
    __tablename__ = "open_answer"

    result: "Result" = Relationship(
        back_populates="open_answers",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class AssignmentAnswer(Answer, AssignmentAnswerBase, table=True):
    __tablename__ = "assignment_answer"

    selected_indices: List[int] = Field(sa_column=Column(JSON))
    result: "Result" = Relationship(
        back_populates="assignment_answers",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class GapTextAnswer(Answer, GapTextAnswerBase, table=True):
    __tablename__ = "gap_text_answer"

    selected_indices: List[int] = Field(sa_column=Column(JSON))
    result: "Result" = Relationship(
        back_populates="gap_text_answers",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class User(UserBase, table=True):
    __tablename__ = "user"

    id: int = Field(default=None, primary_key=True)
    hashed_password: str


class Label(LabelBase, table=True):
    __tablename__ = "label"

    id: int = Field(default=None, primary_key=True)
    quizzes: List["Quiz"] = Relationship(
        back_populates="labels",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=QuizLabelRelation,
    )

    @property
    def quiz_ids(self) -> List[int]:
        return [quiz.id for quiz in self.quizzes]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
    is_admin: bool


class QuizCreate(QuizBase):
    pass


class ResultCreate(ResultBase):
    pass


class SingleChoiceQuestionCreate(SingleChoiceQuestionBase):
    pass


class MultipleChoiceQuestionCreate(MultipleChoiceQuestionBase):
    pass


class OpenQuestionCreate(OpenQuestionBase):
    pass


class AssignmentQuestionCreate(AssignmentQuestionBase):
    pass


class GapTextQuestionCreate(GapTextQuestionBase):
    pass


class GapTextSubQuestionCreate(GapTextSubQuestionBase):
    pass


class SingleChoiceOptionCreate(SingleChoiceOptionBase):
    pass


class MultipleChoiceOptionCreate(MultipleChoiceOptionBase):
    pass


class OpenOptionCreate(OpenOptionBase):
    pass


class AssignmentOptionCreate(AssignmentOptionBase):
    pass


class GapTextOptionCreate(GapTextOptionBase):
    pass


class SingleChoiceAnswerCreate(SingleChoiceAnswerBase):
    pass


class MultipleChoiceAnswerCreate(MultipleChoiceAnswerBase):
    pass


class OpenAnswerCreate(OpenAnswerBase):
    pass


class AssignmentAnswerCreate(AssignmentAnswerBase):
    pass


class GapTextAnswerCreate(GapTextAnswerBase):
    pass


class UserCreate(UserBase):
    password: str | None = None


class LabelCreate(LabelBase):
    quiz_ids: List[int] = []


class QuizRead(QuizBase):
    id: int
    single_choice_questions: List["SingleChoiceQuestionRead"] = []
    multiple_choice_questions: List["MultipleChoiceQuestionRead"] = []
    open_questions: List["OpenQuestionRead"] = []
    assignment_questions: List["AssignmentQuestionRead"] = []
    gap_text_questions: List["GapTextQuestionRead"] = []
    labels: List["LabelRead"] = []


class ResultRead(ResultBase):
    id: int
    created_at: datetime
    single_choice_answers: List["SingleChoiceAnswerRead"] = []
    multiple_choice_answers: List["MultipleChoiceAnswerRead"] = []
    open_answers: List["OpenAnswerRead"] = []
    assignment_answers: List["AssignmentAnswerRead"] = []
    gap_text_answers: List["GapTextAnswerRead"] = []


class AnswerRead(AnswerBase):
    id: int
    result_id: int
    question_id: int
    score: int
    max_score: int


class SingleChoiceQuestionRead(SingleChoiceQuestionBase):
    id: int
    single_choice_options: List["SingleChoiceOptionRead"] = []


class MultipleChoiceQuestionRead(MultipleChoiceQuestionBase):
    id: int
    multiple_choice_options: List["MultipleChoiceOptionRead"] = []


class OpenQuestionRead(OpenQuestionBase):
    id: int
    open_options: List["OpenOptionRead"] = []


class AssignmentQuestionRead(AssignmentQuestionBase):
    id: int
    assignment_options: List["AssignmentOptionRead"] = []


class GapTextQuestionRead(GapTextQuestionBase):
    id: int
    gap_text_sub_questions: List["GapTextSubQuestionRead"] = []


class GapTextSubQuestionRead(GapTextSubQuestionBase):
    id: int
    gap_text_options: List["GapTextOptionRead"] = []


class SingleChoiceOptionRead(SingleChoiceOptionBase):
    id: int


class MultipleChoiceOptionRead(MultipleChoiceOptionBase):
    id: int


class OpenOptionRead(OpenOptionBase):
    id: int


class AssignmentOptionRead(AssignmentOptionBase):
    id: int


class GapTextOptionRead(GapTextOptionBase):
    id: int


class SingleChoiceAnswerRead(AnswerRead, SingleChoiceAnswerBase):
    pass


class MultipleChoiceAnswerRead(AnswerRead, MultipleChoiceAnswerBase):
    pass


class OpenAnswerRead(AnswerRead, OpenAnswerBase):
    pass


class AssignmentAnswerRead(AnswerRead, AssignmentAnswerBase):
    pass


class GapTextAnswerRead(AnswerRead, GapTextAnswerBase):
    pass


class UserRead(UserBase):
    id: int
    results: List["ResultRead"] = []


class LabelRead(LabelBase):
    id: int
    quiz_ids: List[int] = []


class Answers(BaseModel):
    single_choice_answers: List[SingleChoiceAnswerCreate] = []
    multiple_choice_answers: List[MultipleChoiceAnswerCreate] = []
    open_answers: List[OpenAnswerCreate] = []
    assignment_answers: List[AssignmentAnswerCreate] = []
    gap_text_answers: List[GapTextAnswerCreate] = []
