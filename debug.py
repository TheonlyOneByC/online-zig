import requests
import re
import os

versions = ["0.16.0", "0.15.2", "master"]
macro_pattern = r"@readfile\([\'\"](.+?)[\'\"]\)"

def file_return(match):
    name = match.group(1)

    if not os.path.isfile(name):
        raise ValueError(f"{name} is not a file or does not exist")

    with open(name, "r", encoding="utf-8") as e:
        content = e.read()

    escaped_content = content.replace('"', '\\"').replace('\n', '\\n')
    return f'"{escaped_content}"'


def runcode(code, version="0.16.0"):
    if version not in versions:
        raise ValueError("Version is not supported by the API")

    processed_code = re.sub(macro_pattern, file_return, code)

    headers = {
        "Content-Type": "text/plain",
        "X-Zig-Version": version,
    }

    response = requests.post(
        "https://zig-play.dev/server/run",
        headers=headers,
        data=processed_code,
        timeout=10
    )

    print("Status:", response.status_code)
    print("Response:", response.text)

    response.raise_for_status()
    return response.text

def fmtcode(code, version="0.16.0"):
    if not version in versions:
        raise ValueError("Unsupported Version")
    	
    processed_code = re.sub(macro_pattern, file_return, code)

    response = requests.post(
        "https://zig-play.dev/server/fmt",
        headers={
            "Content-Type": "text/plain",
            "X-Zig-Version": version,
        },
        data=processed_code,
        timeout=10,
    )
    print(response.text)
    print(response.status_code)
    response.raise_for_status()
    return response.text
