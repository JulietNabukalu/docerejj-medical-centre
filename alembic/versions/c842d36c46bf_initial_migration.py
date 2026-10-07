"""initial migration

Revision ID: c842d36c46bf
Revises:
Create Date: 2026-09-04 07:03:18.870344

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "c842d36c46bf"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Baseline existing database."""
    pass


def downgrade() -> None:
    """Baseline migration has nothing to downgrade."""
    pass