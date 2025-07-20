import openai
import requests
from openai import OpenAI

# --- Configuration ---
import data_info

openai.api_key = data_info.open_ai_key

# API Key for RapidAPI (IMDB API)
RAPIDAPI_KEY = '766ea387a6msh84ff46479ed9b4bp18b495jsna547d73e1ef5'
IMDB_API_URL = "https://imdb236.p.rapidapi.com/api/imdb/autocomplete"

def call_imdb_api(movie_title):
    headers = {
        'x-rapidapi-host': 'imdb236.p.rapidapi.com',
        'x-rapidapi-key': RAPIDAPI_KEY
    }
    params = {'query': movie_title}

    response = requests.get(IMDB_API_URL, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return "Sorry, couldn't retrieve movie information."


def gpt4o_mini_super_agent(user_input):
    # Step 1: Decide what tool to use
    tool_selection_prompt = f"""You are an assistant with access to movie APIs:

        If the user asks about a movie, respond exactly:
        "CALL_MOVIE_API: <movie-title>"

        Otherwise, answer normally.

        User input: "{user_input}"
        """

    client = OpenAI(api_key=data_info.open_ai_key)
    response = client.responses.create(
        model="gpt-4o-mini",
        input=tool_selection_prompt,
        temperature=0,
    )
    assistant_reply = response.output_text
    print(f"[Assistant Thought] {assistant_reply}")

    if assistant_reply.startswith("CALL_MOVIE_API:"):
        movie_title = assistant_reply.replace("CALL_MOVIE_API:", "").strip()
        api_result = call_imdb_api(movie_title)  # Call the new IMDB API
        final_prompt = f"The movie information about {movie_title} is: {api_result}. Please create a friendly response."

    else:
        # No tool call needed, just reply normally
        return assistant_reply

    # Step 3: Final polish from GPT
    final_response = openai.responses.create(
        model="gpt-4o-mini",
        input=final_prompt,
        temperature=0.1
    )

    final_answer = final_response.output_text
    return final_answer


# --- Main ---

if __name__ == "__main__":
    print("Ask me about movies!")
    while True:
        user_question = input("\nYou: ")
        if user_question.lower() in ['exit', 'quit']:
            break
        answer = gpt4o_mini_super_agent(user_question)
        print("\n[Answer]")
        print(answer)
