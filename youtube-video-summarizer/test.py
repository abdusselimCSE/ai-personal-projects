import requests  # type: ignorecl
import sys

url = "http://127.0.0.1:8000/summary"

if len(sys.argv) >= 2:
    inputVideoId = sys.argv[1]
else:
    inputVideoId = input("Please enter your video id : ")

payload = {
    "video_id": inputVideoId,
}

response = requests.post(url, json=payload)

if not response.ok:
    print("API ERROR:", response.status_code)
    print(response.text)
    raise SystemExit(1)

try:
    data = response.json()
except Exception:
    print("NOT JSON RESPONSE:", response.status_code)
    print(response.text)
    raise SystemExit(1)

print("SUMMARY:\n")
print(data.get("summary", "No summary key in response"))


# print(10*"-" + "\nTRANSCRIPT:\n")
# print(data["transcript"])
