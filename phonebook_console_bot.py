from datetime import datetime, timedelta
from phonebook_control_system import Record


def parse_input(user_input):
    user_input = user_input.strip()
    cmd, *args = user_input.split()
    cmd = cmd.lower()
    return cmd, args


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Enter user name please."
        except IndexError:
            return "Give me name and phone please."
        except ValueError:
            return "Give me name and phone please."
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"
    return inner


@input_error
def add_contact(args, address_book):
    if len(args) == 2:
        name, new_phone = args
        if len(new_phone) != 10 or not new_phone.isdigit():
            print("Phone number must be a 10-digit number. Please try again.")
            while True:
                new_value = input("Enter a 10-digit phone number: ")
                if len(new_value) == 10 and new_value.isdigit():
                    new_phone = new_value
                    break
        record = Record(name)
        record.add_phone(new_phone)
        address_book.add_record(record)
        return f"✔️ Contact {name} added."
    else:
        return "❌ Invalid command. Please give name and phone number."


@input_error
def change_contact(args, address_book):
    if len(args) == 2:
        name, new_phone = args
        if not new_phone.isdigit() or len(new_phone) != 10:
            while True:
                new_phone = input(
                    "❌ Phone number must be a 10-digit number. Enter a 10-digit phone number: ")
                if len(new_phone) == 10 and new_phone.isdigit():
                    break

        record = address_book.find(name)
        if record:
            if len(record.phones) > 0:
                record.edit_phone(new_phone)
                return f"✔️ Phone number updated for {name}."
            else:
                return f"❌ Contact {name} has no phone number to change."
        else:
            return f"❌ Contact {name} not found."
    else:
        return "❌ Invalid command. Please provide name and new phone number."


@input_error
def delete_contact(args, address_book):
    if len(args) == 1:
        name = args[0]
        address_book.delete(name)
        return f"✔️ Contact {name} deleted."
    else:
        return "❌ Invalid command. Please provide a single name."


@input_error
def show_phone(args, address_book):
    if len(args) == 1:
        name = args[0].lower()
        record = address_book.find(name)
        if record:
            if record.phones:
                phone = record.phones[0].value
                return f"☎️ Phone number for {record.name.value}: {phone}"
            else:
                return f"❌ Contact {record.name.value} does not have a phone number."
        else:
            return f"❌ Contact {args[0]} not found."
    else:
        return "❌ Invalid command. Please provide a single name."


@input_error
def show_all(address_book):
    if len(address_book) > 0:
        result = "\n".join(
            [f"{name}: {phone}" for name, phone in address_book.items()])
        return result
    else:
        return "❌ No contacts found."


@input_error
def add_birthday(args, address_book):
    if len(args) == 2:
        name, birthday = args
        record = address_book.find(name)
        if record:
            while True:
                try:
                    record.add_birthday(birthday)
                    return f"📅 Birthday added for {name}."
                except ValueError as e:
                    print("❌ Invalid birthday format. Use DD.MM.YYYY.")
                    birthday = input(
                        "❌ Enter a valid birthday date (DD.MM.YYYY): ")
        else:
            return f"❌ Contact {name} not found."
    else:
        return "❌ Invalid command. Please provide name and birthday in the format DD.MM.YYYY."


@input_error
def show_birthday(args, address_book):
    if len(args) == 1:
        name = args[0]
        record = address_book.find(name)
        if record and record.birthday:
            return f"📅 Birthday for {name}: {record.birthday.value}"
        elif record:
            return f"❌ No birthday set for {name}."
        else:
            return f"❌ Contact {name} not found."
    else:
        return "❌ Invalid command. Please provide a single name."


@input_error
def get_birthdays_per_week(address_book):
    today = datetime.today()
    next_monday = today + timedelta(days=(7 - today.weekday()))
    next_monday = next_monday.replace(
        hour=0, minute=0, second=0, microsecond=0)
    next_sunday = next_monday + \
        timedelta(days=6, hours=23, minutes=59, seconds=59)
    upcoming_birthdays = []

    for record in address_book.data.values():
        if record.birthday:
            bday_date = datetime.strptime(record.birthday.value, '%d.%m.%Y')
            bday_date = bday_date.replace(year=today.year)

            if next_monday <= bday_date <= next_sunday:
                upcoming_birthdays.append(
                    (record.name.value, bday_date.strftime('%d.%m.%Y')))

    if upcoming_birthdays:
        return "✔️📅 Upcoming birthdays in the next week:\n" + "\n".join([f"{name}: {birthday}" for name, birthday in upcoming_birthdays])
    else:
        return "❌📅 No upcoming birthdays in the next week."


if __name__ == "__main__":
    print("Welcome to the assistant function!")
