import re

menu = {"pizza": 10, "burger": 8, "salad": 6, "pasta": 12, "sushi": 15}
cart = {}



def main():
    print("welcome to the restaurant!")


    while True:
        _user_input = get_user_input("enter your command: ")

        args = _user_input.lower().split(" ")

        print(args)
        if args is None:
            print("invalid command")
            continue

        command_args = args[0]
        item_args = args[1:]

        print(command_args , "command_args")

        if command_args == "menu":
            print("heres the menu:")
            for item, price in menu.items():
                print(f"{item}: ${price}")

        elif command_args == "buy":
            print(item_args) 
            for item in item_args:
               add_item(item)

        elif command_args == "remove":
            for item in item_args:
                if item in cart:
                    remove_item(item)
                else:
                    print(f"{item} is not in your cart")

        elif command_args == "cart":
            print("your cart:")
            print(cart)

        

def add_item(item: str):
    _quantity = int(re.search(r"\d+", item).group(0) if re.search(r"\d+", item) else 1) # type: ignore
    item = re.sub(r"\d", "", item)

    if item in cart:
        cart[item][1] += _quantity
        print(f"{item} has been added to your cart")
    
    elif item in menu:
        cart[item] = [menu[item], _quantity]
        print(f"{item} has been added to your cart")

    else:
        print(f"{item} is not on the menu")



def remove_item(item: str):
    if re.search(r"\d+", item):
        _quantity = int(re.search(r"\d+", item).group(0)) #type: ignore
        cart[item][1] -= _quantity
        print(f"{_quantity} {item} has been removed from your cart")
        if cart[item][1] <= 0:
            cart.pop(item)
            print(f"{item} has been removed from your cart")
    else:
        cart.pop(item)
        print(f"{item} has been removed from your cart")


def get_user_input(info: str):
    user_input = input(info)
    return user_input


main()