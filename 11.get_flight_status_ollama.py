import openai
import requests
import data_info
import ollama
model = "gemma3:1b"
# Aviationstack API Key
AVIATIONSTACK_API_KEY = "56420807c490bd835b6e922d2b983fbb"
AVIATIONSTACK_URL = "http://api.aviationstack.com/v1/flights"

def call_flight_status_api(flight_number):
    params = {
        'access_key': AVIATIONSTACK_API_KEY,
        'flight_iata': flight_number
    }
    response = requests.get(AVIATIONSTACK_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get('data'):
            flight_info = data['data'][0]
            status = flight_info['flight_status']
            departure = flight_info['departure']['airport']
            arrival = flight_info['arrival']['airport']
            return f"Flight {flight_number} is currently {status}. Departure: {departure}, Arrival: {arrival}."
        else:
            return "Sorry, couldn't find information for that flight."
    else:
        return "Sorry, couldn't retrieve flight data."

def gpt4o_mini_flight_agent(user_input):
    prompt = f"""You are an assistant with access to a flight status API.

If the user asks about the status of a flight, respond exactly:
"CALL_FLIGHT_API: <flight-number>"

Otherwise, answer normally.

User input: "{user_input}"
"""

    prompt_tweak = f"""You are an assistant with access to a flight status API.

    If the user asks about the status of a flight, respond exactly:
    "CALL_FLIGHT_API: <flight-number>"
    If the flight number is not provided by user then try to assess it using the information provided and put it in <flight-number>. 
    do not add any statement or comment apart from flight-number value
    in
    Otherwise, answer normally.

    User input: "{user_input}"
    """

    response = ollama.generate(model=model, prompt=prompt)

    assistant_reply = response.response

    print(f"[Assistant Thought] {assistant_reply}")

    if assistant_reply.startswith("CALL_FLIGHT_API:"):
        flight_number = assistant_reply.replace("CALL_FLIGHT_API:", "").strip()
        api_result = call_flight_status_api(flight_number)
        final_prompt = f"The flight status information is: {api_result}. Please compose a friendly detailed reply."
    else:
        return assistant_reply

    final_response = ollama.generate(model=model, prompt=final_prompt)

    assistant_reply = final_response.response

    return assistant_reply

# Example usage
# UA2402
user_question = input("Ask me about a flight: ")
answer = gpt4o_mini_flight_agent(user_question)
print("\n[Final Answer]")
print(answer)
