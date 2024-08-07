import sqlmodel

"""Add practice quizzes

Revision ID: 0ddbe21abd60
Revises: 5b540b409d71
Create Date: 2024-07-03 17:14:06.819866

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0ddbe21abd60"
down_revision: Union[str, None] = "5b540b409d71"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "quiz",
        sa.Column(
            "is_practice", sa.Boolean(), nullable=False, server_default=sqlmodel.false()
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("quiz", "is_practice")
    # ### end Alembic commands ###
