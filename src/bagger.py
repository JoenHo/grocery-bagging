from item import Item
from typing import List

class Bagger:

    all_items : List[Item] = []
    selected = []
    bags = []
    BAG_VOLUME_CAPACITY = 50
    BAG_WEIGHT_CAPACITY = 30

    def __init__(self, items):
        self.all_items = items

    def get_all_items(self):
        return self.all_items

    def add_to_selected(self, item : Item, quantity):
        self.selected.append([item, quantity])

    def get_selected(self):
        return self.selected
