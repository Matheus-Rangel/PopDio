"""Correcoes na tabela dio_porta

Revision ID: 192332b9b14f
Revises: 9e95277a842c
Create Date: 2019-03-07 16:17:41.281768

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '192332b9b14f'
down_revision = '9e95277a842c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cabo_fibra', sa.Column('observacao', sa.String(length=128), nullable=True))
    op.create_index(op.f('ix_cabo_fibra_nome'), 'cabo_fibra', ['nome'], unique=True)
    op.drop_constraint('cabo_fibra_nome_key', 'cabo_fibra', type_='unique')
    op.drop_column('dio', 'numero_portas')
    op.drop_constraint('dio_porta_local_destino_id_fkey', 'dio_porta', type_='foreignkey')
    op.drop_constraint('dio_porta_last_user_id_fkey', 'dio_porta', type_='foreignkey')
    op.drop_column('dio_porta', 'local_destino_id')
    op.drop_column('dio_porta', 'bypass')
    op.drop_column('dio_porta', 'fibra_grupo')
    op.drop_column('dio_porta', 'last_user_id')
    op.create_unique_constraint(None, 'estado_link', ['nome'])
    op.alter_column('local', 'observacao',
               existing_type=sa.TEXT(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('local', 'observacao',
               existing_type=sa.TEXT(),
               nullable=False)
    op.drop_constraint(None, 'estado_link', type_='unique')
    op.add_column('dio_porta', sa.Column('last_user_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('dio_porta', sa.Column('fibra_grupo', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('dio_porta', sa.Column('bypass', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.add_column('dio_porta', sa.Column('local_destino_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('dio_porta_last_user_id_fkey', 'dio_porta', 'user', ['last_user_id'], ['id'])
    op.create_foreign_key('dio_porta_local_destino_id_fkey', 'dio_porta', 'local', ['local_destino_id'], ['id'])
    op.add_column('dio', sa.Column('numero_portas', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_unique_constraint('cabo_fibra_nome_key', 'cabo_fibra', ['nome'])
    op.drop_index(op.f('ix_cabo_fibra_nome'), table_name='cabo_fibra')
    op.drop_column('cabo_fibra', 'observacao')
    # ### end Alembic commands ###