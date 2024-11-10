from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor
)
from langchain import hub
from langchain_openai import AzureChatOpenAI
from src.third_party.tavily_search import get_profile_url_tavily
load_dotenv()


def lookup(name: str) -> str:
    llm = AzureChatOpenAI(
        azure_deployment="gpt-4o-mini",
        api_version="2024-02-15-preview",
        temperature=0
    )
    template = """
    given the full name {name_of_person} I want you to give me a link to the linkedin profile page. 
    Your ansewr should contain only a URL
    """
    prompt_template = PromptTemplate(template=template,
                                     input_variables=["name_of_person"])
    tools_for_agent = [
        Tool(name="Crawl Google for linkedin profile page",
             func=get_profile_url_tavily,
             description="Useful when you need to get the URL of linkedin")
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm,
                               tools=tools_for_agent,
                               prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent,
                                   tools=tools_for_agent,
                                   verbose=True)

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )
    linkedin_profile_url = result["output"]
    return linkedin_profile_url


if __name__ == "__main__":
    lookup("chingclee")
