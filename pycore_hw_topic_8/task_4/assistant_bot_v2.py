from colorama import Fore, init

init(autoreset=True)


def input_error(handler):
    def wrapper(*args, **kwargs):
        try:
            return handler(*args, **kwargs)
        except ValueError:
            return f"{Fore.RED}Invalid arguments."
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


@input_error
def add_contact(args, contacts):
    if len(args) != 2:
        raise ValueError

    name, phone = args
    contacts[name] = phone
    return f"{Fore.BLUE}Contact added."


@input_error
def change_contact(args, contacts):
    if len(args) != 2:
        raise ValueError

    name, phone = args
    if name not in contacts:
        raise KeyError

    contacts[name] = phone
    return f"{Fore.BLUE}Contact updated."


@input_error
def show_phone(args, contacts):
    if len(args) != 1:
        raise ValueError

    name = args[0]
    if name not in contacts:
        raise KeyError

    return f"{Fore.BLUE}{contacts[name]}"


def show_all(contacts):
    if not contacts:
        return f"{Fore.BLUE}No contacts saved."

    return "\n".join(
        f"{Fore.BLUE}{name}: {phone}" for name, phone in contacts.items()
    )


def main():
    contacts = {}

    print(f"{Fore.MAGENTA}Welcome to the assistant bot")

    while True:
        try:
            user_input = input(f"{Fore.GREEN}Enter a command: ")
            command, args = parse_input(user_input)

            if command in ["exit", "close"]:
                print(f"{Fore.MAGENTA}Good bye!")
                break

            elif command == "hello":
                print(f"{Fore.BLUE}How can I help you?")

            elif command == "add":
                print(add_contact(args, contacts))

            elif command == "change":
                print(change_contact(args, contacts))

            elif command == "phone":
                print(show_phone(args, contacts))

            elif command == "all":
                print(show_all(contacts))

            else:
                print(f"{Fore.RED}Invalid command.")

        except ValueError:
            print(f"{Fore.RED}Please enter a command.")


if __name__ == "__main__":
    main()
