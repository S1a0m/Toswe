"""Nouvelle base propre

Revision ID: ef063315eadb
Revises: 9e9997024571
Create Date: 2025-04-19 11:48:34.022461

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ef063315eadb'
down_revision: Union[str, None] = '9e9997024571'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('products', 'category',
               existing_type=postgresql.ENUM('tech', 'local', name='productcategory'),
               type_=sa.Enum('computer', 'local', 'accessories', 'fashion', 'sport', name='productcategory', native_enum=False),
               existing_nullable=True)
    op.alter_column('products', 'status',
               existing_type=postgresql.ENUM('draft', 'published', 'unpublished', name='productstatus'),
               type_=sa.Enum('draft', 'published', 'unpublished', name='productstatus', native_enum=False),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('products', 'status',
               existing_type=sa.Enum('draft', 'published', 'unpublished', name='productstatus', native_enum=False),
               type_=postgresql.ENUM('draft', 'published', 'unpublished', name='productstatus'),
               existing_nullable=True)
    op.alter_column('products', 'category',
               existing_type=sa.Enum('computer', 'local', 'accessories', 'fashion', 'sport', name='productcategory', native_enum=False),
               type_=postgresql.ENUM('tech', 'local', name='productcategory'),
               existing_nullable=True)
    # ### end Alembic commands ###
