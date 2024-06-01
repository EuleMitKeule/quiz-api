from datetime import datetime, timezone
from typing import List

from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel


class HasTitle(SQLModel):
    title: str


class HasText(SQLModel):
    text: str


class HasIndex(SQLModel):
    index: int


class HasIsCorrect(SQLModel):
    is_correct: bool = Field(default=False)


class QuizBase(HasTitle):
    pass


class ResultBase(SQLModel):
    quiz_id: int | None = Field(default=None, foreign_key="quiz.id")
    score: int | None = Field(default=None)
    total: int | None = Field(default=None)


class QuestionBase(HasText, HasIndex):
    quiz_id: int | None = Field(default=None, foreign_key="quiz.id")


class SingleChoiceQuestionBase(QuestionBase):
    pass


class MultipleChoiceQuestionBase(QuestionBase):
    pass


class OpenQuestionBase(QuestionBase):
    pass


class AssignmentQuestionBase(QuestionBase):
    pass


class GapTextQuestionBase(QuestionBase):
    pass


class GapTextSubQuestionBase(SQLModel):
    question_id: int | None = Field(default=None, foreign_key="gap_text_question.id")


class SingleChoiceOptionBase(HasText, HasIsCorrect, HasIndex):
    question_id: int | None = Field(
        default=None, foreign_key="single_choice_question.id"
    )


class MultipleChoiceOptionBase(HasText, HasIsCorrect, HasIndex):
    question_id: int | None = Field(
        default=None, foreign_key="multiple_choice_question.id"
    )


class OpenOptionBase(HasText, HasIndex):
    question_id: int | None = Field(default=None, foreign_key="open_question.id")


class AssignmentOptionBase(HasText, HasIndex):
    question_id: int | None = Field(default=None, foreign_key="assignment_question.id")
    correct_index: int


class GapTextOptionBase(HasText, HasIsCorrect, HasIndex):
    sub_question_id: int | None = Field(
        default=None, foreign_key="gap_text_sub_question.id"
    )


class UserBase(SQLModel):
    username: str = Field(index=True, nullable=False)
    is_admin: bool


class Quiz(QuizBase, table=True):
    __tablename__ = "quiz"

    id: int | None = Field(default=None, primary_key=True)
    single_choice_questions: List["SingleChoiceQuestion"] = Relationship(
        back_populates="quiz"
    )
    multiple_choice_questions: List["MultipleChoiceQuestion"] = Relationship(
        back_populates="quiz"
    )
    open_questions: List["OpenQuestion"] = Relationship(back_populates="quiz")
    assignment_questions: List["AssignmentQuestion"] = Relationship(
        back_populates="quiz"
    )
    gap_text_questions: List["GapTextQuestion"] = Relationship(back_populates="quiz")
    results: List["Result"] = Relationship(back_populates="quiz")


class Result(ResultBase, table=True):
    __tablename__ = "result"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    quiz: "Quiz" = Relationship(back_populates="results")
    user: "User" = Relationship(back_populates="results")
    created_at: datetime = Field(default=datetime.now(timezone.utc))


class SingleChoiceQuestion(SingleChoiceQuestionBase, table=True):
    __tablename__ = "single_choice_question"

    id: int | None = Field(default=None, primary_key=True)
    quiz: "Quiz" = Relationship(back_populates="single_choice_questions")
    single_choice_options: List["SingleChoiceOption"] = Relationship(
        back_populates="question"
    )


class MultipleChoiceQuestion(MultipleChoiceQuestionBase, table=True):
    __tablename__ = "multiple_choice_question"

    id: int | None = Field(default=None, primary_key=True)
    quiz: "Quiz" = Relationship(back_populates="multiple_choice_questions")
    multiple_choice_options: List["MultipleChoiceOption"] = Relationship(
        back_populates="question"
    )


class OpenQuestion(OpenQuestionBase, table=True):
    __tablename__ = "open_question"

    id: int | None = Field(default=None, primary_key=True)
    quiz: "Quiz" = Relationship(back_populates="open_questions")
    open_options: List["OpenOption"] = Relationship(back_populates="question")


class AssignmentQuestion(AssignmentQuestionBase, table=True):
    __tablename__ = "assignment_question"

    id: int | None = Field(default=None, primary_key=True)
    quiz: "Quiz" = Relationship(back_populates="assignment_questions")
    assignment_options: List["AssignmentOption"] = Relationship(
        back_populates="question"
    )


class GapTextQuestion(GapTextQuestionBase, table=True):
    __tablename__ = "gap_text_question"

    id: int | None = Field(default=None, primary_key=True)
    quiz: "Quiz" = Relationship(back_populates="gap_text_questions")
    gap_text_sub_questions: List["GapTextSubQuestion"] = Relationship(
        back_populates="question"
    )


class GapTextSubQuestion(GapTextSubQuestionBase, table=True):
    __tablename__ = "gap_text_sub_question"

    id: int | None = Field(default=None, primary_key=True)
    question: "GapTextQuestion" = Relationship(back_populates="gap_text_sub_questions")
    gap_text_options: List["GapTextOption"] = Relationship(
        back_populates="sub_question"
    )


class SingleChoiceOption(SingleChoiceOptionBase, table=True):
    __tablename__ = "single_choice_option"

    id: int | None = Field(default=None, primary_key=True)
    question: "SingleChoiceQuestion" = Relationship(
        back_populates="single_choice_options"
    )


class MultipleChoiceOption(MultipleChoiceOptionBase, table=True):
    __tablename__ = "multiple_choice_option"

    id: int | None = Field(default=None, primary_key=True)
    question: "MultipleChoiceQuestion" = Relationship(
        back_populates="multiple_choice_options"
    )


class OpenOption(OpenOptionBase, table=True):
    __tablename__ = "open_option"

    id: int | None = Field(default=None, primary_key=True)
    question: "OpenQuestion" = Relationship(back_populates="open_options")


class AssignmentOption(AssignmentOptionBase, table=True):
    __tablename__ = "assignment_option"

    id: int | None = Field(default=None, primary_key=True)
    question: "AssignmentQuestion" = Relationship(back_populates="assignment_options")


class GapTextOption(GapTextOptionBase, table=True):
    __tablename__ = "gap_text_option"

    id: int | None = Field(default=None, primary_key=True)
    sub_question: "GapTextSubQuestion" = Relationship(back_populates="gap_text_options")


class User(UserBase, table=True):
    __tablename__ = "user"

    id: int = Field(default=None, primary_key=True)
    hashed_password: str
    results: List["Result"] = Relationship(back_populates="user")


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


class UserCreate(UserBase):
    hashed_password: str
    pass


class QuizRead(QuizBase):
    id: int
    single_choice_questions: List["SingleChoiceQuestionRead"] = []
    multiple_choice_questions: List["MultipleChoiceQuestionRead"] = []


class ResultRead(ResultBase):
    id: int
    created_at: datetime
    user: "UserRead"


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


class UserRead(UserBase):
    id: int
    results: List["ResultRead"] = []
