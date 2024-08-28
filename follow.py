import json
import time
import os
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('TOKEN')
file_path = 'following.json'
followed = []

if not os.path.exists(file_path):
    with open(file_path, 'w') as file:
        json.dump([], file)

with open(file_path, 'r') as file:
    followed = json.load(file)


def repositories(topic):
    sort = 'stars'
    order = 'desc'
    per_page = 10
    url = f'https://api.github.com/search/repositories?q={topic}&sort={sort}&order={order}&per_page={per_page}'
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {token}',
        'X-GitHub-Api-Version': '2022-11-28'
    }

    response = requests.get(url, headers=headers)

    print(response.status_code)
    content = response.json()
    urls = []
    for item in content['items']:
        urls.append(item['url'])

    print(f"Found {len(urls)} for topic {topic}")
    return urls


def follow(username):
    if username in followed:
        print(f"skip user {username}")
        return
    time.sleep(2)

    url = f'https://api.github.com/user/following/{username}'
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {token}',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    response = requests.put(url, headers=headers)
    print(f"https://github.com/{username}  Following: {response.status_code} {username}  ")
    if response.status_code == 429:
        print("Error code waiting 5 minutes for next request")
        time.sleep(60 * 5)

    followed.append(username)
    with open(file_path, 'w') as file:
        json.dump(followed, file)


def contributors(url):
    url = f'{url}/contributors'
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {token}',
        'X-GitHub-Api-Version': '2022-11-28'
    }

    response = requests.get(url, headers=headers)

    content = response.json()
    result = []
    for item in content:
        login = item['login']
        result.append(login)
    print(f'Getting {len(result)} people')
    return result


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    topics = ['fabric', 'paper server', 'spigot plugin', 'spigot', 'minecraft', 'minecraft server', 'mods']
    for topic in topics:
        repos = repositories(topic)
        for repo in repos:
            users = contributors(repo)
            for user in users:
                follow(user)

        print(f"TOPIC DONE: {topic}")
    print("DONE")
