"""Quiz router."""

from datetime import UTC, datetime

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from quiz_api.db import db_engine
from quiz_api.models import (
    Answers,
    AssignmentAnswer,
    AssignmentQuestion,
    GapTextAnswer,
    GapTextSubQuestion,
    MultipleChoiceAnswer,
    MultipleChoiceQuestion,
    OpenAnswer,
    OpenQuestion,
    Quiz,
    QuizCreate,
    QuizRead,
    Result,
    ResultRead,
    SingleChoiceAnswer,
    SingleChoiceQuestion,
    User,
)
from quiz_api.security import get_current_user, require_admin

quiz_router = APIRouter(prefix="/quiz", tags=["quiz"])


@quiz_router.get(
    "",
    response_model=list[QuizRead],
    operation_id="get_quizzes",
)
async def get_quizzes():
    """Get all quizzes."""

    with Session(db_engine) as session:
        quizzes = session.exec(select(Quiz)).unique().all()

        for quiz in quizzes:
            for label in quiz.labels:
                session.refresh(label)

    return quizzes


@quiz_router.get(
    "/{quiz_id}",
    response_model=QuizRead,
    operation_id="get_quiz",
)
async def get_quiz(quiz_id: int):
    """Get a quiz by ID."""

    with Session(db_engine) as session:
        quiz = session.get(Quiz, quiz_id)

        for label in quiz.labels:
            session.refresh(label)

    return quiz


@quiz_router.post(
    "",
    response_model=QuizRead,
    operation_id="create_quiz",
    dependencies=[Depends(require_admin)],
)
async def create_quiz(quiz: QuizCreate):
    """Create a quiz."""

    with Session(db_engine) as session:
        db_quiz = Quiz.model_validate(quiz)
        session.add(db_quiz)
        session.commit()
        session.refresh(db_quiz)

        for label in db_quiz.labels:
            session.refresh(label)

    return db_quiz


@quiz_router.put(
    "/{quiz_id}",
    response_model=QuizRead,
    operation_id="update_quiz",
    dependencies=[Depends(require_admin)],
)
async def update_quiz(quiz_id: int, quiz: QuizCreate):
    """Update a quiz by ID."""

    with Session(db_engine) as session:
        db_quiz = session.get(Quiz, quiz_id)

        db_quiz.title = quiz.title

        session.add(db_quiz)
        session.commit()
        session.refresh(db_quiz)

        for label in db_quiz.labels:
            session.refresh(label)

    return db_quiz


@quiz_router.delete(
    "/{quiz_id}",
    response_model=int,
    operation_id="delete_quiz",
    dependencies=[Depends(require_admin)],
)
async def delete_quiz(quiz_id: int):
    """Delete a quiz by ID."""

    with Session(db_engine) as session:
        quiz = session.get(Quiz, quiz_id)

        results = (
            session.exec(select(Result).filter(Result.quiz_id == quiz_id))
            .unique()
            .all()
        )

        for label in quiz.labels:
            session.refresh(label)

            if len(label.quizzes) == 1:
                session.delete(label)

        for result in results:
            for single_choice_answer in result.single_choice_answers:
                session.delete(single_choice_answer)
            for multiple_choice_answer in result.multiple_choice_answers:
                session.delete(multiple_choice_answer)
            for open_answer in result.open_answers:
                session.delete(open_answer)
            for gap_text_answer in result.gap_text_answers:
                session.delete(gap_text_answer)
            for assignment_answer in result.assignment_answers:
                session.delete(assignment_answer)

            session.delete(result)

        if quiz is not None:
            session.delete(quiz)
            session.commit()

    return quiz_id


@quiz_router.get(
    "/{quiz_id}/results",
    response_model=list[ResultRead],
    operation_id="get_quiz_results",
)
async def get_results(quiz_id: int, current_user: User = Depends(get_current_user)):
    """Get all results for a quiz."""

    with Session(db_engine) as session:
        results = (
            session.exec(
                select(Result).filter(
                    Result.quiz_id == quiz_id and Result.user_id == current_user.id
                )
            )
            .unique()
            .all()
        )

    return results


@quiz_router.post(
    "/{quiz_id}/submit",
    response_model=ResultRead,
    operation_id="submit_quiz",
)
async def submit_quiz(
    quiz_id: int, answers: Answers, current_user: User = Depends(get_current_user)
):
    """Finish a quiz."""

    with Session(db_engine) as session:
        result = Result(
            quiz_id=quiz_id, user_id=current_user.id, created_at=datetime.now(UTC)
        )

        session.add(result)
        session.commit()
        session.refresh(result)

    with Session(db_engine) as session:
        result = session.get(Result, result.id)

        for single_choice_answer in answers.single_choice_answers:
            single_choice_question = session.get(
                SingleChoiceQuestion, single_choice_answer.question_id
            )

            db_single_choice_answer = SingleChoiceAnswer(
                selected_index=single_choice_answer.selected_index,
                result_id=result.id,
                question_id=single_choice_question.id,
            )

            score = (
                1
                if single_choice_question.difficulty == "easy"
                else 2
                if single_choice_question.difficulty == "medium"
                else 3
            )

            if (
                single_choice_answer.selected_index
                == single_choice_question.correct_index
            ):
                result.score += score
                db_single_choice_answer.score = score

            db_single_choice_answer.max_score = score
            result.max_score += score

            session.add(db_single_choice_answer)

        for multiple_choice_answer in answers.multiple_choice_answers:
            multiple_choice_question = session.get(
                MultipleChoiceQuestion, multiple_choice_answer.question_id
            )

            db_multiple_choice_answer = MultipleChoiceAnswer(
                selected_indices=multiple_choice_answer.selected_indices,
                result_id=result.id,
                question_id=multiple_choice_question.id,
            )

            score = (
                1
                if multiple_choice_question.difficulty == "easy"
                else 2
                if multiple_choice_question.difficulty == "medium"
                else 3
            )

            if set(multiple_choice_answer.selected_indices) == set(
                multiple_choice_question.correct_indices
            ):
                result.score += score
                db_multiple_choice_answer.score = score

            db_multiple_choice_answer.max_score = score
            result.max_score += score

            session.add(db_multiple_choice_answer)

        for open_answer in answers.open_answers:
            open_question = session.get(OpenQuestion, open_answer.question_id)

            db_open_answer = OpenAnswer(
                text=open_answer.text,
                result_id=result.id,
                question_id=open_question.id,
            )

            score = (
                1
                if open_question.difficulty == "easy"
                else 2
                if open_question.difficulty == "medium"
                else 3
            )

            if all(
                [
                    open_option.text.lower() in open_answer.text.lower()
                    for open_option in open_question.open_options
                ]
            ):
                result.score += score
                db_open_answer.score = score

            db_open_answer.max_score = score
            result.max_score += score

            session.add(db_open_answer)

        for gap_text_answer in answers.gap_text_answers:
            gap_text_question = session.get(
                GapTextSubQuestion, gap_text_answer.question_id
            )

            db_gap_text_answer = GapTextAnswer(
                selected_indices=gap_text_answer.selected_indices,
                result_id=result.id,
                question_id=gap_text_question.id,
            )

            score = (
                1
                if gap_text_question.difficulty == "easy"
                else 2
                if gap_text_question.difficulty == "medium"
                else 3
            )

            if gap_text_answer.selected_indices == gap_text_question.correct_indices:
                result.score += score * len(gap_text_question.correct_indices)
                db_gap_text_answer.score = score * len(
                    gap_text_question.correct_indices
                )

            db_gap_text_answer.max_score = score * len(
                gap_text_question.correct_indices
            )
            result.max_score += score * len(gap_text_question.correct_indices)

            session.add(db_gap_text_answer)

        for assignment_answer in answers.assignment_answers:
            assignment_question = session.get(
                AssignmentQuestion, assignment_answer.question_id
            )

            db_assignment_answer = AssignmentAnswer(
                selected_indices=assignment_answer.selected_indices,
                result_id=result.id,
                question_id=assignment_question.id,
            )

            score = (
                1
                if assignment_question.difficulty == "easy"
                else 2
                if assignment_question.difficulty == "medium"
                else 3
            )

            if (
                assignment_answer.selected_indices
                == assignment_question.correct_indices
            ):
                result.score += score
                db_assignment_answer.score = score

            db_assignment_answer.max_score = score
            result.max_score += score

            session.add(db_assignment_answer)

        session.add(result)
        session.commit()
        session.refresh(result)

        return result
