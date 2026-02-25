from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError(f"Phone must be 10 digits: {value}")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone_value):
        phone = Phone(phone_value)
        self.phones.append(phone)

    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return True
        return False
    
    def remove_phone(self, phone_value):
        self.phones = [p for p in self.phones if p.value != phone_value]

    def find_phone(self, phone_value):
        for p in self.phones:
            if p.value == phone_value:
                return p.value
        return None

    def __str__(self):
        phones_str = "; ".join(p.value for p in self.phones)
        return f"{self.name.value}: {phones_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return True
        return False
