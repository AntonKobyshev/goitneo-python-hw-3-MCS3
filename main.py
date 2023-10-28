from phonebook_console_bot import *
from phonebook_control_system import AddressBook


def main():
    address_book = AddressBook()
    print("🤖 Welcome to the assistant bot!")
    while True:
        user_input = input("⌨️ Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("🖐 Good bye!")
            break
        elif command == "hello":
            print("🖐 How can I help you?")
        elif command == "add":
            print(add_contact(args, address_book))
        elif command == "change":
            print(change_contact(args, address_book))
        elif command == "remove":
            print(delete_contact(args, address_book))
        elif command == "phone":
            print(show_phone(args, address_book))
        elif command == "all":
            print(show_all(address_book))
        elif command == "add-birthday":
            print(add_birthday(args, address_book))
        elif command == "show-birthday":
            print(show_birthday(args, address_book))
        elif command == "birthdays":
            print(get_birthdays_per_week(address_book))
        else:
            print("❌ Invalid command.")


if __name__ == "__main__":
    main()
