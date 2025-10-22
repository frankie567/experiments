"""
Demonstration of standard SQLAlchemy asyncio usage (for comparison).

This shows how SQLAlchemy's built-in asyncio extension works.
"""

import asyncio
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(100))


async def standard_sqlalchemy_demo():
    """Demonstrate standard SQLAlchemy asyncio usage."""
    print("=== Standard SQLAlchemy AsyncIO (with greenlet) ===\n")
    
    # Create async engine
    engine = create_async_engine(
        "sqlite+aiosqlite:///standard_demo.db",
        echo=True,
    )
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create async session
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    # Insert data
    async with async_session() as session:
        async with session.begin():
            user1 = User(name="Alice", email="alice@example.com")
            user2 = User(name="Bob", email="bob@example.com")
            session.add(user1)
            session.add(user2)
    
    # Query data
    async with async_session() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        
        print("\nUsers found:")
        for user in users:
            print(f"  - {user.name} ({user.email})")
    
    # Cleanup
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(standard_sqlalchemy_demo())
