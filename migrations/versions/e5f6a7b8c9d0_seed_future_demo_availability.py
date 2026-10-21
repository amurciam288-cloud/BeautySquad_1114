"""seed future demo availability slots

Revision ID: e5f6a7b8c9d0
Revises: d4e5f6a7b8c9
Create Date: 2026-10-21 00:45:00.000000

"""
from datetime import date, timedelta

from alembic import op
import sqlalchemy as sa


revision = "e5f6a7b8c9d0"
down_revision = "d4e5f6a7b8c9"
branch_labels = None
depends_on = None


DEMO_TIMES = ("09:00", "12:00", "15:00")
DEMO_BUSINESS_DAYS = 5


def _demo_slots(start_date):
    """Return three daytime slots for the next five weekdays."""
    slots = []
    current_date = start_date + timedelta(days=1)

    while len({slot_date for slot_date, _ in slots}) < DEMO_BUSINESS_DAYS:
        if current_date.weekday() < 5:
            slots.extend((current_date.isoformat(), time) for time in DEMO_TIMES)
        current_date += timedelta(days=1)

    return slots


def upgrade():
    bind = op.get_bind()
    availability_table = sa.table(
        "availability",
        sa.column("id", sa.Integer),
        sa.column("date", sa.String),
        sa.column("time", sa.String),
        sa.column("is_available", sa.Boolean),
    )

    for slot_date, slot_time in _demo_slots(date.today()):
        exists = bind.execute(
            sa.select(availability_table.c.id).where(
                availability_table.c.date == slot_date,
                availability_table.c.time == slot_time,
            )
        ).scalar_one_or_none()

        if exists is None:
            bind.execute(availability_table.insert().values(
                date=slot_date,
                time=slot_time,
                is_available=True,
            ))


def downgrade():
    bind = op.get_bind()
    availability_table = sa.table(
        "availability",
        sa.column("date", sa.String),
        sa.column("time", sa.String),
    )

    for slot_date, slot_time in _demo_slots(date.today()):
        bind.execute(
            availability_table.delete().where(
                availability_table.c.date == slot_date,
                availability_table.c.time == slot_time,
            )
        )
