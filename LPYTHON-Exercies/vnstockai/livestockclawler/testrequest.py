import requests

url = "https://banggia.cafef.vn/stockhandler.ashx?center=undefined"

payload = {}
headers= {}

response = requests.request("POST", url, headers=headers, data = payload)

print(response.text.encode('utf8'))


