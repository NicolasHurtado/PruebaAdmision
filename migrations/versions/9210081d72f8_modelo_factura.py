"""Modelo Factura

Revision ID: 9210081d72f8
Revises: 366e310b70ed
Create Date: 2022-01-17 14:47:45.355638

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9210081d72f8'
down_revision = '366e310b70ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Facturas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fecha', sa.Date(), nullable=True),
    sa.Column('cliente', sa.String(length=50), nullable=True),
    sa.Column('detalle', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('totalimpuestos', sa.Float(), nullable=True),
    sa.Column('totalpagar', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Facturas')
    # ### end Alembic commands ###