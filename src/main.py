import json
import os.path
from rich import box
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from bagger import Bagger
from item import ItemDecoder, Item
from qa import QA


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
    table = Table(title="SELECTED ITEMS",title_style="bold reverse pale_green3", min_width=40)
    table.add_column("#", header_style="bold yellow", justify="center", style="yellow")
    table.add_column("Item Name", header_style="bold", justify="left")
    table.add_column("Quantity", header_style="bold", justify="center")
    table.box = box.MINIMAL_HEAVY_HEAD

    item : Bagger.selected
    for item in items:
        item_id = str(item.id)
        name = item.name
        quantity = str(items[item])
        table.add_row(item_id, name, quantity)
    table.row_styles="b"
    table.caption_style = "bold"
    table.caption = "You have selected [cyan]" + str(len(items)) + "[/cyan] different items!"

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


def bagging_menu():
    table = Table(title="MENU", title_style="bold reverse steel_blue1", min_width=45)
    table.add_column("#", header_style="bold yellow", justify="center", style="yellow")
    table.add_column("BAGGING METHOD OPTIONS", header_style="bold", justify="left")
    table.box = box.HORIZONTALS
    menu_list = ["Passive Constraints Enforcement"]

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
    console = Console()
    menu = bagging_menu()
    cart = get_selected_items(bg.get_selected())
            
    while(True):
        try:
            # display menu
            console.clear()
            console.print(Columns([Panel(menu, expand=True), Panel(cart, expand=True)]), justify="center")
            
            # ask user to select option
            op_no = int(console.input("\nSelect Option # : "))
            if(op_no == 1):
                bg.start_bagging(1)
                display_result(bg)
            elif(op_no == 0):
                break

        except ValueError:
            console.print("Invalid Input", style="red")


def bag_table(bag, no):
    if bag[3] == "food":
        table = Table(title=f"🍓🥦 BAG #{no} 🍪🥛", title_style="bold reverse light_goldenrod2", width=35)
        table.add_column("ITEM NAME", header_style="bold", justify="center", style="")
        table.box = box.HORIZONTALS
    elif bag[3] == "meat&seafood":
        table = Table(title=f"🥩 BAG #{no} 🐟", title_style="bold reverse misty_rose3", width=35)
        table.add_column("ITEM NAME", header_style="bold", justify="center", style="")
        table.box = box.HORIZONTALS
    elif bag[3] == "frozen":
        table = Table(title=f"BAG #{no} 🧊", title_style="bold reverse honeydew2", width=35)
        table.add_column("ITEM NAME", header_style="bold", justify="center", style="")
        table.box = box.HORIZONTALS
    elif bag[3] == "non-food":
        table = Table(title=f"BAG #{no} 🏠", title_style="bold reverse khaki1", width=35)
        table.add_column("ITEM NAME", header_style="bold", justify="center", style="")
        table.box = box.HORIZONTALS

    total_vol, total_wei = 0, 0
    for item in bag[0]:
        table.add_row(item.name)
        total_vol += item.volume
        total_wei += item.weight
    table.row_styles="b"
    table.show_header=False
    table.caption_style = "bold"
    table.caption = f"Volume:{total_vol} 🧅 Weight:{round(total_wei,2)} 🧅"
    
    return table


def no_bag_table(outside):
    table = Table(title=f"NO BAG", title_style="bold reverse pale_violet_red1", width=35)
    table.add_column("ITEM NAME", header_style="bold", justify="center", style="")
    table.box = box.HORIZONTALS

    total_vol, total_wei = 0, 0
    for item in outside:
        table.add_row(item.name)
        total_vol += item.volume
        total_wei += item.weight
    table.row_styles="b"
    table.show_header=False
    table.caption_style = "bold"
    table.caption = f"Volume:{total_vol} 🧅 Weight:{round(total_wei,2)} 🧅"
    
    return table


def format_bags(bg:Bagger):
    panels = []
    for i, bag in enumerate(bg.bags):
        panels.append(Panel(bag_table(bag, i+1), expand=False))
    
    if len(bg.outside) > 0: 
        panels.append(Panel(no_bag_table(bg.outside), expand=False))

    return panels


def display_result(bg:Bagger):
    qa = QA(bg)    
    console = Console()
    console.clear()

    # display result
    console.print(Columns(format_bags(bg)), justify="center")
    console.print('\nEnter 0 to go back\nEnter [b][cyan]FAQ[/cyan][/b] to see list of FAQ')

    # Q&A
    while(True):
        try:
            res = console.input("\nAsk Question >> ")
            if res == '0':
                break
            else:
                console.print(qa.ask_question(res), style="cadet_blue")
        except ValueError:
            console.print("Invalid Input", style="red")


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

    # mock selected for testing
    # mock_selected = [[1,3],[2,3],[3,1],[4,1],[5,1],[6,1],[7,2],[9,1],[10,2],[11,1],[12,1],[13,1],[14,1],[15,1],[17,3],[18,1],[20,1],[21,1],[23,1],[26,2],[27,1],[28,1],[30,1],[31,1],[33,1],[34,1],[35,1],[36,1],[36,1],[38,1],[39,1],[40,1],[43,1],[45,1]]
    # for item in mock_selected:
    #     bg.add_to_selected(next((x for x in items if x.id == item[0]), None), item[1])

    # Display Main Menu
    display_main_menu(bg)


if __name__ == '__main__':
    main()