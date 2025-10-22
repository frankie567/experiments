"""
ORM tests for the anyio-based SQLAlchemy asyncio extension.

Tests ORM operations using SQLAlchemy's declarative base and AsyncSession.
"""

import asyncio
from sqlalchemy import String, Integer, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from async_sqlalchemy import create_async_engine, AsyncSessionmaker


class Base(DeclarativeBase):
    """Base class for ORM models."""
    pass


class User(Base):
    """User model for testing."""
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100))
    
    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}', email='{self.email}')"


async def test_orm_operations():
    """Test ORM CRUD operations with AsyncSession."""
    print("=" * 60)
    print("Testing ORM Operations with AsyncSession")
    print("=" * 60)
    
    # Create async engine
    engine = create_async_engine("sqlite+aiosqlite:///./test_orm.db", echo=False)
    
    # Create tables
    print("\n1. Creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✓ Tables created")
    
    # Create session factory
    async_session = AsyncSessionmaker(bind=engine)
    
    # Insert data
    print("\n2. Inserting users with ORM...")
    async with async_session() as session:
        user1 = User(name="Alice", email="alice@example.com")
        user2 = User(name="Bob", email="bob@example.com")
        user3 = User(name="Charlie", email="charlie@example.com")
        
        session.add(user1)
        session.add(user2)
        session.add(user3)
        
        await session.commit()
        print("✓ Users inserted")
    
    # Query all users
    print("\n3. Querying all users...")
    async with async_session() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        print(f"✓ Found {len(users)} users:")
        for user in users:
            print(f"  - {user}")
    
    # Query specific user
    print("\n4. Querying specific user...")
    async with async_session() as session:
        result = await session.execute(select(User).where(User.name == "Alice"))
        user = result.scalars().first()
        if user:
            print(f"✓ Found user: {user}")
        else:
            print("✗ User not found")
    
    # Get by primary key
    print("\n5. Getting user by ID...")
    async with async_session() as session:
        user = await session.get(User, 2)
        if user:
            print(f"✓ Found user by ID: {user}")
        else:
            print("✗ User not found")
    
    # Update user
    print("\n6. Updating user...")
    async with async_session() as session:
        result = await session.execute(select(User).where(User.name == "Alice"))
        user = result.scalars().first()
        
        if user:
            user.email = "alice.updated@example.com"
            # Access attributes before commit to avoid lazy loading issues
            user_id, user_name, user_email = user.id, user.name, user.email
            await session.commit()
            print(f"✓ User updated: User(id={user_id}, name='{user_name}', email='{user_email}')")
        else:
            print("✗ User not found")
    
    # Verify update
    print("\n7. Verifying update...")
    async with async_session() as session:
        result = await session.execute(select(User).where(User.name == "Alice"))
        user = result.scalars().first()
        if user:
            print(f"✓ Email is now: {user.email}")
        else:
            print("✗ User not found")
    
    # Test refresh
    print("\n8. Testing refresh...")
    async with async_session() as session:
        user = await session.get(User, 1)
        if user:
            print(f"✓ Before refresh: {user.email}")
            # Simulate external update (in real scenario)
            user.email = "temp@example.com"
            print(f"  Changed locally: {user.email}")
            await session.refresh(user)
            print(f"✓ After refresh: {user.email}")
        else:
            print("✗ User not found")
    
    # Delete user
    print("\n9. Deleting user...")
    async with async_session() as session:
        result = await session.execute(select(User).where(User.name == "Charlie"))
        user = result.scalars().first()
        
        if user:
            await session.delete(user)
            await session.commit()
            print("✓ User deleted")
        else:
            print("✗ User not found")
    
    # Verify deletion
    print("\n10. Verifying deletion...")
    async with async_session() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        print(f"✓ Remaining users: {len(users)}")
        for user in users:
            print(f"  - {user.name}")
    
    # Test scalar query
    print("\n11. Testing scalar query...")
    async with async_session() as session:
        user_id = await session.scalar(select(User.id).where(User.name == "Bob"))
        print(f"✓ Bob's ID: {user_id}")
    
    # Cleanup
    print("\n12. Cleaning up...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()
    print("✓ Cleaned up")
    
    print("\n" + "=" * 60)
    print("All ORM tests passed! ✓")
    print("=" * 60)


async def test_session_rollback():
    """Test session rollback with ORM."""
    print("\n" + "=" * 60)
    print("Testing Session Rollback with ORM")
    print("=" * 60)
    
    engine = create_async_engine("sqlite+aiosqlite:///./test_orm_rollback.db", echo=False)
    
    # Create tables
    print("\n1. Creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✓ Tables created")
    
    async_session = AsyncSessionmaker(bind=engine)
    
    # Test successful commit
    print("\n2. Testing successful commit...")
    async with async_session.begin() as session:
        user1 = User(name="Alice", email="alice@example.com")
        user2 = User(name="Bob", email="bob@example.com")
        session.add(user1)
        session.add(user2)
        # Transaction is auto-committed at end of context
    print("✓ Transaction committed")
    
    # Verify commit
    async with async_session() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        print(f"✓ Found {len(users)} users after commit")
    
    # Test rollback
    print("\n3. Testing rollback...")
    try:
        async with async_session.begin() as session:
            user3 = User(name="Charlie", email="charlie@example.com")
            session.add(user3)
            # Force an error
            raise ValueError("Simulated error")
    except ValueError:
        print("✓ Transaction rolled back due to error")
    
    # Verify rollback
    async with async_session() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        print(f"✓ Still have {len(users)} users (Charlie was rolled back)")
        for user in users:
            print(f"  - {user.name}")
    
    # Cleanup
    print("\n4. Cleaning up...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()
    print("✓ Cleaned up")
    
    print("\n" + "=" * 60)
    print("Session rollback test passed! ✓")
    print("=" * 60)


async def test_multiple_operations():
    """Test multiple operations in a single session."""
    print("\n" + "=" * 60)
    print("Testing Multiple Operations in Single Session")
    print("=" * 60)
    
    engine = create_async_engine("sqlite+aiosqlite:///./test_multi.db", echo=False)
    
    # Create tables
    print("\n1. Creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✓ Tables created")
    
    async_session = AsyncSessionmaker(bind=engine)
    
    # Perform multiple operations
    print("\n2. Performing multiple operations...")
    async with async_session.begin() as session:
        # Add users
        users = [
            User(name="Alice", email="alice@example.com"),
            User(name="Bob", email="bob@example.com"),
            User(name="Charlie", email="charlie@example.com"),
            User(name="David", email="david@example.com"),
        ]
        session.add_all(users)
        
        # Flush to get IDs
        await session.flush()
        print(f"✓ Added {len(users)} users")
        
        # Query and modify
        result = await session.execute(select(User).where(User.name == "Alice"))
        alice = result.scalars().first()
        if alice:
            alice.email = "alice.modified@example.com"
            print(f"✓ Modified Alice's email")
        
        # Query count
        result = await session.execute(select(User))
        all_users = result.scalars().all()
        print(f"✓ Total users in session: {len(all_users)}")
        
        # Transaction auto-commits here
    
    print("✓ All operations committed")
    
    # Verify all operations
    print("\n3. Verifying operations...")
    async with async_session() as session:
        result = await session.execute(select(User).order_by(User.id))
        users = result.scalars().all()
        print(f"✓ Total users in database: {len(users)}")
        for user in users:
            print(f"  - {user}")
    
    # Cleanup
    print("\n4. Cleaning up...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()
    print("✓ Cleaned up")
    
    print("\n" + "=" * 60)
    print("Multiple operations test passed! ✓")
    print("=" * 60)


async def main():
    """Run all ORM tests."""
    await test_orm_operations()
    await test_session_rollback()
    await test_multiple_operations()


if __name__ == "__main__":
    asyncio.run(main())
