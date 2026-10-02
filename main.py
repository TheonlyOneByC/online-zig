import requests

def runcode(code, version="0.16.0"):
    headers = {
        "Content-Type": "text/plain",
        "X-Zig-Version": version,
    }
    return requests.post(
        "https://zig-play.dev/server/run",
        headers=headers,
        data=code
    )
