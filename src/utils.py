import json
from litellm import completion
from datetime import datetime


def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")

def invoke_llm(system_prompt, user_message, model, response_format=None, json_output=False):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]
    response = completion(
        model=model,
        messages=messages,
        temperature=0.1,
        response_format=response_format
    )
    output = response.choices[0].message.content
    structured_output = json.loads(output)
    
    if json_output:
        return structured_output
    return response_format(**structured_output)