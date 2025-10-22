"""
Advanced example: Handling sync operations without greenlet.

This demonstrates how to integrate sync SQLAlchemy operations (like metadata
operations, complex ORM patterns) using anyio's to_thread functionality
instead of greenlet.
"""

import anyio
from sqlalchemy import Column, Integer, String, ForeignKey, select
from sqlalchemy.orm import declarative_base, relationship, Session
from sqlalchemy.ext.asyncio import create_async_engine

from anyio_engine import AnyIOAsyncEngine, AnyIOAsyncSession

Base = declarative_base()


class Author(Base):
    __tablename__ = "authors"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship("Author", back_populates="books")


async def advanced_demo():
    """
    Demonstrate advanced patterns without greenlet.
    
    Shows how to:
    1. Use anyio.to_thread for truly sync operations
    2. Handle complex ORM relationships
    3. Perform bulk operations
    """
    print("=== Advanced SQLAlchemy with AnyIO ===\n")
    
    async with AnyIOAsyncEngine(
        "sqlite+aiosqlite:///advanced_demo.db",
        echo=False,
    ) as engine:
        
        # Create tables using run_sync (this is still supported)
        print("Creating tables...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        
        session_factory = engine.session_maker()
        
        # Insert data with relationships
        print("Inserting authors and books...")
        async with AnyIOAsyncSession(session_factory) as session:
            async with session.begin():
                # Create authors
                author1 = Author(name="Isaac Asimov")
                author2 = Author(name="Arthur C. Clarke")
                
                # Create books
                book1 = Book(title="Foundation", author=author1)
                book2 = Book(title="I, Robot", author=author1)
                book3 = Book(title="2001: A Space Odyssey", author=author2)
                book4 = Book(title="Rendezvous with Rama", author=author2)
                
                session.add_all([author1, author2, book1, book2, book3, book4])
        
        # Query with relationships
        print("\nQuerying authors with their books...")
        async with AnyIOAsyncSession(session_factory) as session:
            result = await session.execute(
                select(Author).order_by(Author.name)
            )
            authors = result.scalars().all()
            
            for author in authors:
                # Eagerly load books
                await session.refresh(author, ["books"])
                print(f"\n{author.name}:")
                for book in author.books:
                    print(f"  - {book.title}")
        
        # Bulk operations using anyio task groups
        print("\n\nPerforming concurrent bulk queries...")
        
        async def get_books_by_author(author_name: str):
            """Get all books by an author."""
            async with AnyIOAsyncSession(session_factory) as session:
                result = await session.execute(
                    select(Book)
                    .join(Author)
                    .where(Author.name == author_name)
                )
                return result.scalars().all()
        
        # Query multiple authors concurrently
        results = {}
        async with anyio.create_task_group() as tg:
            async def query_asimov():
                books = await get_books_by_author("Isaac Asimov")
                results["asimov"] = books
            
            async def query_clarke():
                books = await get_books_by_author("Arthur C. Clarke")
                results["clarke"] = books
            
            tg.start_soon(query_asimov)
            tg.start_soon(query_clarke)
        
        print("\nConcurrent query results:")
        print(f"Asimov books: {[book.title for book in results['asimov']]}")
        print(f"Clarke books: {[book.title for book in results['clarke']]}")
        
        # Demonstrate error handling with task groups
        print("\n\nDemonstrating structured error handling...")
        
        async def failing_query():
            """A query that will fail."""
            async with AnyIOAsyncSession(session_factory) as session:
                # This will fail because we're querying a non-existent column
                await session.execute(select(Author).where(Author.id == 999))
                raise ValueError("Simulated error")
        
        async def successful_query():
            """A query that will succeed."""
            async with AnyIOAsyncSession(session_factory) as session:
                result = await session.execute(select(Author).limit(1))
                return result.scalar_one_or_none()
        
        try:
            async with anyio.create_task_group() as tg:
                tg.start_soon(failing_query)
                tg.start_soon(successful_query)
        except Exception as e:
            print(f"Task group caught exception: {type(e).__name__}: {e}")
            print("All tasks were cancelled properly (structured concurrency)")


async def show_sync_compatibility():
    """
    Show how to handle truly synchronous operations using anyio.to_thread.
    
    This is useful for sync-only libraries or CPU-bound operations.
    """
    print("\n\n=== Handling Sync Operations with anyio.to_thread ===\n")
    
    def sync_heavy_computation(n: int) -> int:
        """Simulate a CPU-bound sync operation."""
        total = 0
        for i in range(n):
            total += i * i
        return total
    
    # Run sync operations in thread pool
    print("Running sync operations in thread pool...")
    result = await anyio.to_thread.run_sync(sync_heavy_computation, 1000000)
    print(f"Result: {result}")
    
    print("""
Key Point: With anyio.to_thread.run_sync, we can run truly synchronous
operations without greenlet. This is useful for:
- CPU-bound operations
- Sync-only libraries
- Operations that can't be async

The difference from greenlet:
- greenlet: Cooperative context switching within the same thread
- anyio.to_thread: Actual thread pool execution
- Both achieve async compatibility, but anyio.to_thread is simpler
  and doesn't require greenlet's complex context switching
    """)


if __name__ == "__main__":
    anyio.run(advanced_demo)
    anyio.run(show_sync_compatibility)
