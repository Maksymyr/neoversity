
from colorama import Fore, init

from assistant_bot_v3_classes import (
    AddressBook, 
    Record,
)
from assistant_bot_v3_helper import input_error

init(autoreset=True)

@input_error
def add_contact(args, book: AddressBook):
    if len(args) != 2:
        raise ValueError("Expected: add <name> <phone>")
    name, phone = args
    record = book.find(name)
    if record:
        record.add_phone(phone)
        return f"{Fore.BLUE}Added phone to existing contact."
    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)
    return f"{Fore.BLUE}Contact added."

@input_error
def change_contact(args, book: AddressBook):
    if len(args) != 3:
        raise ValueError("Expected: change <name> <old_phone> <new_phone>")
    name, old_phone, new_phone = args
    record = book.find(name)
    if not record:
        raise KeyError
    if record.edit_phone(old_phone, new_phone):
        return f"{Fore.BLUE}Phone updated."
    else:
        return f"{Fore.RED}Old phone not found."

@input_error
def show_phone(args, book: AddressBook):
    if len(args) != 1:
        raise ValueError("Expected: phone <name>")
    name = args[0]
    record = book.find(name)
    if not record:
        raise KeyError
    return f"{Fore.BLUE}{record}"

@input_error
def find_phone_owner(args, book: AddressBook):
    if len(args) != 1:
        raise ValueError("Expected: find_phone <phone>")
    phone_to_find = args[0]
    for record in book.data.values():
        if record.find_phone(phone_to_find):
            return f"{Fore.BLUE}Phone {phone_to_find} belongs to {record.name.value}."
    return f"{Fore.RED}Phone {phone_to_find} not found."

def show_all(book: AddressBook):
    if not book.data:
        return f"{Fore.BLUE}No contacts saved."
    return "\n".join(f"{Fore.BLUE}{r}" for r in book.data.values())

@input_error
def delete_contact(args, book: AddressBook):
    if len(args) != 1:
        raise ValueError("Expected: delete_contact <name>")
    name = args[0]
    if book.delete(name):
        return f"{Fore.BLUE}Contact '{name}' deleted."
    else:
        return f"{Fore.RED}Contact not found."
    
@input_error
def delete_phone(args, book: AddressBook):
    if len(args) != 2:
        raise ValueError("Expected: delete_phone <name> <phone>")
    name, phone = args
    record = book.find(name)
    if not record:
        raise KeyError
    record.remove_phone(phone)
    
    if not record.phones:
        book.delete(name)
        return f"{Fore.BLUE}Phone '{phone}' removed and contact '{name}' deleted (no phones left)."
    
    return f"{Fore.BLUE}Phone '{phone}' removed from {name}."


