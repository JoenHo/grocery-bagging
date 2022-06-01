from item import Item
from typing import List

class Bagger:

    all_items : List[Item] = []
    selected = {}
    bags = []
    BAG_VOLUME_CAPACITY = 50
    BAG_WEIGHT_CAPACITY = 30

    def __init__(self, items):
        self.all_items = items


    def get_all_items(self):
        return self.all_items


    def add_to_selected(self, item : Item, quantity):
        if item in self.selected:
            q = self.selected[item] + quantity
        else:
            q = quantity
        # add / update selected set
        self.selected[item] = q
        if self.selected[item] <= 0:
        # remove item from set
            self.selected.pop(item)


    def get_selected(self):
        return self.selected


    def sorting(self, item_list):
        # Return sorted item list
        # Sort: point =  0.5 * weight + 0.5 * volume + rigidity
        print()


    def meat_seafood_bagging(self, meat_seafood_list):
        total_weight, total_volume = 0, 0

        self.sorting(meat_seafood_list)

        print('\nStart bagging meat and seafood items')
        for item in meat_seafood_list:
            total_volume += (item[0].volume * item[1])
            total_weight += (item[0].weight * item[1])
            print(f"name: {item[0].name}")
            print(f"quantity: {item[1]}")

        volume_bag = int(total_volume / self.BAG_VOLUME_CAPACITY) + (
                    total_volume %
                    self.BAG_VOLUME_CAPACITY > 0)
        weight_bag = int(total_weight / self.BAG_WEIGHT_CAPACITY) + (
                    total_weight %
                    self.BAG_WEIGHT_CAPACITY > 0)
        estimate_bag = max(volume_bag, weight_bag)
        print(f"Estimated bags: {estimate_bag}")


    def frozen_bagging(self, frozen_list):
        print('\nStart bagging frozen items')
        for item in frozen_list:
            print(f"name: {item[0].name}")
            print(f"quantity: {item[1]}")


    def food_bagging(self, food_list):
        print('\nStart bagging food items')
        for item in food_list:
            print(f"name: {item[0].name}")
            print(f"quantity: {item[1]}")

    def non_food_bagging(self, non_food_list):
        print('\nStart bagging non-food items')
        for item in non_food_list:
            print(f"name: {item[0].name}")
            print(f"quantity: {item[1]}")


    def grouping_items(self):
        item: Bagger.selected
        items = self.selected

        meat_seafood_list = []
        frozen_list = []
        food_list = []
        non_food_list = []

        for item in items.items():
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
            self.meat_seafood_bagging(meat_seafood_list)
        if len(frozen_list):
            self.frozen_bagging(frozen_list)
        if len(food_list):
            self.food_bagging(food_list)
        if len(non_food_list):
            self.non_food_bagging(non_food_list)


    def start_bagging(self, op):
        
        if op == 1: # Passive Constraints Enforcement
            self.grouping_items()
            

