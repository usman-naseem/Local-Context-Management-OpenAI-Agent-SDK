import asyncio
from connection import config
from agents import Agent, RunContextWrapper, Runner, function_tool
from pydantic import BaseModel


# Define Student Profile Model
class StudentProfile(BaseModel):
    student_id: str
    student_name: str
    current_quarter: int|str
    total_courses: int |str

student = StudentProfile(
    student_id="GIAIC-49455",
    student_name="Muhammad Usman",
    current_quarter="Quarter 4",
    total_courses= 8
)
# Dynamic instruction for LLM
def dynamic_instruction(wrapper: RunContextWrapper[StudentProfile], agent: Agent[StudentProfile]) -> str:
    return (
        "When prompted, call the tool 'student_profile_details' to fetch details. "
        "Then, provide a clear and polite explanation of the student’s profile information."
    )

# Function tool that formats student profile details
@function_tool
def student_profile_details(wrapper: RunContextWrapper[StudentProfile]) -> str:
    profile = wrapper.context
    return (
        f"Here are the details of the student profile:\n\n"
        f"👨‍🎓 Student Name: {profile.student_name}\n"
        f"📚 Student ID: {profile.student_id}\n"

        f"📅 Current Quarter: {profile.current_quarter}\n"
        f"📖 Total Courses: {profile.total_courses}\n\n"
    )


# Agent setup
student_profile_agent = Agent[StudentProfile](
    name="Student Profile Agent",
    instructions=dynamic_instruction,
    tools=[student_profile_details]
)
# Runner
async def main():
    result = await Runner.run(
        student_profile_agent,
        "Please provide the student profile details.",
        run_config=config,

        context=student
    )
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
