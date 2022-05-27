import json
import os.path


def read_input_file():
    # Get the json file path
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "../data/items.json")

    # Open file and get items
    with open(path, 'r') as f:
        items = json.load(f)

    return items


def select_items():
    print("modify funtion here")


def main():
    # Read Input File
    items = read_input_file()

    # e.g. Display all the items
    for item in items:
        print ('\033[33m' + str(item['id']) + '\033[0m', item['name'])

    # e.g. if the user choose vegetable category, display the items of
    # vegetable
    print('\033[1;34m' + "Vegetable:" + '\033[1;34m')
    for item in items:
        if item['category'] == 'vegetable':
            print ('\033[33m' + str(item['id']) + '\033[0m', item['name'])

    # Ask User to Select Items
    select_items()

    # Start Bagging

    # Display Result


if __name__ == '__main__':
    main()