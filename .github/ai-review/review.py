import json
import os
import requests
from pathlib import Path

from matplotlib import lines
from openai import OpenAI

OPENAI_MODEL="gpt-5.6-luna"
OPEN_API_KEY= os.environ["OPENAI_API_KEY"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
GITHUB_REPOSITORY = os.environ["GITHUB_REPOSITORY"]
PR_NUMBER=os.environ["PR_NUMBER"]
GITHUB_API="https://api.github.com"

openai_client=OpenAI(api_key=OPEN_API_KEY)

github_headers={
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "X-Github-Api-Version": "2022-11-28",
}

def get_pull_request():
    url=f"{GITHUB_API}/repos/{GITHUB_REPOSITORY}/pulls/{PR_NUMBER}"
    response=requests.get(url,headers=github_headers,timeout=30,)

    response.raise_for_status()
    return response.json()

def get_pull_request_diff():
    url=f"{GITHUB_API}/repos/{GITHUB_REPOSITORY}/pulls/{PR_NUMBER}"
    headers={**github_headers,"Accept": "application/vnd.github.v3+json"}
    response=requests.get(url,headers=headers,timeout=60,)
    response.raise_for_status()
    return response.json()

def load_review_rules():
    rules_file=(Path(__file__).parent / "review-rules.md")
    if not rules_file.exists():
        return """Use Standard software engineering bet practices. Focus on meaningful problems rather than style preferences"""

    return rules_file.read_text(encoding="utf-8")

def limit_diff(diff,max_characters=120000):
    if len(diff) <= max_characters:
        return diff
    print(f"Diff is {len(diff)} characters.")
    print(f"Limiting diff to {max_characters} characters.")

    return diff[:max_characters]+ "\n\n[DIFF TRUNCATED]"

def review_with_ai(pull_request,diff,review_rules):
    system_prompt="""You are a senior software engineer performing
an automated pull request review.

Your job is to identify meaningful problems
introduced by the pull request.

Review for:

1. Bugs
2. Incorrect logic
3. Security vulnerabilities
4. Performance problems
5. Error handling problems
6. Maintainability problems
7. Breaking changes
8. Missing important tests
9. Problems with edge cases
10. Problems where implementation does not
   match the PR description

Do NOT report:
- Personal coding style preferences
- Minor formatting issues
- Trivial naming preferences
- Issues unrelated to the changed code
- Speculative problems without reasonable evidence

Only report actionable issues.

The human TL/repository owner makes
the final decision.

Return JSON only.
"""
    user_prompt=f"""Review this Github pull request.
                 Repository: {GITHUB_REPOSITORY} Pull Request: #{pull_request} PR title: {pull_request.get('title',"")}
                 PR description: {pull_request.get('body',"")} Author: {pull_request.get('user',{}).get('login',"")}
                 {review_rules} {diff} 
                  Return exactly this JSON structure:
                   {{
                      "overall":"PASS,
                       "summary":"Short summary of the review",
                       "findings":[
                       {{
                            "severity": "HIGH",
                            "file": "path/to/file.py",
                            "line": 42,
                            "title": "Short issue title",
                            "description": "Explain the problem",
                            "recommendation": "Explain how it could be fixed"
                            }}     
                       ]
                  }}
                  Allowed overall values: 
                        PASS
                        WARNING
                        REQUEST_CHANGES
                        Allowed severity values:
                        LOW
                        MEDIUM
                        HIGH
                        CRITICAL
                        If there are no meaningful issues:
                        "findings": []
                        Do not invent line numbers
                      """
    response=openai_client.responses.create(model=OPENAI_MODEL,input=[{
        "role":"system",
        "content":system_prompt,
         },
        {
            "role":"user",
            "content": user_prompt,
        },],)
    output=response.output_text.strip()

    if output.startswith("```"):
        output=output.replace("```json","")
        output=output.replace("```","")
        output=output.strip()

    try:
        return json.loads(output)
    except json.JSONDecodeError:
        print("WARNING: AI returned invalid JSON.")
        print(output)
        return {
            "overall":"WARNING",
            "summary": (
                "AI returned an invalid review response."
            ),
            "findings": [
                {
                    "severity": "MEDIUM",
                    "file": "",
                    "line": 0,
                    "title": "AI response error",
                    "description": (
                        "The AI reviewer returned "
                        "an invalid response."
                    ),
                    "recommendation": (
                        "Run the review again."
                    ),
                }
            ],
        }

def create_comment(review):
    overall=review.get("overall","WARNING")
    summary=review.get("summary","")
    findings=review.get("findings",[])
    if overall=="PASS":
        status="PASS"
    elif overall=="WARNING":
        status="WARNING"
    else:
        status="REQUEST_CHANGES"
    line = []
    line.append("AI Code Review")
    line.append("")
    line.append(f"## Result: {status}")
    line.append("")
    line.append(f"**Summary:** {summary}")
    line.append("")

    if not findings:
        line.append("### Findings")
        line.append("")
        line.append("No Meaningful issues found")
    else:
        line.append(f"### Findings ({len(findings)})")
        line.append("")
        for index,findings in enumerate(findings,start=1):
            severity=findings.get("severity","MEDIUM")
            file=findings.get("file","")
            line=findings.get("line","")
            title=findings.get("title","Issue")
            description=findings.get("description","")
            recommendation=findings.get("recommendation","")
            line.append(f"### {index}."
                        f"{severity}-{title}")
            line.appen("")

            if file:
                if line:
                    lines.append(f"**Location:** "
                                 f"`{file}:{line}`")

                else:
                    line.append(f"**Location:**"
                                f"`{file}`")
                lines.append("")

            line.append(f"**Problem:**{description}")
            line.append("")
            line.append(f"**Recommendation:**{recommendation}")
            line.append("")

    line.append("Automated AI review")
    return  "\n".join(lines)

def post_comment(comment):
    url= f"{GITHUB_API}/repos/{GITHUB_REPOSITORY}/issues/{PR_NUMBER}/comments"
    payload= {"body":comment}
    response=requests.post(url=url,headers=github_headers,json=payload,timeout=30,)
    response.raise_for_status()

def main():
    print("AI Review")
    print(f"Repository: {GITHUB_REPOSITORY}")
    print(f"Pull Request: {PR_NUMBER}")
    print()
    print("Getting pull request information")
    pull_request=get_pull_request()
    print(f"Title: {pull_request.get('title',"")}")

    print("Getting pull request diff...")
    diff=get_pull_request_diff()
    if not diff.strip():
        print("No changes found.")
        return
    print(f"Diff size: {len(diff)} characters")

    diff=limit_diff(diff)

    review_rules=load_review_rules()
    print()
    print("Sending PR to AI...")
    review=review_with_ai(pull_request,diff,review_rules)
    print()
    print("AI review result")
    print(json.dumps(review,indent=2))

    print()
    print("Posting review to Github...")

    comment=create_comment(review)
    post_comment(comment)
    print("Review posted successfully")

if __name__ == "__main__":
    try:
        main()
    except Expection as error:
        print(f"ERROR: {error}")
        raise
