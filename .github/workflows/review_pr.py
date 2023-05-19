from github import Github
import os
import openai

def call_open_ai(patch):
    openai.api_key = os.environ["OPENAI_API_KEY"]
    openai.api_base = os.environ["OPENAI_API_ENDPOINT"]
    openai.api_type = os.environ["OPENAI_API_TYPE"]
    openai.api_version = os.environ["OPENAI_API_VERSION"]

    response = openai.ChatCompletion.create(
        engine=os.getenv("AZURE_MODEL"), # engine = "deployment_name".
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0,
        messages=[
            {"role": "system", "content": "Please act as a code reviewer and review code in three steps: \
              1. Give an overall score for the current modification according to a 10-point scale; \
             2. Provide a brief explanation for the score; 3. Suggest what the author should do next."},
            {"role": "user", "content": f"Please review the following code patch: {patch}"}
        ]
    )
    return response.choices[0].message.content

def review_changes():
    g = Github(os.environ["GITHUB_TOKEN"])
    repo = g.get_repo(os.environ["GITHUB_REPOSITORY"]) 
    pr = repo.get_pull(int(os.environ["PR_NUMBER"])) 
    files = pr.get_files()
    last_commit = pr.get_commits().reversed[0]
    for file in files:
        if file.status != "modified" and file.status != "added":
            continue
        patch = file.patch
        comment = call_open_ai(patch)
        pr.create_review_comment(
                body=comment,
                commit_id=last_commit,
                path=file.filename,
                position=len(patch.split("\n"))-1,  
            )

if __name__ == '__main__':
    review_changes()
