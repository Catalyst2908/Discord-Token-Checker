import requests
import colorama
import os

colorama.init()

# Cata

def checkToken(token):
    try:
        r = requests.get("https://discord.com/api/v9/users/@me", headers={"Authorization": token})
        r.raise_for_status()
        return r.status_code
    except requests.exceptions.RequestException as e:
        print(colorama.Fore.RED + f"Error checking token: {e}")
        return None

def printResult(status, token):
    if status is None:
        color = colorama.Fore.RED
        invalid.append(token)
        print(color + "Invalid" + colorama.Fore.LIGHTBLACK_EX + f" | {token}")
    elif status == 200:
        color = colorama.Fore.GREEN
        valid_tokens.append(token)
        print(color + "Valid" + colorama.Fore.LIGHTBLACK_EX + f" | {token}")
    elif status == 429:
        color = colorama.Fore.YELLOW
        print(color + str(status) + colorama.Fore.LIGHTBLACK_EX + f" | {token}")
    else:
        color = colorama.Fore.RED
        invalid.append(token)
        print(color + "Invalid" + colorama.Fore.LIGHTBLACK_EX + f" | {token}")

# Main

def ensure_files_exist():
    if not os.path.exists("tokens-to-verify.txt"):
        with open("tokens-to-verify.txt", "w"):
            pass

    if not os.path.exists("tokens-invalid.txt"):
        with open("tokens-invalid.txt", "w"):
            pass

    if not os.path.exists("tokens-valid.txt"):
        with open("tokens-valid.txt", "w"):
            pass

def main():
    ensure_files_exist()

    print(colorama.Fore.LIGHTBLACK_EX + "Checking tokens...")

    try:
        with open("tokens-to-verify.txt", "r") as file:
            tokens = file.read().splitlines()
    except FileNotFoundError:
        print(colorama.Fore.RED + "Error: tokens-to-verify.txt not found.")
        return

    for token in tokens.copy():
        status = checkToken(token)
        printResult(status, token)

    print(colorama.Fore.LIGHTBLACK_EX + "Saving valid tokens to tokens-valid.txt...")

    with open("tokens-valid.txt", "a") as valid_file:
        valid_file.write("\n".join(valid_tokens) + "\n")

    print(colorama.Fore.LIGHTBLACK_EX + "Saving invalid tokens to tokens-invalid.txt...")

    with open("tokens-invalid.txt", "a") as invalid_file:
        invalid_file.write("\n".join(invalid) + "\n")

    print(colorama.Fore.LIGHTBLACK_EX + "Removing verified tokens from tokens-to-verify.txt...")

    with open("tokens-to-verify.txt", "w"):
        pass

    print(colorama.Fore.RESET + "Done!")

if __name__ == "__main__":
    invalid = []
    valid_tokens = []
    main()