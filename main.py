import requests

def runcode(code, version="0.16.0"):
    headers = {
        "Content-Type": "text/plain",
        "X-Zig-Version": version,
    }
    response = requests.post(
        "https://zig-play.dev/server/run",
        headers=headers,
        data=code, timeout=10
    )
    response.raise_for_status()
    return response.text
