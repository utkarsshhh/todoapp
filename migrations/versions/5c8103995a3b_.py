"""empty message

Revision ID: 5c8103995a3b
Revises: 
Create Date: 2024-02-29 16:05:04.384264

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c8103995a3b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todolists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('todos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('list_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'todolists', ['list_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('todos', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('list_id')

    op.drop_table('todolists')
    # ### end Alembic commands ###
