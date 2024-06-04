import re


def normalize_phone(phone_number: str):
    phone_number = phone_number.strip()
    phone_number = re.sub("\D",repl='', string=phone_number)
    phone_number = re.sub("^38",repl='', string=phone_number)
    if len(phone_number) != 10:
        raise ValueError("The phone number must consist of 10 digits.")
    return '+38' + phone_number