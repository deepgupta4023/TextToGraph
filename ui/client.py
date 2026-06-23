import requests

API_URL = "http://localhost:8000"


def ingest(text):

    response = requests.post(
        f"{API_URL}/ingest",
        json={"text": text}
    )

    if response.status_code != 200:
        return {
            "error": response.text
        }

    try:
        return response.json()
    except Exception:
        return {
            "error": "Invalid JSON response",
            "raw": response.text
        }


def query(question):

    response = requests.post(
        f"{API_URL}/query",
        json={"question": question}
    )

    if response.status_code != 200:
        return {
            "error": response.text
        }

    return response.json()