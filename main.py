import os
import types
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import MAX_ITERS
from functions.call_function import call_function, available_functions
from prompts import system_prompt

def main():
    global WORKING_DIR
    arguments = sys.argv  # "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)
    # WORKING_DIR = input(f"Set working Director\n") or "./"
    prompt = input(f"Enter a prompt:\n")
    verbose = True if "--verbose" in arguments else False


    messages = [types.Content(role="user", parts=[types.Part(text=prompt)]), ]
    iters = 0
    while True:
        iters += 1
        if iters > MAX_ITERS:
            print(f"Maximum iterations reached. Exiting.")
            sys.exit(1)

        try:
            finale_response = generate_content(client, messages, verbose)
            if finale_response:
                print("Final response:")
                print(finale_response)
                break

        except Exception as e:
            print(f"Error: {e}")


def generate_content(client,messages,verbose):
    response = client.models.generate_content(model="gemini-2.0-flash-001",
                                              contents=messages,
                                              config=types.GenerateContentConfig(
                                                  tools=[available_functions],
                                                  system_instruction=system_prompt), )
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            messages.append(function_call_content)

    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception( "empty function call result")

        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")

        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")

    messages.append(types.Content(role="user", parts=function_responses))

if __name__ == "__main__":
    main()
