import requests, json

url = "http://localhost:5000/shorten"
data = {"url": "https://www.energyworks.com/",
	"shortcode": 'ggh3_c'
	}

response = requests.post(url, json=data)
print(response.json())
