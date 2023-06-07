from http.cookies import SimpleCookie
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 '
                  'Safari/537.36',
}

cookie = SimpleCookie()
import requests

r = requests.get("http://192.168.64.123:3000/", headers=headers)
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 '
                  'Safari/537.36',
    r.cookies.keys()[0]:r.cookies.values()[0]
}

s = requests.get("http://192.168.64.123:3000/index.php/apps/files/", headers=headers, cookies={r.cookies.keys()[0]:r.cookies.values()[0]})
print(1)