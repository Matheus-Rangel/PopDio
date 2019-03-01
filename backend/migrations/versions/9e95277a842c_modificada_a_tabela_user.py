"""Modificada a Tabela User

Revision ID: 9e95277a842c
Revises: e2096e2b9d66
Create Date: 2019-02-28 16:17:31.780548

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e95277a842c'
down_revision = 'e2096e2b9d66'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('revoked_tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jti', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_revoked_tokens_jti'), 'revoked_tokens', ['jti'], unique=True)
    op.create_unique_constraint(None, 'cabo_fibra', ['nome'])
    op.create_index(op.f('ix_local_nome'), 'local', ['nome'], unique=True)
    op.add_column('user', sa.Column('admin', sa.Boolean(), nullable=True))
    op.drop_index('ix_user_email', table_name='user')
    op.drop_column('user', 'profile_image')
    op.drop_column('user', 'email')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('email', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('profile_image', sa.VARCHAR(length=20), autoincrement=False, nullable=False))
    op.create_index('ix_user_email', 'user', ['email'], unique=True)
    op.drop_column('user', 'admin')
    op.drop_index(op.f('ix_local_nome'), table_name='local')
    op.drop_constraint(None, 'cabo_fibra', type_='unique')
    op.drop_index(op.f('ix_revoked_tokens_jti'), table_name='revoked_tokens')
    op.drop_table('revoked_tokens')
    # ### end Alembic commands ###
