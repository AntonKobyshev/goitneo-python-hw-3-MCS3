from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not (len(value) == 10 or value.isdigit()):
            raise ValueError(
                "❌ Phone number must be a 10-digit number. Please try again.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("❌ Invalid birthday format. Use DD.MM.YYYY")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)

    def edit_phone(self, new_phone):
        while True:
            if len(new_phone) != 10 or not new_phone.isdigit():
                print("❌ Phone number must be a 10-digit number. Please try again.")
                new_phone = input("☎️ Enter a 10-digit phone number: ")
            else:
                self.phones[0] = Phone(new_phone)
                break

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p.value

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phone_list = '; '.join(str(p) for p in self.phones)
        return f"👤 Contact name: {self.name.value}, phone: {phone_list}, birthday: {self.birthday}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        for contact_name, record in self.data.items():
            if contact_name.lower() == name.lower():
                return record
        return None

    def delete(self, name):
        for key in list(self.data.keys()):
            if key.lower() == name.lower():
                del self.data[key]
