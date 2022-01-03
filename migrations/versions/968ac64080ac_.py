"""Inital Migration

Revision ID: 968ac64080ac
Revises: 
Create Date: 2022-01-03 06:34:37.871976

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "968ac64080ac"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=80), nullable=True),
        sa.Column("password", sa.String(length=100), nullable=True),
        sa.Column("week_start_pref", sa.String(length=3), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.create_table(
        "tile",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("icon", sa.String(length=200), nullable=False),
        sa.Column("url", sa.String(length=200), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("tile")
    op.drop_table("user")
    # ### end Alembic commands ###