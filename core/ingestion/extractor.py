import json
import re
from openai import OpenAI
from config import config
from core.prompts import EXTRACTION_PROMPT

client = OpenAI(api_key=config.OPENAI_API_KEY)
model= config.OPENAI_MODEL

def extract_graph_from_text(text):

    prompt = EXTRACTION_PROMPT.format(text=text)

    response = client.chat.completions.create(
        model=model,
        temperature=0,
        messages=[
            {"role": "system", "content": "You extract entities and relationships."},
            {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content

    # Extract JSON safely
    try:
        json_text = re.search(r"\{.*\}", content, re.DOTALL).group()
        data = json.loads(json_text)
    except Exception:
        data = {"entities": [], "relations": []}

    return data