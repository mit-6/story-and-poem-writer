from langchain_groq import ChatGroq
from langchain import PromptTemplate, LLMChain
import pprint
from dotenv import load_dotenv
import os
import streamlit as st
import sqlite3

load_dotenv()
os.environ['GROQ_API_KEY']="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"

# Create a SQLite database
conn = sqlite3.connect('story_and_poem_generator.db')
cursor = conn.cursor()

# Create a table to store the output
cursor.execute('''
    CREATE TABLE IF NOT EXISTS output (
        id INTEGER PRIMARY KEY,
        question TEXT,
        response TEXT
    )
''')

st.title("Story and Poem Generator")
option = st.selectbox('select one', ('Story', 'Poem'))
question = st.text_input("Enter a question or topic for the story or poem:")

# prompt template
prompt = PromptTemplate(
    input_variables=["question", "story_or_poem"],
    template= """
    
        You are only write story and peom don't write any other things. based on user question.
        Poem Stucture:
            1. Title: The title should be a single line, centered on the page.
            2. Stanza 1: The first stanza should have 4 lines, with a rhyme scheme of AABB.
            3. Stanza 2: The second stanza should have 2 lines, with a rhyme scheme of CC.
        
        Story Stucture:
            1. Title: The title should be a single line, centered on the page.
            2. Paragraph 1: The first paragraph should introduce the main character and setting.
            3. Paragraph 2: The second paragraph should describe the main conflict or problem.
            4. Paragraph 3: The third paragraph should resolve the conflict or problem.
        
        Write a creative story or a poem on the theme of {question} based on user request {story_or_poem}.

        Note:
            1. If user say Story then you only write story.
            2. If user say Poem then you only write poem.
            3. Story write in 3 paragraph and poem write in 6 lines.
            4. Do not show any tags but use that tags in your output.

"""
)


if st.button("Generate"):
    # Initialize the ChatGroq client
    client = ChatGroq(model_name = 'llama-3.3-70b-versatile', temperature=0.6)
    
    chain = LLMChain(llm=client, prompt=prompt)
    
    response = chain.invoke({"question": question, "story_or_poem": option})
    
    # Save database
    cursor.execute('INSERT INTO output (question, response) VALUES (?, ?)', (question, response["text"]))
    conn.commit()
    
    # Display the response
    st.write(response["text"])
    st.success("Output saved to database!")