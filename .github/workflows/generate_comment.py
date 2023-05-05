import openai
import os
import sys

def generate_comment(pr_url):
    openai.api_key = os.environ["OPENAI_API_KEY"]

    model_engine = "gpt-3.5-turbo"
    prompt = (f"Please review the changes made in this pull request: {pr_url}. "
              "What is good about this pull request? What needs improvement?")

    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )

    comment = response.choices[0].text.strip()
    return comment

if __name__ == '__main__':
    generate_comment(sys.argv[1:])
