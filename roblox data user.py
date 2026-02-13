from asyncio import wait
import requests
import colorama

from colorama  import Fore, Style
from requests.exceptions import JSONDecodeError

print(Fore.GREEN + "This tool is used to scrape Roblox user data." + Style.RESET_ALL)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/91.0.4472.124 Safari/537.36"
}
# Function to fetch count from a given URL
def fetch_count(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except requests.RequestException as exc:
        return None, f"Request failed: {exc}"

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        return None, "Response was not JSON"

    if "count" not in data:
        return None, "Missing 'count' in response"
    return data["count"], None

# getting the user info from the api
def get_follower_count(user_id):
    url = f"https://friends.roblox.com/v1/users/{user_id}/followers/count"
    return fetch_count(url)


def get_friends_count(user_id):
    url = f"https://friends.roblox.com/v1/users/{user_id}/friends/count"
    return fetch_count(url)


def get_following_count(user_id):
    url = f"https://friends.roblox.com/v1/users/{user_id}/followings/count"
    return fetch_count(url)


def get_groups_count(user_id):
    url = f"https://groups.roblox.com/v1/users/{user_id}/groups/roles"
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except requests.RequestException as exc:
        return None, f"Request failed: {exc}"

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        return None, "Response was not JSON"

    groups = data.get("data", [])
    return len(groups), None

def get_user_data(user_id):
    url = f"https://users.roblox.com/v1/users/{user_id}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except requests.RequestException as exc:
        return None, f"Request failed: {exc}"

    try:
        data = response.json()
    except JSONDecodeError:
        return None, "Response was not JSON"

    return data, None

# printing the user data in format
def main():
    user_id = input("Enter the user ID: ")

    follower_count, error = get_follower_count(user_id)
    if error:
        print(f"{Fore.RED}Failed to get follower count: {error}{Style.RESET_ALL}")
    else:
        print(f"User ID: {user_id} has {follower_count} followers.")

    friends_count, error = get_friends_count(user_id)
    if error:
        print(f"{Fore.RED}Failed to get friends count: {error}{Style.RESET_ALL}")
    else:
        print(f"User ID: {user_id} has {friends_count} friends.")

    following_count, error = get_following_count(user_id)
    if error:
        print(f"{Fore.RED}Failed to get following count: {error}{Style.RESET_ALL}")
    else:
        print(f"User ID: {user_id} is following {following_count} users.")

    groups_count, error = get_groups_count(user_id)
    if error:
        print(f"{Fore.RED}Failed to get groups count: {error}{Style.RESET_ALL}")
    else:
        print(f"User ID: {user_id} is in {groups_count} groups.")

    user_data, error = get_user_data(user_id)
    if error:
        print(f"{Fore.RED}Failed to get user info: {error}{Style.RESET_ALL}")
    else:
        print(f"User Data for ID {user_id}: {user_data}")

if __name__ == "__main__":
    main()
    print(f"{Fore.BLUE}////{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}Data retrieval complete.{Style.RESET_ALL}")


    close = input(f"{Fore.YELLOW}Click enter to close program.{Style.RESET_ALL}")

