from collections import UserDict
from utils import normalize_phone, string_to_date, date_to_string
from datetime import date, datetime

class Field:    
    def __init__(self):
        self._value = None

    def __str__(self):
        return str(self._value)    
    
    def to_dict(self):
        return {"value": self._value}


class Name(Field):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __repr__(self):
        return f"Name({self.value})"
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value        


class Phone(Field):
    def __init__(self, value):
        super().__init__()
        self.value = value
        
    def __repr__(self):
        return f"Phone({self.value})"
    
    def __eq__(self, other):
        if isinstance(other, Phone):
            return self.value == other.value
        elif isinstance(other, str):
            return self.value == other
        else:
            return NotImplemented   
         
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        try:
            value = normalize_phone(value)
        except ValueError as e: 
            raise e 
        self._value = value
        

class Birthday(Field):
    def __init__(self, value: str):
        try:
            self.__value = None
            self.value = value
            
        except ValueError as e:
            raise ValueError(f"Invalid date format. Use DD.MM.YYYY\n{e}")
        
    def __str__(self):
        return date_to_string(self.value) if self.value else ''
    
    def __repr__(self) -> str:
        return f'Birthday({str(self.value)})'

    def to_dict(self):
        return {"value": date_to_string(self.value) if self.value else ''}  # assuming this is your date format
        
    @property
    def value(self) -> datetime:
        return self.__value
    
    @value.setter
    def value(self, value: str | datetime):
        self.__value = string_to_date(value) if isinstance(value, str) else value
  
    
class Record:
    def __init__(self, name: str, phones: list[str] | None = None, birthday: str | None = None):
        self.__name = None
        self.name = name
        
        self.__phones = None
        self.phones = [Phone(phone) for phone in phones] if phones else []
        # self.add_phone(phone)
        
        self.__birthday = None
        self.birthday = Birthday(birthday) if birthday else None
        
    @classmethod
    def from_objects(cls, name: Name, phones: list[Phone] | None = None, birthday: Birthday | None = None):
        return cls(name.value, [phone.value for phone in phones], birthday.value)
    
    def __str__(self):
        return f"Contact name: {self.__name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"
    
    def __repr__(self) -> str:
        return f"Record.from_objects({self.name}, {self.phones}, {self.birthday})"
    
    def remove_phone(self, phone: str):
        try:
            phone = Phone(phone)
        except ValueError as e:
            print(f"ERROR: {e}")
            return
        self.phones.remove(phone)
        
    def edit_phone(self, phone_to_edit: str, new_phone: str):
        old_phone = Phone(phone_to_edit)
        if old_phone in self.phones:
            new_phone = Phone(new_phone)
            self.phones.remove(old_phone)
            self.phones.append(new_phone)
        else:
            raise ValueError(f"No such phone number is present in a current record.\n The record is: {str(self)}")
        
        
    def find_phone(self, phone: str) -> str:
        return [ph for ph in self.phones if ph == Phone(phone)][0].value
    

    def add_phone(self, phone: str):
        try:
            phone = Phone(phone)
        except ValueError as e:
            raise e
        self.phones.append(phone)
        
    def add_birthday(self, birthday: str):
        try:
            birthday = string_to_date(birthday)
            if birthday > date.today():
                raise ValueError('The birtday cannot be the future date.')
            self.birthday = birthday
        except ValueError as e:
            raise e

    def to_dict(self):
        return {
            "name": self.name,
            "phones": [phone.to_dict() for phone in self.phones],
            "birthday": self.birthday.to_dict() if self.birthday else None,
        }

    @property
    def name(self) -> str:
        return self.__name.value
    
    @name.setter
    def name(self, value:str):
        self.__name = Name(value)
        
    @property
    def phones(self) -> list[Phone] | None:
        return self.__phones
    
    @phones.setter
    def phones(self, value: list[Phone]):
        self.__phones = value
        
    @property
    def birthday(self) -> Birthday | None:
        return self.__birthday
    
    @birthday.setter
    def birthday(self, value: Birthday):
        self.__birthday = value


class AddressBook(UserDict):
    
    def add_record(self, value: Record):
        self.data[value.name] = value
        
    def find(self, name: str) -> Record | None:
        """
        Used to define whether the record in address book should be updated, or created.
        
        Returns None, if record must be created and added, or Record, if it's present
        """
        try:
            return self.data[name]
        except Exception as e:
            return None
    
    def delete(self, name: str) -> Record | None:
        "Is actually not used anywhere. Legacy from precious tasks"
        return self.data.pop(name, None)
    
    def get_upcoming_birthdays(self, days=7) -> list[Record]:
        upcoming_birthdays = []
        today = date.today()

        for user in self.data.values():
            
            # Skipping the iteration, if birthday for a user is not specified 
            # (I wish there was a better way doing it, than that)
            if user.birthday is None:
                continue
            birthday_this_year = user.birthday.value.replace(year=today.year)
            
            # Перевірка чи день народження вже не минув, щоб коректно обраховувавати крайній випадок - 2024.12.30 - 2025.01.01
            if birthday_this_year <= today:
                birthday_this_year = birthday_this_year.replace(year=today.year+1)
            
            if 0 <= (birthday_this_year - today).days <= days:           
                congratulation_date_str = date_to_string(birthday_this_year)
                upcoming_birthdays.append(Record(user.name.value, [str(phone) for phone in user.phones] , congratulation_date_str))
        return upcoming_birthdays
    
    def to_list(self) -> list:
        return [{name: {'phones': self.data[name].phones, 'birthday': str(self.data[name].birthday)} for name in self.data.keys()}]

    def to_dict(self):
        return {name: record.to_dict() for name, record in self.data.items()}
