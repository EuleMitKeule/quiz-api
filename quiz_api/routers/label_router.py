"""Label router."""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from quiz_api.db import db_engine
from quiz_api.models import Label, LabelCreate, LabelRead, Quiz
from quiz_api.security import require_admin

label_router = APIRouter(prefix="/label", tags=["label"])


@label_router.post(
    "",
    response_model=LabelRead,
    operation_id="create_label",
    dependencies=[Depends(require_admin)],
)
async def create_label(label: LabelCreate):
    """Create a label."""

    with Session(db_engine) as session:
        db_quizzes: list[Quiz] = []

        for quiz_id in label.quiz_ids:
            db_quiz = session.get(Quiz, quiz_id)

            if db_quiz is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Quiz with ID {quiz_id} not found.",
                )

            db_quizzes.append(db_quiz)

        db_label = Label(
            text=label.text,
            quizzes=db_quizzes,
        )

        session.add(db_label)
        session.commit()
        session.refresh(db_label)
        for db_quiz in db_quizzes:
            session.refresh(db_quiz)

    return db_label


@label_router.get(
    "",
    response_model=list[LabelRead],
    operation_id="get_labels",
)
async def get_labels():
    """Get all labels."""

    with Session(db_engine) as session:
        labels = session.exec(select(Label)).all()

        for label in labels:
            session.refresh(label)

            for quiz in label.quizzes:
                session.refresh(quiz)

    return labels


@label_router.get(
    "/{label_id}",
    response_model=LabelRead,
    operation_id="get_label",
)
async def get_label(label_id: int):
    """Get a label by ID."""

    with Session(db_engine) as session:
        db_label = session.get(Label, label_id)

        if db_label is None:
            raise HTTPException(
                status_code=404,
                detail=f"Label with ID {label_id} not found.",
            )

    return db_label


@label_router.put(
    "/{label_id}",
    response_model=LabelRead,
    operation_id="update_label",
    dependencies=[Depends(require_admin)],
)
async def update_label(label_id: int, label: LabelCreate):
    """Update a label by ID."""

    with Session(db_engine) as session:
        db_label = session.get(Label, label_id)

        if db_label is None:
            raise HTTPException(
                status_code=404,
                detail=f"Label with ID {label_id} not found.",
            )

        db_quizzes: list[Quiz] = []

        for quiz_id in label.quiz_ids:
            db_quiz = session.get(Quiz, quiz_id)

            if db_quiz is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Quiz with ID {quiz_id} not found.",
                )

            db_quizzes.append(db_quiz)

        db_label.text = label.text
        db_label.quizzes = db_quizzes

        session.add(db_label)
        session.commit()
        session.refresh(db_label)
        for db_quiz in db_quizzes:
            session.refresh(db_quiz)

    return db_label


@label_router.delete(
    "/{label_id}",
    response_model=int,
    operation_id="delete_label",
    dependencies=[Depends(require_admin)],
)
async def delete_label(label_id: int):
    """Delete a label by ID."""

    with Session(db_engine) as session:
        db_label = session.get(Label, label_id)

        if db_label is None:
            raise HTTPException(
                status_code=404,
                detail=f"Label with ID {label_id} not found.",
            )

        session.delete(db_label)
        session.commit()

    return label_id
