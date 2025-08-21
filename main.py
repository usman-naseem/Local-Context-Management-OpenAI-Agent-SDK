from pydantic import BaseModel
import asyncio
from connection import config
from agents import Agent, RunContextWrapper, Runner, function_tool
from pydantic import BaseModel
import rich



# Define a simple user context model

class UserInfo(BaseModel):
    id: int
    name:str

user=UserInfo(id=231 ,name="Usman") 


@function_tool
def user_context_wrapper(wrapper: RunContextWrapper[UserInfo]):
    return wrapper.context


personal_agent=Agent(
    name="Personal Agent",
    instructions="You are helpful assitant always get the tools call to get user information ",
    tools=[user_context_wrapper]
)
async def main():
    result= await Runner.run(
        personal_agent,
        "What is my name?",
        run_config=config,
        context=user,  # Local Context
     
    

    )
    rich.print(result.final_output)



if __name__=="__main__":
    asyncio.run(main())


    