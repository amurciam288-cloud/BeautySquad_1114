"""replace fictitious public team profiles with project members

Revision ID: d4e5f6a7b8c9
Revises: 8c2e7d4a1b90
Create Date: 2026-10-21 00:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "d4e5f6a7b8c9"
down_revision = "8c2e7d4a1b90"
branch_labels = None
depends_on = None


TEAM_MEMBERS = (
    "Cathalina Murcia",
    "Valentina Alape",
    "Liseth Reyes",
)
TEAM_SPECIALTY = "Equipo BeautySquad"
FALLBACK_IMAGE = "/static/placeholder-team.svg"
DEMO_TEAM = (
    ("Laura Gómez", "Dietética y bienestar"),
    ("Mariana Rojas", "Estilismo y color"),
    ("Sofía Torres", "Uñas y manicure"),
    ("Camila Vargas", "Depilación y cuidado corporal"),
)


def upgrade():
    bind = op.get_bind()
    team_table = sa.table(
        "team_member",
        sa.column("id", sa.Integer),
        sa.column("name", sa.String),
        sa.column("specialty", sa.String),
        sa.column("image_url", sa.String),
    )

    existing_images = [
        row.image_url
        for row in bind.execute(
            sa.select(team_table.c.image_url).order_by(team_table.c.id)
        )
        if row.image_url
    ]

    # Rebuild this small public projection so repeated execution always leaves
    # exactly the confirmed project members and no fictitious profiles.
    bind.execute(team_table.delete())
    for index, name in enumerate(TEAM_MEMBERS):
        image_url = (
            existing_images[index]
            if index < len(existing_images)
            else FALLBACK_IMAGE
        )
        bind.execute(team_table.insert().values(
            name=name,
            specialty=TEAM_SPECIALTY,
            image_url=image_url,
        ))


def downgrade():
    bind = op.get_bind()
    team_table = sa.table(
        "team_member",
        sa.column("name", sa.String),
        sa.column("specialty", sa.String),
        sa.column("image_url", sa.String),
    )
    bind.execute(team_table.delete())
    for name, specialty in DEMO_TEAM:
        bind.execute(team_table.insert().values(
            name=name,
            specialty=specialty,
            image_url=FALLBACK_IMAGE,
        ))
