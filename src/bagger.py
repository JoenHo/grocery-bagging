from item import Item
from typing import List

# --- CONSTANT --- #
BAG_VOLUME_CAPACITY = 17
BAG_WEIGHT_CAPACITY = 30

W_WEIGHT = 0.5
W_VOLUME = 0.5
W_RIGIDITY = 0.8
W_CONTAINER = 0.3
# ---------------- #


class Bagger:

    all_items : List[Item] = []
    selected = {}
    bags = []
    outside = []
    

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


    def calc_item_point(self, item : Item):
        # W_CONTAINER * item.container
        point = W_WEIGHT * item.weight + W_VOLUME * item.volume + W_RIGIDITY * item.rigidity
        return point


    def sorting_items(self, item_list):

        print("Before Sort")
        for item in item_list:
            print(f"Name: {item[0].name} Points: {item[2]}")

        # sort item list by points in descending order
        item_list.sort(key=lambda x: x[2], reverse=True)

        print(f"After Sort")
        for item in item_list:
            print(f"Name: {item[0].name} Points: {item[2]}")

    
    def estimate_num_bags(self, item_list):
        total_weight, total_volume = 0, 0

        for item in item_list:
            if(item[0].volume <= BAG_VOLUME_CAPACITY and item[0].weight <= BAG_WEIGHT_CAPACITY):
                total_volume += (item[0].volume * item[1])
                total_weight += (item[0].weight * item[1])

        volume_bag = int(total_volume / BAG_VOLUME_CAPACITY) + (
                    total_volume %
                    BAG_VOLUME_CAPACITY > 0)
        weight_bag = int(total_weight / BAG_WEIGHT_CAPACITY) + (
                    total_weight %
                    BAG_WEIGHT_CAPACITY > 0)
        return max(volume_bag, weight_bag)


    def put_items_into_bags(self, item_list, num_bags, type): # item_list: list of [Item, quantity, points]
        i = 0
        bags = [[[], BAG_VOLUME_CAPACITY, BAG_WEIGHT_CAPACITY, type] for _ in range(num_bags)]    # List of [List of [Item], volume left, weight left, type]
        for item in item_list:
            # if item is larger and heavier than limit capacity of bag
            if item[0].weight > BAG_WEIGHT_CAPACITY or item[0].volume > BAG_VOLUME_CAPACITY:
                # leave it out
                for _ in range(item[1]):
                    self.outside.append(item[0])
                continue
                
            # until item quantity becomes zero find a bag to put
            count = 0
            while item[1] > 0:
                count += 1
                if(count >= len(bags)):
                    bags.append([[], BAG_VOLUME_CAPACITY, BAG_WEIGHT_CAPACITY, type])
                    num_bags += 1
                    count = 0

                # if possible to put in this bag
                if bags[i][1] > item[0].volume and bags[i][2] > item[0].weight:
                    # place item into bag
                    bags[i][0].insert(0, item[0])
                    # reduce bag space
                    bags[i][1] -= item[0].volume
                    bags[i][2] -= item[0].weight
                    # reduce quantity by 1
                    item[1] -= 1
                    # reset count to zero
                    count = 0
                
                # move to next bag
                if i < num_bags -1:
                    i+=1
                else:
                    i = 0
        self.bags += bags



    def meat_seafood_bagging(self, meat_seafood_list):
        print('\nStart bagging meat and seafood items')
        for item in meat_seafood_list:
            print(f"name: {item[0].name}")
            print(f"quantity: {item[1]}")
        


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


    def process_items(self, item_list, type):
        # sort item list
        self.sorting_items(item_list)

        # estimate number of bags
        num_bags = self.estimate_num_bags(item_list)

        # put items to bags in order
        self.put_items_into_bags(item_list, num_bags, type)


    def grouping_items(self):
        item: Bagger.selected
        items = self.selected

        meat_seafood_list = []
        frozen_list = []
        food_list = []
        non_food_list = []

        for item, quantity in items.items():
            # calculate item points and assign all related information to array
            item_info = [item, quantity, self.calc_item_point(item)]   # [item, quantity, point]

            # classify item by category
            if item.category == 'meat' or item.category == 'seafood':
                meat_seafood_list.append(item_info)
            elif item.category == 'frozen':
                frozen_list.append(item_info)
            elif item.category == 'vegetable' or item.category == 'fruit' \
                    or item.category == 'dairy' or item.category == \
                    'beverage' or item.category == 'snack' or item.category\
                    == 'other_food' or item.category == 'baked':
                food_list.append(item_info)
            else:
                non_food_list.append(item_info)
        
        # bagging by group
        for group in [[food_list, "food"], [meat_seafood_list, "meat&seafood"], [frozen_list, "frozen"], [non_food_list, "non-food"]]:
            self.process_items(group[0], group[1])

        # if len(meat_seafood_list):
        #     self.meat_seafood_bagging(meat_seafood_list)
        # if len(frozen_list):
        #     self.frozen_bagging(frozen_list)
        # if len(food_list):
        #     self.food_bagging(food_list)
        # if len(non_food_list):
        #     self.non_food_bagging(non_food_list)


    def start_bagging(self, op):
        #reset bags and outside list
        self.bags.clear()
        self.outside.clear()

        if op == 1: # Passive Constraints Enforcement
            self.grouping_items()
            

