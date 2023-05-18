from github import Github
import os
import openai


openai.api_key = os.environ["OPENAI_API_KEY"]
openai.endpoint = os.environ["OPENAI_API_ENDPOINT"]
openai.api_type = os.environ["OPENAI_API_TYPE"]
openai.api_version =os.environ["OPENAI_API_VERSION"]

def call_open_ai(patch):
    response = openai.ChatCompletion.create(
        engine="gpt-35-turbo-0301", # engine = "deployment_name".
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0,
        messages=[
            {"role": "system", "content": "You are a code reviewer."},
            {"role": "user", "content": f"Please do a simple review on the following code patch: {patch}"}
        ]
    )
    return response.choices[0].message.content

def review_changes():
    g = Github(os.environ["GITHUB_TOKEN"])
    repo = g.get_repo(os.environ["GITHUB_REPOSITORY"]) 
    pr = repo.get_pull(os.environ["PR_NUMBER"]) 
    files = pr.get_files()
    last_commit = pr.get_commits().reversed[0]
    for file in files:
        patch = file.patch
        print(file.filename)
        comment = call_open_ai(patch)
        pr.create_review_comment(
                body=comment,
                commit_id=last_commit,
                path=file.filename,
                position=len(patch.split("\n"))-1,  
            )

if __name__ == '__main__':
    review_changes()
