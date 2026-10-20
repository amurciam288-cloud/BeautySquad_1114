"""add simulated payments

Revision ID: 4a1f7f0e4e2a
Revises: fbd3966caad0
Create Date: 2026-10-20 15:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "4a1f7f0e4e2a"
down_revision = "fbd3966caad0"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "payment",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("appointment_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("method", sa.String(length=30), nullable=False),
        sa.Column("reference", sa.String(length=80), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["appointment_id"], ["appointment.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("appointment_id"),
        sa.UniqueConstraint("reference"),
    )


def downgrade():
    op.drop_table("payment")
