from github import Github
import requests
import os
from dotenv import load_dotenv

load_dotenv()
ghusername = os.getenv('GHUSERNAME') 
access_token = os.getenv('ACCESS_TOKEN')
repo_name = os.getenv('REPO_NAME')
base_url = os.getenv('BASE_URL')


#функция создания нового репозитория
def create_repo(access_token, repo_name):
    data = {
        "name": repo_name,
        "private": False
    }

    response = requests.post(f"{base_url}/user/repos", json=data, headers={
        "Authorization": f"Bearer {access_token}"
    })

    if response.status_code == 201:
        print(f"Репозиторий создан. Код: {response.status_code}")
    else:
        print(f"Репозиторий не удалось создать. Код: {response.status_code}")

#функция вывода списка репозиториев для проверки
def check_repo(access_token, ghusername):  
    gh = Github(access_token)
    user = gh.get_user(ghusername)
    repos = user.get_repos()
    for repo in repos:
        print(repo.name)

    gh.close()

#функция удаления репозитория
def delete_repo(access_token, ghusername, repo_name):
    url = f"{base_url}/repos/{ghusername}/{repo_name}"
   
    headers = {
        "Authorization": f"token {access_token}",
    }
    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        print(f"Репозиторий успешно удалён. Код: {response.status_code}")
    elif response.status_code == 404:
        print(f"Репозиторий не найден или уже удалён. Код: {response.status_code}")
    else:
        print(f"Репозиторий не удалось удалить. Код: {response.status_code}")


#Функция ввода команды и проверки значения
def check_number():
    while True:
        try:
            num = int(input("Введите команду (1-создать репозиторий, 2-вывести список репозиториев, 3-удалить репозиторий): "))
            if num not in (1, 2, 3):
                print("Неверное значение. Введите 1, 2 или 3.")
            else:
                return num
        except ValueError:
            print("Вы ввели не число. Попробуйте ещё раз.")


num = check_number()
if num == 1:
    create_repo(access_token, repo_name)
elif num == 2:
    check_repo(access_token, ghusername)
elif num == 3:
    delete_repo(access_token, ghusername, repo_name)
else:
    raise ValueError("Неизвестное значение")