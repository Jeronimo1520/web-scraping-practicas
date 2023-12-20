import requests
headers = {
    "user-agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/119.0.0.0 Safari/537.36'
}

token = "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"

for i in range(1,3):
    endpoint = "https://api.github.com/user/repos?page="+str(i)

    usuario = "Jeronimo1520"
    password = open('./password.txt').readline().strip()

    response = requests.get(endpoint, headers=headers, auth=(usuario, token))
    repos = response.json()
    for repo in repos:
        print(repo["name"])
        print()












