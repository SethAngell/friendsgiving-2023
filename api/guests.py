import json
import re

db_path = "data/guests.json"


class GuestEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


class Guest:
    def __init__(self, name: str = None, phone_number: str = None, json_guest: dict=None):
        if (json_guest != None):
            print(f'JSON GUEST: {json_guest}')
            self.name = json_guest["name"]
            self.phone_number = json_guest["phone_number"]
        else:
            self.name = name
            self.phone_number = phone_number

    def __str__(self):
        return self.name

    def serialize(self):
        return {"name": self.name, "phone_number": self.phone_number}


class GuestList:
    def __init__(self, json_guest_list: list[dict]):
        print('GuestList', json_guest_list)
        self.guest_list: list[Guest] = [
            Guest(None, None, json_guest=json_guest) for json_guest in json_guest_list
        ]
    
    def find_guest_in_guestlist(self, phone_number: str) -> Guest:
        for guest in self.guest_list:
            if guest.phone_number == phone_number: 
                return guest
        
        return None

    def serialize(self):
        return json.dumps(self, indent=4, cls=GuestEncoder)


def read_database():
    with open(db_path, "r") as db_file:
        return json.load(db_file)

def write_database(new_guest_list: GuestList):
    with open(db_path, 'w') as db_file:
        db_file.write(new_guest_list.serialize())


def get_guest_list() -> GuestList:
    return GuestList(read_database()['guest_list'])


def get_guest_by_phone_number(phone_number: str) -> Guest:
    guests = get_guest_list()
    return guests.find_guest_in_guestlist(phone_number)
    

def sanitize_phone_number(phone_number: str) -> str:
    result = re.match(r"(?P<first>[0-9]{3})(-|.|\s)?(?P<second>[0-9]{3})(-|.|\s)?(?P<third>[0-9]{4})", phone_number)
    try:
        groups = result.groupdict()
        sanitized_phone_number = ".".join([groups['first'], groups['second'], groups['third']])
        return sanitized_phone_number
    except AttributeError as e:
        return 'ERROR: Unable to parse phone number'
    
def add_guest_to_guest_list(request_body: dict):
    sanitized_phone_number = sanitize_phone_number(request_body["phone_number"])
    existing_user = get_guest_by_phone_number(sanitized_phone_number)
    if (existing_user == None):
        guests = get_guest_list()
        print(request_body["name"])
        new_guest = Guest(request_body['name'], sanitized_phone_number)
        guests.guest_list.append(new_guest)
        write_database(guests)



    
