from colorama import Fore, init

from assistant_bot_v3_commands import (
    add_contact,
    change_contact,
    delete_contact,
    delete_phone,
    show_all,
    show_phone,
    find_phone_owner,
)
from assistant_bot_v3_helper import parse_input
from assistant_bot_v3_classes import AddressBook

init(autoreset=True)

def run_tests():
    book = AddressBook()

    # --- parse_input ---
    cmd, args = parse_input("add John 1234567890")
    assert cmd == "add"
    assert args == ["John", "1234567890"]

    try:
        parse_input("   ")
        assert False, "Empty input should raise ValueError"
    except ValueError:
        pass

    # --- add_contact ---
    result = add_contact(["John", "1234567890"], book)
    result = add_contact(["John", "5555555555"], book)
    assert "Contact added" in result or "Added phone to existing contact" in result
    john = book.find("John")
    assert john is not None
    assert john.find_phone("1234567890") == "1234567890"
    assert john.find_phone("5555555555") == "5555555555"

    result = add_contact(["Kate", "5555555555"], book)
    kate = book.find("Kate")
    assert kate is not None
    assert kate.find_phone("5555555555") == "5555555555"

    # invalid phone
    result = add_contact(["Mike", "123"], book)
    assert "Invalid arguments" in result

    # --- change_contact ---
    result = change_contact(["John", "1234567890", "1112223333"], book)
    assert "Phone updated" in result
    assert john.find_phone("1112223333") == "1112223333"
    assert john.find_phone("5555555555") == "5555555555"
    assert john.find_phone("1234567890") is None

    # change missing contact
    result = change_contact(["Unknown", "0000000000", "1111111111"], book)
    assert "Contact not found" in result

    # invalid args
    result = change_contact(["OnlyName"], book)
    assert "Invalid arguments" in result

    # --- show_phone ---
    result = show_phone(["John"], book)
    assert "1112223333" in result
    assert "5555555555" in result

    result = show_phone(["Unknown"], book)
    assert "Contact not found" in result

    result = show_phone([], book)
    assert "Invalid arguments" in result or "Not enough arguments" in result

    # --- show_all ---
    result = show_all(book)
    assert "John" in result
    assert "Kate" in result

    empty_book = AddressBook()
    empty_result = show_all(empty_book)
    assert "No contacts saved" in empty_result

    # --- delete_contact ---
    result = delete_contact(["Kate"], book)
    assert "deleted" in result
    assert book.find("Kate") is None

    result = delete_contact(["Unknown"], book)
    assert "Contact not found" in result

    result = delete_contact([], book)
    assert "Invalid arguments" in result or "Not enough arguments" in result

    # --- delete_phone ---
    result = delete_phone(["John", "5555555555"], book)
    assert "removed" in result
    assert john.find_phone("5555555555") is None

    result = delete_phone(["John", "0000000000"], book)
    assert "removed" in result or "Invalid arguments" in result

    # --- find_phone_owner ---
    add_contact(["Alice", "9998887777"], book)
    result = find_phone_owner(["9998887777"], book)
    assert "Phone 9998887777 belongs to Alice" in result

    result = find_phone_owner(["0000000000"], book)
    assert "not found" in result

    # --- delete_phone removes last phone ---
    add_contact(["Bob", "7776665555"], book)
    bob = book.find("Bob")
    assert bob is not None
    assert bob.find_phone("7776665555") == "7776665555"

    result = delete_phone(["Bob", "7776665555"], book)
    assert "deleted" in result
    assert book.find("Bob") is None

    print(f"{Fore.GREEN}All bot tests passed successfully!")


if __name__ == "__main__":
    run_tests()
