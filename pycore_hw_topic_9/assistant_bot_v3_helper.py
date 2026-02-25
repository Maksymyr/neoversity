from colorama import Fore, init

init(autoreset=True)

def input_error(handler):
    def wrapper(*args, **kwargs):
        try:
            return handler(*args, **kwargs)
        except ValueError as e:
            return f"{Fore.RED}Invalid arguments. {e}"
        except KeyError:
            return f"{Fore.RED}Contact not found."
        except IndexError:
            return f"{Fore.RED}Not enough arguments."
    return wrapper

def parse_input(user_input: str):
    parts = user_input.strip().split()
    if not parts:
        raise ValueError("Empty input")
    cmd = parts[0].lower()
    args = parts[1:]
    return cmd, args
