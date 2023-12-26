from collections import UserDict
from datetime import datetime
import re


class Field:
    def __init__(self, value):
        if not self.is_valid(value):
            raise ValueError
        self.__value = value

    def __str__(self):
        return str(self.__value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if not self.is_valid(new_value):
            raise ValueError
        self.__value = new_value

    def is_valid(self, value):
        return True


class Name(Field):
    pass


class Phone(Field):
    def is_valid(self, value):
        if len(value) != 10 or re.search(r"\D", value):
            raise ValueError("Incorrect phone number format")
        return True


class Birthday(Field):
    def is_valid(self, value):
        try:
            birthday = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError(
                "Incorrect birthday data format. Please use dd.mm.yyyy pattern"
            )
        if birthday > datetime.today():
            raise ValueError(f"Birthday date '{value}' is in the future")
        return True


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, rm_phone):
        for phone in self.phones:
            if phone.value == rm_phone:
                self.phones.remove(phone)
                return
        raise ValueError(f'Phone "{rm_phone}" does not exist')

    def edit_phone(self, old_phone, new_phone):
        for i, _ in enumerate(self.phones):
            if self.phones[i].value == old_phone:
                self.phones[i].value = new_phone
                return
        raise ValueError(f'Phone "{old_phone}" does not exist')

    def find_phone(self, find_phone):
        for phone in self.phones:
            if phone.value == find_phone:
                return phone
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, " \
            f"phones: {'; '.join(p.value for p in self.phones)}, " \
            f"birthday: {self.birthday}"

    def days_to_birthday(self):
        if self.birthday is None:
            return None

        birthday = datetime.strptime(self.birthday.value, "%d.%m.%Y")

        today = datetime.today()
        # truncating hours, minutes etc.
        today = today.replace(hour=0, minute=0, second=0, microsecond=0)

        current_year = int(today.strftime("%Y"))
        this_year_bday = birthday.replace(year=current_year)

        if this_year_bday < today:
            this_year_bday = birthday.replace(year=current_year + 1)

        delta = this_year_bday - today
        return delta.days


class AddressBook(UserDict):
    def add_record(self, record):
        name = record.name.value
        if self.data.get(name):
            raise ValueError(f'Name "{name}" already exist')
        self.data[name] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if self.data.get(name):
            self.data.pop(name)

    def iterator(self, n=1):
        if n <= 0:
            raise ValueError("Incorrect N value. N shuld be greater than 0")
        output = {}
        for index, (key, val) in enumerate(self.data.items()):
            output[key] = val
            if (index + 1) % n == 0:
                yield output
                output = {}
        if output:
            yield output
