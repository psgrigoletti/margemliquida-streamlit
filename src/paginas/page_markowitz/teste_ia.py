import os

from openai import OpenAI

# OPENAI_API_KEY = "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"

client = OpenAI(
    # This is the default and can be omitted
    api_key="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"
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="gpt-3.5-turbo",
)
