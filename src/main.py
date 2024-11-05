from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_openai import AzureChatOpenAI
from src.third_party import scrape_linkedin_profile
from langchain_core.output_parsers import StrOutputParser
from flask import Flask, request
import markdown

summary_template = """
    Given the information {information} about a personm I want you create:
    1. a short summary
    2. two interesting part about the summary
    """
summary_prompt_template = PromptTemplate(
    input_variables="information",
    template=summary_template
)

output_parser = StrOutputParser()

llm = AzureChatOpenAI(
    azure_deployment="gpt-4",
    api_version="2024-08-01-preview"
)

chain = summary_prompt_template | llm | output_parser
app = Flask(__name__)

@app.route("/health_check")
def health_check():
    return "OK"

@app.route("/")
def main():
    linkedin_url = request.args.get('linkedin-url')

    if linkedin_url is not None:
        scrape_param = {
            "linkedin_url": linkedin_url,
            "mock": False
        }
    else:
        scrape_param = {
            "mock": True
        }

    linkedin_json_str = scrape_linkedin_profile(**scrape_param)
    print(f"request llm using linkedin_json:")
    print(linkedin_json_str)
    result = chain.invoke(
        input={"information": linkedin_json_str}
    )
    return markdown.markdown(result)  


if __name__ == "__main__":
    main()
