import requests

versions = ["0.16.0", "0.15.2", "master"]

def runcode(code, version="0.16.0"): 
    if version not in versions:
        raise ConnectionError("Version is not supported by the API");
        return;
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
