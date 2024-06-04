from utils import normalize_phone, input_error, save_data, load_data
import json
from classes import AddressBook, Record, Phone, Birthday, Name
from colorama import Fore


def parse_input(user_input: str):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def parse_name_and_last_param(args, num_of_params: int | None = None) -> tuple:
    """
    Takes arguments, given by user, and the number of params from the end, thta ou are interested in
    
    Note: return params in direct order. As they were passed by user.
    """
    name_and_params = [arg for arg in args]
    if num_of_params:
        params = []
        for i in range(-num_of_params, 0, 1):
            params.append(name_and_params[i])
            name = ' '.join([name for name in name_and_params[:-num_of_params]]).strip()
            return [name, *params]
    name = ' '.join([name for name in name_and_params]).strip()
    return name


@input_error
def add_contact(args, book: AddressBook):
    if not args:
        raise ValueError('Enter the argument for the command')

    name, phone = parse_name_and_last_param(args, 1)
    
    # Checks to see, if everything's ok
    if not len(phone) or not len(name):
        raise ValueError('Enter the argument for the command')

    # Normalizing the phone number to keep it consistent
    phone = normalize_phone(phone) 
    
    # Check to see whether we have to update or add a new contact
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        if not phone in record.phones:
            record.add_phone(phone)
        else:
            message = f'Such phone number is already present in contact {record.name}'
    return message


@input_error
def change_contact(args, book: AddressBook):
    if not args:
        raise ValueError('Enter the argument for the command')
        
    name, old_phone, new_phone = parse_name_and_last_param(args, 2)
    
    # Checks to see, if everything's ok
    if not len(new_phone) or not len(old_phone) or not len(name):
        raise ValueError('Enter the arguments for the command: Name, Old Phone, New Phone')
    if not name in book.keys():
        raise ValueError("There's no such a name in your contacts, please, add the person first")
    
    # Normalizing the phone number to keep it consistent
    new_phone = normalize_phone(new_phone)
    old_phone = normalize_phone(old_phone)
    book[name].edit_phone(old_phone, new_phone)
    
    return f"For user {name}, phone {old_phone} is replaced with {new_phone}."


@input_error
def show_phone(args, book: AddressBook):
    name = parse_name_and_last_param(args)
    return 'Phones: ' + ' '.join([str(phone) for phone in book[name].phones])


@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = parse_name_and_last_param(args, 1)
    book[name].add_birthday(birthday)
    return "Succesfully updated the birthday"


@input_error
def show_birthday(args, book: AddressBook):
    name = parse_name_and_last_param(args)
    return book[name].birthday.value if book[name].birthday else f'There is no birthday specified for the user {name}.'


@input_error
def show_upcoming_birthdays(book: AddressBook):
    return book.get_upcoming_birthdays()


@input_error
def show_all(book: AddressBook):
    return [{name: str(book[name])} for name in book.keys()]


@input_error
def handle_wrong_input():
    raise ValueError("Invalid command. Type 'help' to get the list of commands")


@input_error # Is nescessary here, because it handles ^C(KeyboardInterruption) exit
def run():

    commands = {
    'hello': 'The greeting',
    'add': f'To add the contact, {Fore.GREEN}example{Fore.RESET}: add John +380679796518',
    'change': f'To alter the contact, {Fore.GREEN}example{Fore.RESET}: change John +380679796518 +380997215120',
    'phone': f'Get the phone number of a user',
    'all': 'List all the users',
    'add-birthday': f'To add a birthday to a specific user, {Fore.GREEN}example{Fore.RESET}: John 2003.06.07',
    'show-birthday': 'To show a birthday of a specific user',
    'birthdays': "To get the closest birthdays of your contacts (7 days ahead)"
    }
    
    book = load_data()
    print("* Welcome to the assistant bot!\n* Type 'help' to see the list of available commands")
    print("* Type 'exit', 'close' or Ctrl|Cmd+C to exit")

    
    while True:
        try:
            user_input = input("\nEnter a command: ")
            command, *args = parse_input(user_input)
        except KeyboardInterrupt:
            print('Bye-bye!')
            break

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print('Your contacts are:')
            for person in book.values():
                print(" * " + str(person))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))      
        elif command == "birthdays":
            print("The people to give congratulations to are:")
            people_to_congrat = show_upcoming_birthdays(book)
            if people_to_congrat:
                for person in people_to_congrat:
                    print(" * " + str(person))
            else:
                print("There are no people celebrating :'(")
        elif command == 't':
            print(f'Book:\n{dict(book)}')
        elif command == "help":
            print('List of all the available commands:')
            # Find the longest key to set the spacing
            longest_key = max(len(key) for key in commands.keys())
            for key, value in commands.items():
                print(f"{Fore.YELLOW}{key:<{longest_key}}{Fore.RESET} : {value}")
            
        else:
            print(handle_wrong_input())
    
    # On the app's exit
    save_data(book)
