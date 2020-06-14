def run(o):    
    import requests
    r = requests.get('https://google.com')
    print(r.text)
    return r