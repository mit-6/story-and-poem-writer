from fastapi import FastAPI, Request
from langchain_groq import ChatGroq
from langchain import PromptTemplate, LLMChain
import pprint
from dotenv import load_dotenv
import os

load_dotenv()
os.environ['GROQ_API_KEY']="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"

app = FastAPI()

@app.get("/story_and_poem_generator")
async def story_and_poem_generator(question: str):
    # Create a prompt template
    prompt = PromptTemplate(
        input_variables=["question"],
        template= """

        The story should be short and simple. The poem should be short and simple.
        You are only write story and peom don't write any other things.
        Poem Stucture:
            1. Title: The title should be a single line, centered on the page.
            2. Stanza 1: The first stanza should have 4 lines, with a rhyme scheme of AABB.
        
        Story Stucture:
            1. Title: The title should be a single line, centered on the page.
            2. Paragraph 1: The first paragraph should introduce the main character and setting.
            3. Paragraph 2: The second paragraph should describe the main conflict or problem.
            4. Paragraph 3: The third paragraph should resolve the conflict or problem.
        
        Write a creative story or a poem on the theme of {question} based on user question.

        Note:
            1. If user say Story then you only write story.
            2. If user say Poem then you only write poem.
            3. Story write in 3 paragraph and poem write in 6 lines.


"""
    )

    # ChatGroq
    client = ChatGroq(model_name = 'llama-3.3-70b-versatile', temperature=0.6)

    chain = LLMChain(llm=client, prompt=prompt)

    response = chain.invoke({"question": question})

    # Return the response
    return {"response": response}