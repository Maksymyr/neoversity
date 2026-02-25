from colorama import Fore, init

from assistant_bot_v3_commands import (
    add_contact,
    change_contact,
    delete_phone,
    delete_contact,
    find_phone_owner,
    show_all,
    show_phone,
)
from assistant_bot_v3_helper import parse_input
from assistant_bot_v3_classes import AddressBook

init(autoreset=True)

def main():
    book = AddressBook()
    print(f"{Fore.MAGENTA}Welcome to the assistant bot")

    while True:
        user_input = input(f"{Fore.GREEN}Enter a command: ")
        try:
            command, args = parse_input(user_input)

            if command in ["exit", "close"]:
                print(f"{Fore.MAGENTA}Good bye!")
                break
            elif command == "hello":
                print(f"{Fore.BLUE}How can I help you?")
            elif command == "add":
                print(add_contact(args, book))
            elif command == "change":
                print(change_contact(args, book))
            elif command == "delete_contact":
                print(delete_contact(args, book))
            elif command == "delete_phone":
                print(delete_phone(args, book))
            elif command == "phone":
                print(show_phone(args, book))
            elif command == "find_owner":
                print(find_phone_owner(args, book))
            elif command == "all":
                print(show_all(book))
            else:
                print(f"{Fore.RED}Invalid command.")

        except ValueError:
            print(f"{Fore.RED}Please enter a command.")

if __name__ == "__main__":
    main()