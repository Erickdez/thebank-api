import requests

data = {
    "name": "Erick Hernandez",
    "number": "7000123456780000",
    "date": "12/24",
    "code": "182"
}
response = requests.post("http://localhost:12345/verify", data=data)
print(response)
if response.status_code == 200:
    dataJson = response.json()
    print(dataJson) 

""" data = {
    "name": "Erick Hernandez",
    "number": "7000123456780000",
    "date": "12/24",
    "code": "182",
    "balance": 1583.26
}
response = requests.put("http://localhost:12345/insert", data=data)
print(response)
if response.status_code == 200:
    dataJson = response.json()
    print(dataJson) """

""" data = {
    "number": "7000123456780000",
    "balance": 1583.26
}
response = requests.patch("http://localhost:12345/modify", data=data)
print(response)
if response.status_code == 200:
    dataJson = response.json()
    print(dataJson) """
