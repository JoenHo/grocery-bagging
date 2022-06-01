import json
import os.path
from rich import box
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from bagger import Bagger
from item import ItemDecoder, Item


def read_input_file():
    # Get the json file path
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "../data/items.json")

    # Open file and get items
    with open(path, 'r') as f:
        items = json.load(f, cls=ItemDecoder)
    
    return items


def get_item_table(items):

    table = Table(title="ITEM LIST",title_style="bold reverse steel_blue1")
    table.add_column("#", header_style="bold yellow", justify="center", style="yellow")
    table.add_column("Item Name", header_style="bold", justify="left")
    table.add_column("Category", header_style="bold", justify="center")
    table.add_column("Container Type", header_style="bold", justify="center")
    table.add_column("Volume ×🧅", header_style="bold", justify="center")
    table.add_column("Weight ×🧅", header_style="bold", justify="center")
    table.add_column("Rigidity (1-5)", header_style="bold", justify="center")
    table.box = box.MINIMAL_HEAVY_HEAD

    item : Item
    for item in items:
        item_id = str(item.id)
        name = item.name
        category = item.category
        container = item.container
        volume = str(item.volume)
        weight = str(item.weight)
        rigidity = str(item.rigidity)
        table.add_row(item_id, name, category, container, volume, weight, rigidity)
    table.add_row()
    table.add_row("[orange4]0[/orange4]", "[orange4]Return to Previous Menu[/orange4]")
    table.row_styles="b"

    return table


def get_selected_items(items):
    table = Table(title="SELECTED ITEMS",title_style="bold reverse pale_green3", min_width=35)
    table.add_column("#", header_style="bold yellow", justify="center", style="yellow")
    table.add_column("Item Name", header_style="bold", justify="left")
    table.add_column("Quantity", header_style="bold", justify="left")
    table.box = box.MINIMAL_HEAVY_HEAD

    item : Bagger.selected
    for item in items:
        item_id = str(item.id)
        name = item.name
        quantity = str(items[item])
        table.add_row(item_id, name, quantity)
    table.row_styles="b"
    table.caption_style = "bold"
    table.caption = "You have selected [cyan]" + str(len(items)) + "[/cyan] items!"

    return table


def main_menu():
    table = Table(title="WELCOME TO GROCERY BAGGING PROGRAM", title_style="bold reverse steel_blue1", min_width=45)
    table.add_column("#", header_style="bold yellow", justify="center", style="yellow")
    table.add_column("MENU OPTIONS", header_style="bold", justify="left")
    table.box = box.HORIZONTALS
    menu_list = ["Select Items", "Start Bagging"]

    for i, option in enumerate(menu_list):
        no = "[yellow]" + str(i + 1) + "[/yellow]"
        table.add_row(no, option)
    table.add_row()
    table.add_row("[orange4]0[/orange4]", "[orange4]Exit[/orange4]")
    table.row_styles="b"
    
    return table


def sub_menu():
    table = Table(title="MENU", title_style="bold reverse steel_blue1", min_width=45)
    table.add_column("#", header_style="bold yellow", justify="center", style="yellow")
    table.add_column("MENU OPTIONS", header_style="bold", justify="left")
    table.box = box.HORIZONTALS
    menu_list = ["Select From: All Categories", "Select From: Vegetables & Fruits", "Select From: Meat & Seafood", "Select From: Frozen",
     "Select From: Other Foods", "Select From: Household Products", "Clear All Selected Items"]

    for i, option in enumerate(menu_list):
        no = "[yellow]" + str(i + 1) + "[/yellow]"
        table.add_row(no, option)
    table.add_row()
    table.add_row("[orange4]0[/orange4]", "[orange4]Return to Main Menu[/orange4]")
    table.row_styles="b"
    
    return table


def display_main_menu(bg:Bagger):
    console = Console()
    menu = main_menu()

    while(True):
        try:
            # display menu
            console.clear()
            console.print(Columns([Panel(menu, expand=True)]), justify="center")
            
            # ask user to select option
            op_no = int(console.input("\nSelect Option # : "))
            if(op_no == 1):
                display_sub_menu(bg)
            elif(op_no == 2):
                display_start_bagging(bg)
            elif(op_no == 0):
                break

        except ValueError:
            console.print("Invalid Input", style="red")


def display_sub_menu(bg:Bagger):
    console = Console()
    menu = sub_menu()

    while(True):
        try:
            # display menu
            console.clear()
            cart = get_selected_items(bg.get_selected())
            console.print(Columns([Panel(menu, expand=True), Panel(cart, expand=True)]), justify="center")
            
            # ask user to select option
            op_no = int(console.input("\nSelect Option # : "))
            if(op_no == 1):
                select_items(bg, bg.all_items)
            elif(op_no == 2):
                items = [x for x in bg.all_items if x.category in ['vegetable','fruit']]
                select_items(bg, items)
            elif(op_no == 3):
                items = [x for x in bg.all_items if x.category in ['meat','seafood']]
                select_items(bg, items)
            elif(op_no == 4):
                items = [x for x in bg.all_items if x.category in ['frozen']]
                select_items(bg, items)
            elif(op_no == 5):
                items = [x for x in bg.all_items if x.category in ['dairy','beverage', 'baked', 'snack', 'other_food']]
                select_items(bg, items)
            elif(op_no == 6):
                items = [x for x in bg.all_items if x.category in ['kitchen','personal','cleaning','other_nonfood']]
                select_items(bg, items)
            elif(op_no == 7):
                bg.selected.clear()
            elif(op_no == 0):
                break

        except ValueError:
            console.print("Invalid Input", style="red")


def display_start_bagging(bg:Bagger):
    item: Bagger.selected
    items = bg.get_selected()

    meat_seafood_list = []
    frozen_list = []
    food_list = []
    non_food_list = []

    for item in items:
        if item[0].category == 'meat' or item[0].category == 'seafood':
            meat_seafood_list.append(item)
        elif item[0].category == 'frozen':
            frozen_list.append(item)
        elif item[0].category == 'vegetable' or item[0].category == 'fruit' \
                or item[0].category == 'dairy' or item[0].category == \
                'beverage' or item[0].category == 'snack' or item[0].category\
                == 'other_food':
            food_list.append(item)
        else:
            non_food_list.append(item)

    if len(meat_seafood_list):
        bg.meat_seafood_bagging(meat_seafood_list)
    if len(frozen_list):
        bg.frozen_bagging(frozen_list)
    if len(food_list):
        bg.food_bagging(food_list)
    if len(non_food_list):
        bg.non_food_bagging(non_food_list)


def select_items(bg:Bagger, item_list):
    
    console = Console()
    item_tb = get_item_table(item_list)

    while(True):
        try:
            # refresh and display item list and selected list
            console.clear()
            cart = get_selected_items(bg.get_selected())
            console.print(Columns([Panel(item_tb, expand=True), Panel(cart, expand=True)]), justify="center")

            # ask user to add items
            item_no = int(console.input("\nEnter Item # : "))
            if(item_no == 0): break
            item_qty = int(console.input("Enter Quantity: "))

            # find item and put in the selected list
            selected = next((x for x in item_list if x.id == item_no), None)
            if(selected == None): raise ValueError("incorrect item number.")
            bg.add_to_selected(selected, item_qty)

        except ValueError:
            console.print("Invalid Input", style="red")


def main():
    # Read Input File
    items = read_input_file()

    # Create Bagger Instance
    bg = Bagger(items)

    # Display Main Menu
    display_main_menu(bg)

    # # Mock that user selected item
    # item1 = 1
    # item2 = 3
    # item3 = 23
    # item4 = 20
    # item5 = 7
    # selected = next((x for x in items if x.id == item1), None)
    # bg.add_to_selected(selected, 5)
    # selected = next((x for x in items if x.id == item2), None)
    # bg.add_to_selected(selected, 1)
    # selected = next((x for x in items if x.id == item3), None)
    # bg.add_to_selected(selected, 2)
    # selected = next((x for x in items if x.id == item4), None)
    # bg.add_to_selected(selected, 1)
    # selected = next((x for x in items if x.id == item5), None)
    # bg.add_to_selected(selected, 2)

    display_start_bagging(bg)

    # Ask User to Select Items

    # Start Bagging

    # Display Result


if __name__ == '__main__':
    main()