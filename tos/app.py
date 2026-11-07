import re

from textual.app import App, ComposeResult

from rich.text import Text
import textual.containers as containers
import textual.widgets as widgets
from textual.screen import ModalScreen



menu = {"pizza": 10,
        "burger": 8,
        "salad": 6,
        "pasta": 12,
        "sushi": 15
        }


cart = {}

      

def add_item(self,item: str):
    _quantity = int(re.search(r"\d+", item).group(0) if re.search(r"\d+", item) else 1) # type: ignore
    item = re.sub(r"\d", "", item)

    if item in cart:
        cart[item][1] += _quantity
        print(f"{item} has been added to your cart")
    
    elif item in menu:
        cart[item] = [menu[item], _quantity]
        print(f"{item} has been added to your cart")

    else:
        self.notify(f"{item} is not on the menu", severity="warning")
        print(f"{item} is not on the menu")



def remove_item(self,item: str):
    _item = re.sub(r"\d", "", item)
    if _item not in cart:
        self.notify(f"{item} is not on the cart", severity="warning")
        print("item not in cart")
        return

    _quantity = int(re.search(r"\d+", item).group(0) if re.search(r"\d+", item) else 1) # type: ignore

    if _quantity:
        cart[_item][1] -= _quantity
        print(f"{_quantity} {_item} has been removed from your cart")
        if cart[_item][1] <= 0:
            cart.pop(_item)
            print(f"{_item} has been removed from your cart")
    else:
        cart.pop(_item)
        print(f"{_item} has been removed from your cart")


def update_cart(ui_cart, total_price):
    ui_cart.clear(False)
    # print(cart.items())
    total = 0
    for i, (name, item) in enumerate(cart.items()):
        subtotal = item[0] * item[1]
        total += subtotal
        print(name, item)
        ui_cart.add_row(i+1, name, str(item[0]), str(item[1]), str(subtotal) +"$")

    total_price.update(f"Total\t\t: {total}$")

    



class TOS(App):
    CSS_PATH = "style.tcss"

    def compose(self) -> ComposeResult:

        with containers.Container(id="container"):
            with containers.Container(id="main-dock"):
                self.menu_table = widgets.DataTable(id="menu")
                self.menu_table.border_title = "Menu"

                guide = widgets.Static("-- buy <item><quantity>\n\tbuy pizza2 salad5 or buy pizza\n\n-- remove <item><quantity>\n\tremove pizza2 or remove pizza to remove all\n\n-- checkout", id="guide")
                guide.border_title = "Command"

                yield self.menu_table
                yield guide


                with containers.VerticalScroll(id="history-container"):
                    self.history = widgets.Static("", id="history")
                    yield self.history
                
            
            with containers.Container(id="right-dock"):
                self.ui_cart = widgets.DataTable(id="cart")
                self.ui_cart.border_title = "Cart"

                self.total_price = widgets.Static("Total\t\t: ", id="totalprice")

                yield self.ui_cart
                yield self.total_price


        command_field = widgets.Input(placeholder="Enter your command", id="command-field")

        yield command_field

    def on_mount(self) -> None:
        self.menu_table.add_columns("No", "Menu        ", "Price")
        self.ui_cart.add_columns("No", "Name    ", "Price        ", "Quantity       ", "Subtotal")


        scroll = self.query_one("#history-container", containers.VerticalScroll)
        scroll.scroll_end(animate=True)
        scroll.border_title = "Command History"
        for i, (name, price) in enumerate(menu.items()):

            self.menu_table.add_row(i+1, name, str(price)+"$")



    def on_input_submitted(self, event: widgets.Input.Submitted) -> None:
        new_history = Text(str(self.history.content) + "\n" + event.value)
        

        value = event.value.lower().split(" ")
        event.input.clear()

        command_args = value[0]
        item_args = value[1:]

        print(command_args , "command_args")

        if command_args == "buy":
            self.history.update(new_history)
            for item in value[1:]:
                print(item)
                add_item(self,item)
            update_cart(self.ui_cart, self.total_price)

        elif command_args == "remove":
            self.history.update(new_history)
            for item in item_args:
                remove_item(self,item)
            update_cart(self.ui_cart, self.total_price)

        elif command_args == "checkout":
            self.history.update(new_history)
            if not cart:
                self.notify("Your cart is empty", severity="warning")
                return
            self.push_screen(Checkout(cart))        
        else:
            self.notify(f"{value} <- Invalid Command", severity="warning")



class Checkout(ModalScreen):

    def __init__(self, cart: dict) -> None:
        super().__init__()
        self.cart = cart

    def compose(self) -> ComposeResult:
        total = sum(price * qty for price, qty in self.cart.values())
        with containers.Container(id="dialog"):
            yield widgets.Label("Thanks for buying in this restaurant\n")
            yield widgets.DataTable(id="summary")
            yield widgets.Static(f"Tax\t\t: \nTotal\t\t: {total}$", id="grand-total")

    def on_mount(self) -> None:
        table = self.query_one("#summary", widgets.DataTable)
        table.show_cursor = False
        table.add_columns("Name", "Price", "Qty", "Subtotal")
        for name, (price, qty) in self.cart.items():
            table.add_row(name, f"{price}$", str(qty), f"{price * qty}$")



def main():
    TOS().run()


if __name__ == "__main__":
    main()