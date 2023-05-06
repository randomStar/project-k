import openai
import os
import sys
import requests

def generate_comment(pr_url):
    pr_patch = requests.get(f"{pr_url}.patch")
    content = pr_patch.text
    openai.api_key = os.environ["OPENAI_API_KEY"]

    model_engine = "gpt-3.5-turbo"
    prompt = (f"Please act as a code reviewer and review the changes made in the following patch format pull request: {content}. ")
    messages=[{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=messages,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=1,
    )

    comment = response.choices[0].message.content
    print(f"comment by openai: {comment}")
    return comment

if __name__ == '__main__':
    generate_comment(sys.argv[1:])
