# pip install openai requests
import openai
from openai import OpenAI
# Configure OpenAI API key
import data_info
from txt2sql import generate_sql, run_sql

openai.api_key = data_info.open_ai_key

def gpt4o_mini_agent(user_input):
    schema_description = """
        Table: customers
        - id (integer)
        - name (text)
        - email (text)
        - signup_date (date)
        """
    # First, let our Agent decide what to do
    # This agent will check the intent of the user
    intent_identification_prompt = f"""
    ### Role: You are an intelligent assistant with access to following database schema to answer user query. 
    ### Database Schema:
    {schema_description}
    
    ### User Query:
    {user_input}
    
    ### Task: Your task is to identify if the User Query can be answered using the database schema you have available.
 
    ### Output format: If the user query can be answered with the database schema. 
                       return response as "CALL_TXT2SQL_API" else return "No".
    """

    client = OpenAI(api_key=data_info.open_ai_key)
    response = client.responses.create(
        model="gpt-4o-mini",
        input=intent_identification_prompt,
        temperature=0,
    )
    assistant_reply = response.output_text
    print(f"[Assistant Thought] {assistant_reply}")
    # If GPT indicates to call the API
    if assistant_reply.find("CALL_TXT2SQL_API") != -1:
        sql_query = generate_sql(user_input)
        print(sql_query)
        final_answer = run_sql(sql_query)
        print(final_answer)
        return final_answer
    else:
        return assistant_reply


# Example usage
# user_input = input("Ask me something: ")
user_input ="show me customer name who signed up in 2025"

gpt4o_mini_agent(user_input)


