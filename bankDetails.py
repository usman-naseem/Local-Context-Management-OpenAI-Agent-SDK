import asyncio
from connection import config
from agents import Agent, RunContextWrapper, Runner, function_tool
from pydantic import BaseModel

# Define Bank Account Model
class BankAccount(BaseModel):
    account_number: str
    customer_name: str
    account_balance: float
    account_type: str

# Create Bank Account Instance
bank_account = BankAccount(
    account_number="ACC-3456456",
    customer_name="Muhammad Usman",
    account_balance=80000.50,
    account_type="savings"
)

# Dynamic instruction for LLM
def dynamic_ins(wrapper: RunContextWrapper[BankAccount], agent: Agent[BankAccount]) -> str:
    return (
        "You are a professional customer service assistant for the bank. "
        "When prompted, call the tool 'customer_bank_account_details' to fetch details. "
        "Then, provide a clear and polite explanation of the customer’s bank account information."
    )

# Function tool that formats account details
@function_tool
def customer_bank_account_details(wrapper: RunContextWrapper[BankAccount]) -> str:
    acc = wrapper.context
    return (
        f"Here are the details of the customer’s bank account:\n\n"
        f"👤 Customer Name: {acc.customer_name}\n"
        f"🏦 Account Number: {acc.account_number}\n"
        f"💰 Account Balance: PKR {acc.account_balance:,.2f}\n"
        f"📂 Account Type: {acc.account_type.capitalize()} Account\n\n"
       
    )

# Agent setup
customer_bankaccount_agent = Agent[BankAccount](
    name="Customer Bank Account Agent",
    instructions=dynamic_ins,
    tools=[customer_bank_account_details]
)

# Runner
async def main():
    result = await Runner.run(
        customer_bankaccount_agent,
        "Please provide the customer bank account details.",
        run_config=config,
        context=bank_account
    )
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())




