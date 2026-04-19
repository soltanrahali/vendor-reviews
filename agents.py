import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()


def intake_agent(comment: str, vendor_name: str) -> dict:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a comment intake agent. Your job is to:\n"
                    "1. Check if the comment is meaningful (not spam or gibberish)\n"
                    "2. Fix obvious typos or formatting\n"
                    "3. Identify the sentiment: positive, negative, or neutral\n"
                    "Return ONLY a JSON object with these keys: "
                    "valid (bool), cleaned_comment (str), sentiment (str), reason (str)"
                ),
            },
            {"role": "user", "content": f"Vendor: {vendor_name}\nComment: {comment}"},
        ],
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content)


def summary_agent(comments: list[dict], vendor_name: str) -> str:
    if not comments:
        return "No comments yet for this vendor."

    comments_text = "\n".join(
        f"- [{c['sentiment']}] {c['content']}" for c in comments
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a summary agent. Given comments about a vendor, produce a "
                    "concise structured summary covering: overall sentiment, key themes, "
                    "and notable highlights. Keep it under 200 words."
                ),
            },
            {
                "role": "user",
                "content": f"Vendor: {vendor_name}\n\nComments:\n{comments_text}",
            },
        ],
    )
    return response.choices[0].message.content


def orchestrator(task: str, **kwargs):
    if task == "intake":
        return intake_agent(kwargs["comment"], kwargs["vendor_name"])
    elif task == "summarize":
        return summary_agent(kwargs["comments"], kwargs["vendor_name"])
    else:
        raise ValueError(f"Unknown task: {task}")
