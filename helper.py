from langchain_core.prompts import PromptTemplate
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

def get_data(summary, story_points):

    class feedback(BaseModel):
        summary: str = Field(..., description="Summary of the title")
        description: str = Field(..., description="Description of the title")
        acceptance_criteria: str = Field(..., description="Acceptance criteria of the title")

    parser = PydanticOutputParser(pydantic_object=feedback)


    prompt = PromptTemplate(
    template="""
    You are a helpful assistant that is going to provide useful and professional answers only.

    Based on the title of the Jira issue, give me a :
    Suitable summary of the Jira issue in around 5-10 words (DO NOT GIVE THE OUTPUT IN MORE THAN 10 WORDS)
    Suitable description which tells what will be done in the issue, and this should be in around 40-50 words (DO NOT GIVE THE OUTPUT IN LESS THAN 40 WORDS)
    Suitable acceptance criteria which tells what is expected from the issue, and this should be around 20-30 words (DO NOT GIVE THE OUTPUT IN LESS THAN 20 WORDS)

    title: {summary}

    Respond ONLY with valid JSON in this format:
        {format_instruction}
        """,

    input_variables = ['summary'],
    partial_variables={'format_instruction':parser.get_format_instructions()}
    )

    repo_id = 'mistralai/Mistral-7B-Instruct-v0.3'

    from langchain_huggingface import ChatHuggingFace

    llm = HuggingFaceEndpoint(repo_id=repo_id, temperature=0.7)
    model = ChatHuggingFace(llm=llm)

    chain = prompt | model | parser

    result = chain.invoke({'summary':summary})
    summary = result.summary
    description = result.description
    ac = result.acceptance_criteria


    return(summary,description,ac)