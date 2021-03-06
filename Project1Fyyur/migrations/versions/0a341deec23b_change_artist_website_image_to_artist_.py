"""Change Artist.website_image to Artist.website

Revision ID: 0a341deec23b
Revises: 28c79058f65a
Create Date: 2020-11-17 19:49:25.129472

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a341deec23b'
down_revision = '28c79058f65a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('website', sa.String(length=120), nullable=True))
    op.drop_column('artists', 'website_link')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('website_link', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.drop_column('artists', 'website')
    # ### end Alembic commands ###
