import json
from guests import Guest, get_guest_by_phone_number, sanitize_phone_number

db_path = "data/menu.json"


class MenuEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


class MenuItem:
    def __init__(self, item: str, type: str, chef: Guest, json_item: dict=None):
        if json_item != None:
            print(f'JSONE ITEM: {json_item}')
            self.item = json_item["item"]
            self.type = json_item["type"]
            self.chef = Guest( None, None,json_item["chef"])
        else:
            self.item = item
            self.type = type
            self.chef = chef
        

    def __str__(self):
        return f"{self.chef} is bringing {self.item}"

    def serialize(self):
        return {"item": self.item, "type": self.type, "chef": self.chef.serialize()}


class Menu:
    def __init__(self, items: list[MenuItem]):
        self.items = items

    def serialize(self) -> str:
        return json.dumps(self, indent=4, cls=MenuEncoder)


def read_database():
    with open(db_path, "r") as db_file:
        return json.load(db_file)


def get_menu():
    raw_menu = read_database()

    menu: list[MenuItem] = []
    for item in raw_menu["items"]:
        menu.append(MenuItem(None, None, None, item))

    return Menu(menu)


def write_database(current_menu: Menu, new_items: list[MenuItem]):
    current_menu.items = current_menu.items + new_items
    
    with open(db_path, 'w') as db_file:
        db_file.write(current_menu.serialize());


def add_all_items_to_menu(request_body: dict):
    index = 1
    more_items = True
    item_keys = request_body.keys()
    phone_number = sanitize_phone_number(request_body['phone_number'])
    guest = get_guest_by_phone_number(phone_number)
    item_list = []

    while more_items:
        if f'new-item-type-{index}' in item_keys:
            item_name = request_body[f'new-item-{index}']
            item_type = request_body[f'new-item-type-{index}']

            item_list.append(MenuItem(item_name, item_type, guest))
                
            index += 1
        else:
            more_items = False
        
    current_menu = get_menu()
    write_database(current_menu, item_list)
        

    print(request_body.keys())
