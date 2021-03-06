"""Change genres to array and remove genres table

Revision ID: 28c79058f65a
Revises: 9ebe5a59a0cd
Create Date: 2020-11-16 06:02:48.483465

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28c79058f65a'
down_revision = '9ebe5a59a0cd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('genres')
    op.execute(('ALTER TABLE artists '
                'ALTER COLUMN genres '
                'TYPE VARCHAR[] '
                'USING genres::character varying[];'))
    op.alter_column('artists', 'genres',
               existing_type=sa.ARRAY(sa.String()),
               nullable=False)
    op.add_column('venues', sa.Column('genres', sa.ARRAY(sa.String()), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venues', 'genres')
    op.alter_column('artists', 'genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.create_table('genres',
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('name', name='genres_pkey')
    )
    # ### end Alembic commands ###
