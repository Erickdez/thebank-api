import requests

"""
response = requests.get("http://localhost:12345/card/7000123456780000")
print(response)
dataJson = response.json()
print(dataJson)
"""


data = {
    "name": "Erick Hernandez",
    "number": "7000123456780000",
    "date": "12/24",
    "code": "182",
    "balance": 20.25
}
response = requests.post("http://localhost:12345/verify", data=data)
print(response)
if response.status_code == 200:
    dataJson = response.json()
    if dataJson['response'] == '00':
        print(dataJson)
    else:
        print(dataJson)

"""
data = {
    "name": "Erick Hernandez",
    "number": "7000123456780000",
    "date": "12/24",
    "code": "182",
    "balance": 0.00
    "limit": 1000.00
    "status": "Activa"
}
response = requests.put("http://localhost:12345/insert", data=data)
print(response)
if response.status_code == 200:
    dataJson = response.json()
    print(dataJson) 
"""

""" 

"""
