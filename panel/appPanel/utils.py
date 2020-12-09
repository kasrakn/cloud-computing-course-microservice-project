import requests

def auth_checker(username, token):
    r = requests.post("http://localhost:8000/auth/check/", data={'username': username, 'token': token})

    return True if r.status_code == 200 else False
