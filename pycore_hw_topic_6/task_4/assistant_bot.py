from colorama import Fore, init

init(autoreset=True)

def parse_input(user_input: str):
    parts = user_input.split()
    if not parts:
        return "", []
    cmd = parts[0].lower()
    args = parts[1:]
    return cmd, args


def add_contact(args, contacts):
    name, phone = args
    contacts[name] = phone
    return f"{Fore.BLUE}Contact added."


def change_contact(args, contacts):
    name, phone = args
    if name not in contacts:
        return f"{Fore.RED}Contact not found."
    contacts[name] = phone
    return f"{Fore.BLUE}Contact updated."


def show_phone(args, contacts):
    name = args[0]
    if name not in contacts:
        return f"{Fore.RED}Contact not found."
    return contacts[name]


def show_all(contacts):
    if not contacts:
        return f"{Fore.BLUE}No contacts saved."
    return "\n".join(f"{Fore.BLUE}{name}: {phone}" for name, phone in contacts.items())


def main():
    contacts = {}

    print(f"{Fore.MAGENTA}Welcome to the assistant bot")

    while True:
        user_input = input(f"{Fore.GREEN}Enter a command: ")

        command, args = parse_input(user_input)

        if command in ["exit", "close"]:
            print(f"{Fore.MAGENTA}Good bye!")
            break

        elif command == "hello":
            print(f"{Fore.BLUE}How can I help you?")

        elif command == "add":
            try:
                print(f"{Fore.BLUE}{add_contact(args, contacts)}")
            except ValueError:
                print(f"{Fore.RED}Invalid arguments. Usage: add name phone")

        elif command == "change":
            try:
                print(f"{Fore.BLUE}{change_contact(args, contacts)}")
            except ValueError:
                print(f"{Fore.RED}Invalid arguments. Usage: change name phone")

        elif command == "phone":
            try:
                print(f"{Fore.BLUE}{show_phone(args, contacts)}")
            except (ValueError, IndexError):
                print(f"{Fore.RED}Invalid arguments. Usage: phone name")

        elif command == "all":
            print(f"{Fore.BLUE}{show_all(contacts)}")

        else:
            print(f"{Fore.RED}Invalid command.")


if __name__ == "__main__":
    main()
