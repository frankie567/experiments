"""
Comprehensive example demonstrating the anyio-based SQLAlchemy asyncio extension.

This example shows various usage patterns including:
- Creating engines and connections
- Using Core SQL
- Using ORM with declarative models
- Transaction management
- Session lifecycle
"""

import asyncio
from sqlalchemy import String, Integer, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from async_sqlalchemy import create_async_engine, AsyncSessionmaker


# Define ORM models
class Base(DeclarativeBase):
    """Base class for ORM models."""
    pass


class Product(Base):
    """Product model."""
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column(Integer)  # Price in cents
    
    def __repr__(self):
        return f"Product(id={self.id}, name='{self.name}', price=${self.price/100:.2f})"


async def example_core_usage():
    """Example using SQLAlchemy Core."""
    print("=" * 60)
    print("Example: SQLAlchemy Core Usage")
    print("=" * 60)
    
    # Create an async engine
    # Note: We use sqlite+aiosqlite URL, but the implementation converts it
    # to use standard sqlite with thread pool execution via anyio
    engine = create_async_engine("sqlite+aiosqlite:///./example.db", echo=False)
    
    # Create tables using the sync engine in a thread
    import anyio
    await anyio.to_thread.run_sync(lambda: Base.metadata.create_all(engine.sync_engine))
    
    # Insert data using a connection with automatic transaction
    print("\nInserting products...")
    async with engine.begin() as conn:
        from sqlalchemy import insert, Table, MetaData
        
        # Get the products table
        products_table = Product.__table__
        
        # Insert multiple rows
        await conn.execute(
            insert(products_table).values([
                {'name': 'Laptop', 'price': 99900},
                {'name': 'Mouse', 'price': 2500},
                {'name': 'Keyboard', 'price': 7500},
            ])
        )
        # Transaction auto-commits when exiting the context
    
    print("✓ Products inserted")
    
    # Query data
    print("\nQuerying products...")
    async with engine.connect() as conn:
        result = await conn.execute(select(Product))
        rows = await result.fetchall()
        
        print(f"Found {len(rows)} products:")
        for row in rows:
            print(f"  - {row.name}: ${row.price/100:.2f}")
    
    # Clean up
    await anyio.to_thread.run_sync(lambda: Base.metadata.drop_all(engine.sync_engine))
    await engine.dispose()
    
    print("\n✓ Core usage example complete")


async def example_orm_usage():
    """Example using SQLAlchemy ORM with AsyncSession."""
    print("\n" + "=" * 60)
    print("Example: SQLAlchemy ORM Usage")
    print("=" * 60)
    
    # Create engine
    engine = create_async_engine("sqlite+aiosqlite:///./example.db", echo=False)
    
    # Create tables
    import anyio
    await anyio.to_thread.run_sync(lambda: Base.metadata.create_all(engine.sync_engine))
    
    # Create session factory
    async_session = AsyncSessionmaker(bind=engine)
    
    # Add products using ORM
    print("\nAdding products with ORM...")
    async with async_session.begin() as session:
        products = [
            Product(name="Desktop", price=149900),
            Product(name="Monitor", price=29900),
            Product(name="Webcam", price=8900),
        ]
        session.add_all(products)
        # Transaction auto-commits when exiting begin() context
    
    print("✓ Products added")
    
    # Query with ORM
    print("\nQuerying products with ORM...")
    async with async_session() as session:
        result = await session.execute(select(Product).order_by(Product.price.desc()))
        products = await (await result.scalars()).all()
        
        print(f"Products ordered by price (descending):")
        for product in products:
            print(f"  - {product}")
    
    # Get by ID
    print("\nGetting product by ID...")
    async with async_session() as session:
        product = await session.get(Product, 2)
        if product:
            print(f"✓ Found product with ID 2: {product}")
    
    # Update a product
    print("\nUpdating product...")
    async with async_session.begin() as session:
        result = await session.execute(select(Product).where(Product.name == "Monitor"))
        product = await (await result.scalars()).first()
        
        if product:
            old_price = product.price
            product.price = 24900  # Discount!
            print(f"✓ Updated {product.name} price from ${old_price/100:.2f} to ${product.price/100:.2f}")
    
    # Delete a product
    print("\nDeleting product...")
    async with async_session.begin() as session:
        result = await session.execute(select(Product).where(Product.name == "Webcam"))
        product = await (await result.scalars()).first()
        
        if product:
            await session.delete(product)
            print(f"✓ Deleted product: {product.name}")
    
    # Verify changes
    print("\nFinal product list...")
    async with async_session() as session:
        result = await session.execute(select(Product))
        products = await (await result.scalars()).all()
        
        print(f"Remaining products ({len(products)}):")
        for product in products:
            print(f"  - {product}")
    
    # Clean up
    await anyio.to_thread.run_sync(lambda: Base.metadata.drop_all(engine.sync_engine))
    await engine.dispose()
    
    print("\n✓ ORM usage example complete")


async def example_transaction_management():
    """Example demonstrating transaction management."""
    print("\n" + "=" * 60)
    print("Example: Transaction Management")
    print("=" * 60)
    
    engine = create_async_engine("sqlite+aiosqlite:///./example.db", echo=False)
    
    import anyio
    await anyio.to_thread.run_sync(lambda: Base.metadata.create_all(engine.sync_engine))
    
    async_session = AsyncSessionmaker(bind=engine)
    
    # Example 1: Automatic commit with begin()
    print("\n1. Automatic commit on successful exit...")
    async with async_session.begin() as session:
        product = Product(name="Tablet", price=39900)
        session.add(product)
        print("✓ Product added, will commit on context exit")
    
    print("✓ Transaction committed automatically")
    
    # Verify
    async with async_session() as session:
        count = await session.scalar(select(Product).where(Product.name == "Tablet"))
        print(f"✓ Verified: Found product with ID {count}")
    
    # Example 2: Automatic rollback on exception
    print("\n2. Automatic rollback on exception...")
    try:
        async with async_session.begin() as session:
            product = Product(name="Smartphone", price=69900)
            session.add(product)
            print("  Product added, but will raise exception...")
            raise ValueError("Simulated error")
    except ValueError:
        print("✓ Exception caught, transaction rolled back")
    
    # Verify rollback
    async with async_session() as session:
        result = await session.execute(select(Product).where(Product.name == "Smartphone"))
        products = await (await result.scalars()).all()
        print(f"✓ Verified: Smartphone was NOT saved (found {len(products)} matches)")
    
    # Example 3: Manual commit/rollback
    print("\n3. Manual transaction control...")
    async with async_session() as session:
        product = Product(name="Headphones", price=14900)
        session.add(product)
        await session.commit()
        print("✓ Manually committed transaction")
    
    # Clean up
    await anyio.to_thread.run_sync(lambda: Base.metadata.drop_all(engine.sync_engine))
    await engine.dispose()
    
    print("\n✓ Transaction management example complete")


async def main():
    """Run all examples."""
    await example_core_usage()
    await example_orm_usage()
    await example_transaction_management()
    
    print("\n" + "=" * 60)
    print("All examples completed successfully! ✓")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
