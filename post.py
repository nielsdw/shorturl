import requests, json

url = "http://localhost:5000/ggh3_c"
data = {"url": "https://www.energyworks.com/",
	"shortcode": 'ggh3_c'
	}

response = requests.get(url, allow_redirects=False)
print(response.headers, response.status_code)
