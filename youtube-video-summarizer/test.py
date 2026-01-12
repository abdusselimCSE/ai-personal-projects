import requests  # type: ignore

url = "http://127.0.0.1:8000/summary"

payload = {
    "video_id": "I1g3etLad3M",
}

response = requests.post(url, json=payload)

data = response.json()

print("SUMMARY:\n")
print(data["summary"])

# print(10*"-" + "\nTRANSCRIPT:\n")
# print(data["transcript"])
