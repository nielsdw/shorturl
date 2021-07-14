import requests, json

url = "http://localhost:5000/shorten"
data = {"url": "https://www.nu.nl/",
        "shortcode": "MNcQc"
        }

response = requests.post(url, json=data, allow_redirects=False)
print(response.content, response.headers, response.status_code)
