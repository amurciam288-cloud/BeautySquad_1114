"""add demo catalog and public team profiles

Revision ID: 8c2e7d4a1b90
Revises: 4a1f7f0e4e2a
Create Date: 2026-10-21 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "8c2e7d4a1b90"
down_revision = "4a1f7f0e4e2a"
branch_labels = None
depends_on = None


SERVICES = [
    ("Corte y peinado", "Corte personalizado y peinado con acabado profesional.", 45000, "https://images.unsplash.com/photo-1562322140-8baeececf3df?auto=format&fit=crop&w=900&q=85"),
    ("Coloración y brushing", "Coloración pensada para renovar tu look y brushing de larga duración.", 110000, "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=900&q=85"),
    ("Manicure semipermanente", "Manicure semipermanente con cuidado de uñas y acabado brillante.", 55000, "https://images.unsplash.com/photo-1604654894610-df63bc536371?auto=format&fit=crop&w=900&q=85"),
    ("Depilación corporal", "Cuidado corporal y depilación con atención delicada y profesional.", 60000, "https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=900&q=85"),
    ("Asesoría de nutrición y bienestar", "Orientación práctica para construir hábitos de bienestar sostenibles.", 80000, "https://images.unsplash.com/photo-1490645935967-10de6ba17061?auto=format&fit=crop&w=900&q=85"),
]

TEAM = [
    ("Laura Gómez", "Dietética y bienestar", "https://images.unsplash.com/photo-1490645935967-10de6ba17061?auto=format&fit=crop&w=700&q=85"),
    ("Mariana Rojas", "Estilismo y color", "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=700&q=85"),
    ("Sofía Torres", "Uñas y manicure", "https://images.unsplash.com/photo-1604654894610-df63bc536371?auto=format&fit=crop&w=700&q=85"),
    ("Camila Vargas", "Depilación y cuidado corporal", "https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=700&q=85"),
]


def upgrade():
    op.add_column("service", sa.Column("image_url", sa.String(length=500), nullable=True))
    op.create_table(
        "team_member",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("specialty", sa.String(length=120), nullable=False),
        sa.Column("image_url", sa.String(length=500), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )

    bind = op.get_bind()
    service_table = sa.table(
        "service",
        sa.column("name", sa.String),
        sa.column("description", sa.String),
        sa.column("price", sa.Numeric(10, 2)),
        sa.column("image_url", sa.String),
    )
    team_table = sa.table(
        "team_member",
        sa.column("name", sa.String),
        sa.column("specialty", sa.String),
        sa.column("image_url", sa.String),
    )

    existing_services = {row.name for row in bind.execute(sa.select(service_table.c.name))}
    for name, description, price, image_url in SERVICES:
        if name not in existing_services:
            bind.execute(service_table.insert().values(
                name=name,
                description=description,
                price=price,
                image_url=image_url,
            ))

    existing_team = {row.name for row in bind.execute(sa.select(team_table.c.name))}
    for name, specialty, image_url in TEAM:
        if name not in existing_team:
            bind.execute(team_table.insert().values(
                name=name,
                specialty=specialty,
                image_url=image_url,
            ))


def downgrade():
    op.drop_table("team_member")
    op.drop_column("service", "image_url")
