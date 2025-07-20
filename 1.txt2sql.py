import openai
from openai import OpenAI
import sqlite3
import data_info
import re
import json
openai.api_key = data_info.open_ai_key

def setupdb():
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()

    # Create table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        signup_date DATE
    )
    """)

    # Insert some sample data
    cursor.executemany("""
    INSERT INTO customers (id,name, email, signup_date)
    VALUES (?,?, ?, ?)
    """, [
        (1, "Alice Johnson", "alice@example.com", "2025-06-15"),
        (2, "Bob Smith", "bob@example.com", "2024-07-01"),
        (3, "Clara White", "clara@example.com", "2024-07-10")
    ])

    conn.commit()
    conn.close()
def generate_sql(question: str) -> str:
    schema_description = """
    Table: customers
    - id (integer)
    - name (text)
    - email (text)
    - signup_date (date)
    """

    final_prompt = f"""
    ### You are an expert SQL query writer. Who translates user requirements into sql queries. I have given you database schema.
    Use this database schema to generate sql queries. 
     
    ### Database Schema:
    {schema_description}
    
    ### Question:
    {question}
    
    ### Output format: The output format should be json object with 'SQL' and value as  generated sql query      
          "SQL": "..."
            
    """

    client = OpenAI(api_key=data_info.open_ai_key)
    response = client.responses.create(
            model="gpt-4o-mini",
            input=final_prompt,
            temperature=0,
        )

    sql_query = response.output_text
    match = re.search(r"```json\s*(\{.*?\})\s*```", sql_query, re.DOTALL)
    if not match:
        raise ValueError("No JSON code block found.")
    json_str = match.group(1)

    # Step 2: Parse JSON and extract the SQL
    data = json.loads(json_str)
    sql_query = data.get("SQL")
    return sql_query

def run_sql(query: str):
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        print("\n Results:")
        print(columns)
        for row in rows:
            print(row)
    except Exception as e:
        print(" Error executing SQL:", e)
    finally:
        conn.close()


if __name__ == "__main__":
    # Setup database first time when you run the program. Post that comment it
    setupdb()
    # Sample question: show me customer name who signed up in 2025
    # Sample question: show me the details of customer  who signed up in 2025
    question = input("Enter your natural language question: ")
    # Generate SQL query for user question
    sql_query = generate_sql(question)
    print("=======Generated SQL:========")
    print(sql_query)
    # Execute the SQL query
    run_sql(sql_query)

