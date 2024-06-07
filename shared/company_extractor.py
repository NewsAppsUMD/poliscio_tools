import os
import json
import anthropic

client = anthropic.Anthropic(
    api_key=os.environ.get("CLAUDE_API_KEY")
)

def extract_info(text):
    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=4000,
        temperature=0,
        system=f"create only valid JSON objects based on the provided text. Never include any additional text or explanation. Always use double-quotes for every value. No yapping, no hallucinations.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Extract only company names contained in the following text into a valid JSON array: {text}. If no companies are found, return an empty array."
                    }
                ]
            }
        ]
    )
    return message.content[0].text