from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Phone number must be a 10-digit number")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid birthday format. Use DD.MM.YYYY")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number):
        for p in self.phones:
            if p.value == phone_number:
                self.phones.remove(p)

    def edit_phone(self, current_number, new_number):
        for p in self.phones:
            if p.value == current_number:
                p.value = new_number

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phone_list = "; ".join(str(p) for p in self.phones)
        birthday_info = f"Birthday: {self.birthday.value}" if self.birthday else "No birthday specified"
        return f"Contact name: {self.name}, phones: {phone_list}, {birthday_info}"


class AddressBook(UserDict):
    def add_record(self, contact):
        self.data[contact.name.value] = contact

    def find(self, key):
        return self.data.get(key, None)

    def delete(self, key):
        if key in self.data:
            del self.data[key]

    def get_birthdays_per_week(self):
        today = datetime.now()
        next_week = today + timedelta(days=7)
        upcoming_birthdays = []
        for contact in self.data.values():
            if contact.birthday:
                birthdate = datetime.strptime(
                    contact.birthday.value, '%d.%m.%Y')
                if today <= birthdate < next_week:
                    upcoming_birthdays.append(contact)
        return upcoming_birthdays


if __name__ == "__main__":
    print("Test script:")

book = AddressBook()

john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")
john_record.add_birthday("01.01.1990")
book.add_record(john_record)

jane_record = Record("Jane")
jane_record.add_phone("9876543210")
jane_record.add_birthday("15.11.1985")
book.add_record(jane_record)

for name, record in book.data.items():
    print(record)

john = book.find("John")
john.edit_phone("1234567890", "1112223333")
print(john)

found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")

book.delete("Jane")

upcoming_birthdays = book.get_birthdays_per_week()
if upcoming_birthdays:
    print("Upcoming birthdays:")
    for contact in upcoming_birthdays:
        print(f"{contact.name}: {contact.birthday.value}")
else:
    print("No upcoming birthdays.")
