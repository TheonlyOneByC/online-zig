import requests
import re
import os
from functools import partial

versions = ["0.16.0", "0.15.2", "master"]
macro_pattern = r"@readfile\([\'\"](.+?)[\'\"]\)"

write_macro = r"@writefile\(\s*['\"](.+?)['\"]\s*,\s*['\"](.+?)['\"]\s*\);"

def file_return(match):
	name = match.group(1)
	
	try:
		if os.path.isfile(name):
			with open(name, "r") as e:
				content = e.read()
			return f'"{content}"'
	except FileNotFoundError:
		raise NameError(f"{name} does not exist")

def writefile(match, overwrite=True):
    name = match.group(1)
    content = match.group(2)

    if os.path.exists(name):
        if overwrite:
            with open(name, "w") as e:
                e.write(content)
        else:
            raise ValueError("File already exists")
    else:
        with open(name, "w") as e:
            e.write(content)
    return ""

def runcode(code, version="0.16.0", o=True):
    if version not in versions:
        raise ValueError("Version is not supported by the API")

    processed_code = re.sub(macro_pattern, file_return, code)
    processed_code = re.sub(write_macro, partial(writefile, overwrite=o), processed_code)

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
