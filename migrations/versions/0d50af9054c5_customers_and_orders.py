"""customers and orders

Revision ID: 0d50af9054c5
Revises: 27b6a1fab7eb
Create Date: 2024-10-18 13:01:33.984207

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d50af9054c5'
down_revision: Union[str, None] = '27b6a1fab7eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customers',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('address', sa.String(length=128), nullable=True),
    sa.Column('phone', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_customers'))
    )
    op.create_index(op.f('ix_customers_name'), 'customers', ['name'], unique=True)
    op.create_table('orders',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('customer_id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], name=op.f('fk_orders_customer_id_customers')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_orders'))
    )
    op.create_index(op.f('ix_orders_customer_id'), 'orders', ['customer_id'], unique=False)
    op.create_index(op.f('ix_orders_timestamp'), 'orders', ['timestamp'], unique=False)
    op.create_table('order_items',
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Uuid(), nullable=False),
    sa.Column('unit_price', sa.Float(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], name=op.f('fk_order_items_order_id_orders')),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], name=op.f('fk_order_items_product_id_products')),
    sa.PrimaryKeyConstraint('product_id', 'order_id', name=op.f('pk_order_items'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order_items')
    op.drop_index(op.f('ix_orders_timestamp'), table_name='orders')
    op.drop_index(op.f('ix_orders_customer_id'), table_name='orders')
    op.drop_table('orders')
    op.drop_index(op.f('ix_customers_name'), table_name='customers')
    op.drop_table('customers')
    # ### end Alembic commands ###
