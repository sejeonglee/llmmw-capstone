import openai

with open("openai_key.txt", encoding="utf8", mode="r") as apikeyfile:
    openai.api_key = apikeyfile.read()


def generate_response(prompt: str):
    """
    (OpenAI ChatGPT) Generate response from prompt

    Args:
        prompt (str): Prompt to generate response from

    Returns:
        str: Generated response"""
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )
    return completion.choices[0].text
