"""
Demonstration of SQLAlchemy with anyio instead of direct asyncio.

This shows how to use SQLAlchemy's async features with anyio,
providing a greenlet-free alternative that works with both asyncio and trio.
"""

import anyio
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.orm import declarative_base

from anyio_engine import AnyIOAsyncEngine, AnyIOAsyncSession

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(100))


async def anyio_demo():
    """Demonstrate SQLAlchemy with anyio."""
    print("=== SQLAlchemy with AnyIO (greenlet-free) ===\n")
    
    # Create anyio-wrapped async engine
    async with AnyIOAsyncEngine(
        "sqlite+aiosqlite:///anyio_demo.db",
        echo=True,
    ) as engine:
        
        # Create tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        # Create session factory
        session_factory = engine.session_maker()
        
        # Insert data
        print("\n--- Inserting data ---")
        async with AnyIOAsyncSession(session_factory) as session:
            async with session.begin():
                user1 = User(name="Charlie", email="charlie@example.com")
                user2 = User(name="Diana", email="diana@example.com")
                session.add(user1)
                session.add(user2)
        
        # Query data
        print("\n--- Querying data ---")
        async with AnyIOAsyncSession(session_factory) as session:
            result = await session.execute(select(User))
            users = result.scalars().all()
            
            print("\nUsers found:")
            for user in users:
                print(f"  - {user.name} ({user.email})")
        
        # Demonstrate anyio task group for concurrent queries
        print("\n--- Concurrent queries with anyio ---")
        
        async def get_user_by_name(session, name):
            """Query helper."""
            result = await session.execute(
                select(User).where(User.name == name)
            )
            return result.scalar_one_or_none()
        
        # Execute multiple queries concurrently using anyio's task group
        async with anyio.create_task_group() as tg:
            results = {}
            
            async def query_charlie():
                async with AnyIOAsyncSession(session_factory) as session:
                    user = await get_user_by_name(session, "Charlie")
                    results["charlie"] = user
            
            async def query_diana():
                async with AnyIOAsyncSession(session_factory) as session:
                    user = await get_user_by_name(session, "Diana")
                    results["diana"] = user
            
            tg.start_soon(query_charlie)
            tg.start_soon(query_diana)
        
        print("\nConcurrent query results:")
        if results.get("charlie"):
            print(f"  - Charlie: {results['charlie'].email}")
        if results.get("diana"):
            print(f"  - Diana: {results['diana'].email}")


async def compare_with_standard():
    """
    Show that our anyio implementation works the same as standard SQLAlchemy asyncio.
    """
    print("\n" + "="*60)
    print("Comparison: Both implementations use the same async drivers")
    print("="*60)
    print("""
Key Insights:
1. SQLAlchemy's async extension already uses async drivers (aiosqlite, asyncpg, etc.)
2. Greenlet is used primarily for backwards compatibility with sync ORM patterns
3. With anyio, we can use the same async drivers but with backend-agnostic primitives
4. anyio provides structured concurrency (task groups) and works with asyncio & trio
5. This approach is ready for Python 3.14+ free-threading

Benefits of anyio approach:
- No greenlet dependency (simpler, potentially more compatible with free-threading)
- Backend agnostic (works with asyncio, trio, etc.)
- Structured concurrency with task groups
- Cleaner async/await patterns throughout
    """)


if __name__ == "__main__":
    # anyio.run works with both asyncio and trio backends
    anyio.run(anyio_demo)
    anyio.run(compare_with_standard)
