import asyncio
from connection import config
from agents import Agent, RunContextWrapper, Runner, function_tool
from pydantic import BaseModel


# Define Library Book Model
class LibraryBook(BaseModel):
    book_id: str
    book_title: str
    author_name: str
    is_available: bool


# 3. LIBRARY BOOK CONTEXT
library_book = LibraryBook(
    book_id="BOOK-123",
    book_title="Python Programming",
    author_name="John Smith",
    is_available=True
)


@function_tool
def library_book_details(wrapper: RunContextWrapper[LibraryBook]):
    book = wrapper.context
    return (
        f"📚 The book title is {book.book_title}\n"
        f"✍️ Author: {book.author_name}\n"
        f"🆔 Book ID: {book.book_id}\n"
        f"✅ Available: {'Yes' if book.is_available else 'No'}\n\n"
    )


personal_agent = Agent(
    name="Library Book Agent",
    instructions="You are a helpful library assistant. Always call the tool 'library_book_details' to provide book information.",
    tools=[library_book_details]
)


async def main():
    result = await Runner.run(
        personal_agent,
        "Please provide the Library book details.",
        run_config=config,
        context=library_book   # ✅ FIX: pass instance, not class
    )
    print(result.final_output)


if __name__ == "__main__":   
    asyncio.run(main())





