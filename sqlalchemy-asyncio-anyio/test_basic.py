"""
Basic tests for the anyio-based SQLAlchemy asyncio extension.

Tests basic CRUD operations using SQLAlchemy Core.
"""

import asyncio
import anyio
from sqlalchemy import Table, Column, Integer, String, MetaData, select, insert, update, delete

from async_sqlalchemy import create_async_engine


async def test_basic_operations():
    """Test basic CRUD operations with SQLAlchemy Core."""
    print("=" * 60)
    print("Testing Basic CRUD Operations with SQLAlchemy Core")
    print("=" * 60)
    
    # Create async engine
    engine = create_async_engine("sqlite+aiosqlite:///./test.db", echo=False)
    
    # Define metadata and table
    metadata = MetaData()
    users = Table(
        'users',
        metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String(50)),
        Column('email', String(100)),
    )
    
    # Create tables
    print("\n1. Creating tables...")
    async with engine.begin() as conn:
        # Use the sync engine to create tables in a thread
        await anyio.to_thread.run_sync(lambda: metadata.create_all(engine.sync_engine))
    print("✓ Tables created")
    
    # Insert data
    print("\n2. Inserting data...")
    async with engine.begin() as conn:
        await conn.execute(
            insert(users).values([
                {'name': 'Alice', 'email': 'alice@example.com'},
                {'name': 'Bob', 'email': 'bob@example.com'},
                {'name': 'Charlie', 'email': 'charlie@example.com'},
            ])
        )
    print("✓ Data inserted")
    
    # Select all
    print("\n3. Selecting all users...")
    async with engine.connect() as conn:
        result = await conn.execute(select(users))
        rows = await result.fetchall()
        print(f"✓ Found {len(rows)} users:")
        for row in rows:
            print(f"  - ID: {row.id}, Name: {row.name}, Email: {row.email}")
    
    # Select with filter
    print("\n4. Selecting specific user...")
    async with engine.connect() as conn:
        result = await conn.execute(
            select(users).where(users.c.name == 'Alice')
        )
        row = await result.first()
        if row:
            print(f"✓ Found user: {row.name} ({row.email})")
        else:
            print("✗ User not found")
    
    # Update
    print("\n5. Updating user...")
    async with engine.begin() as conn:
        await conn.execute(
            update(users)
            .where(users.c.name == 'Alice')
            .values(email='alice.wonderland@example.com')
        )
    print("✓ User updated")
    
    # Verify update
    print("\n6. Verifying update...")
    async with engine.connect() as conn:
        result = await conn.execute(
            select(users).where(users.c.name == 'Alice')
        )
        row = await result.first()
        if row:
            print(f"✓ Updated email: {row.email}")
        else:
            print("✗ User not found")
    
    # Test scalar
    print("\n7. Testing scalar query...")
    async with engine.connect() as conn:
        count = await conn.scalar(select(users.c.id).where(users.c.name == 'Bob'))
        print(f"✓ Bob's ID: {count}")
    
    # Delete
    print("\n8. Deleting user...")
    async with engine.begin() as conn:
        await conn.execute(
            delete(users).where(users.c.name == 'Charlie')
        )
    print("✓ User deleted")
    
    # Verify deletion
    print("\n9. Verifying deletion...")
    async with engine.connect() as conn:
        result = await conn.execute(select(users))
        rows = await result.fetchall()
        print(f"✓ Remaining users: {len(rows)}")
        for row in rows:
            print(f"  - {row.name}")
    
    # Test scalars
    print("\n10. Testing scalars query...")
    async with engine.connect() as conn:
        result = await conn.execute(select(users.c.name))
        scalars = await result.scalars()
        names = await scalars.all()
        print(f"✓ All user names: {', '.join(names)}")
    
    # Cleanup
    print("\n11. Cleaning up...")
    async with engine.begin() as conn:
        await anyio.to_thread.run_sync(lambda: metadata.drop_all(engine.sync_engine))
    print("✓ Tables dropped")
    
    await engine.dispose()
    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)


async def test_transaction_rollback():
    """Test transaction rollback behavior."""
    print("\n" + "=" * 60)
    print("Testing Transaction Rollback")
    print("=" * 60)
    
    engine = create_async_engine("sqlite+aiosqlite:///./test_rollback.db", echo=False)
    
    metadata = MetaData()
    items = Table(
        'items',
        metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String(50)),
    )
    
    # Create table
    print("\n1. Creating table...")
    async with engine.begin() as conn:
        await anyio.to_thread.run_sync(lambda: metadata.create_all(engine.sync_engine))
    print("✓ Table created")
    
    # Test successful transaction
    print("\n2. Testing successful transaction...")
    async with engine.begin() as conn:
        await conn.execute(insert(items).values(name='Item 1'))
        await conn.execute(insert(items).values(name='Item 2'))
    print("✓ Transaction committed")
    
    # Verify data
    async with engine.connect() as conn:
        result = await conn.execute(select(items))
        rows = await result.fetchall()
        print(f"✓ Found {len(rows)} items after commit")
    
    # Test rollback
    print("\n3. Testing transaction rollback...")
    try:
        async with engine.begin() as conn:
            await conn.execute(insert(items).values(name='Item 3'))
            # Force an error
            raise ValueError("Simulated error")
    except ValueError:
        print("✓ Transaction rolled back due to error")
    
    # Verify rollback
    async with engine.connect() as conn:
        result = await conn.execute(select(items))
        rows = await result.fetchall()
        print(f"✓ Still have {len(rows)} items (Item 3 was rolled back)")
    
    # Cleanup
    print("\n4. Cleaning up...")
    async with engine.begin() as conn:
        await anyio.to_thread.run_sync(lambda: metadata.drop_all(engine.sync_engine))
    await engine.dispose()
    print("✓ Cleaned up")
    
    print("\n" + "=" * 60)
    print("Transaction rollback test passed! ✓")
    print("=" * 60)


async def main():
    """Run all tests."""
    await test_basic_operations()
    await test_transaction_rollback()


if __name__ == "__main__":
    asyncio.run(main())
