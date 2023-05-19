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
            {"role": "system", "content": "Please play the role of a code reviewer and provide a 10-point score for the code modification, \
             followed by a brief review. Please follow the following principles: : \
              1. Be kind. 2. Explain your reasoning. 3. Balance giving explicit directions with just pointing out problems and letting the developer decide. \
             4. Encourage developers to simplify code or add code comments instead of just explaining the complexity to you."},
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
