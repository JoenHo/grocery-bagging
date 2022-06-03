
import re
import json
import random
import os.path
from bagger import Bagger


class QA:

    qa_bank = []
    bg : Bagger = None

    def __init__(self, bg : Bagger):
        self.bg = bg
        self.qa_bank = self.read_input_file()
        

    def read_input_file(self):
        # Get the json file path
        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, "../data/qa.json")

        # Open file and read qa list
        with open(path, 'r') as f:
            qas = json.load(f)
        
        return qas


    def get_answer_template(self, question):
        
        # if question contains substring of question in question bank, consider it as a match
        for qa in self.qa_bank:
            if qa['Q'] in question:
                return qa

        return None


    def get_answer(self, question):

        no_ans_list = ["Sorry, I didn't get you.", "Good question, but I don't know the answer.", "I don't have answer to you question.",
        "Your guess is as good as mine.", "I am not the best person to answer that.", "It’s beyond me.", "Hmmm. I'm not sure if I understand the question.", "It’s a mystery to me."]

        # extract item names
        items = []
        for item in self.bg.selected:
            idx = question.find(item.name.lower())
            if idx != -1:
                items.append([item, idx])

        # sort items by index in ascending order (in the order it appears in question statement)
        items.sort(key=lambda x: x[1])

        # replace name of item with *
        for i, item in enumerate(items):
            question = question.replace(item[0].name.lower(), f"[item_{i+1}]")
    
        # get answer template
        qa = self.get_answer_template(question)
        
        if qa == None:
             return random.choice(no_ans_list)

        # check if question type and validity
        if qa['type'] == 'general':
            # directory return answer
            return qa['A']
        if qa['type'] == '<':
            if len(items) != 2:
                return random.choice(no_ans_list)
            # check if score of item_1 < item_2
            if self.bg.calc_item_point(items[0][0]) > self.bg.calc_item_point(items[1][0]):
                return f"That's interesting. {items[0][0].name} should be placed below {items[1][0].name}."
        elif qa['type'] == '>':
            if len(items) != 2:
                return random.choice(no_ans_list)
            # check if score of item_1 > item_2
            if self.bg.calc_item_point(items[0][0]) < self.bg.calc_item_point(items[1][0]):
                return f"That's interesting. {items[0][0].name} should be placed above {items[1][0].name}."
        elif qa['type'] == 'no bag':
            if len(items) != 1:
                return random.choice(no_ans_list)
            # check if item have no bag
            if items[0][0] not in self.bg.outside:
                return f"That's interesting. {items[0][0].name} should be placed in a bag."
        elif qa['type'] == 'separate bag':
            # check if item_1 and item_2 are in different group of categories
            if len(items) != 2:
                return random.choice(no_ans_list)
            for group in self.bg.category_group:
                if items[0][0].category in group and items[1][0].category in group:
                    return f"{items[0][0].name} and {items[1][0].name} could be placed in a same bag because they are in the same group of categories.\nI may have put them in separate bags for distribution purpose."
        elif qa['type'] == 'same bag':
            # check if item_1 and item_2 are in different group of categories
            if len(items) != 2:
                return random.choice(no_ans_list)
            for group in self.bg.category_group:
                if items[0][0].category in group and items[1][0].category not in group:
                    return f"That's interesting. {items[0][0].name} and {items[1][0].name} should be placed in separate bags because they are in different group of categories."           

        # fill the information to answer template
        ans = qa['A']
        for i, item in enumerate(items):
            # construct item info
            info = f" ✔︎ {item[0].name}: Category = {item[0].category}, Volume = {item[0].volume}, Weight = {item[0].weight}, Rigidity = {item[0].rigidity}, Score = {self.bg.calc_item_point(item[0])}"
            ans = ans.replace(f"[item_{i+1}]", item[0].name)
            ans = ans.replace(f"[item_{i+1}_info]", info)

        return ans


    def ask_question(self, question):
        # cast to lower cases
        q = question.lower()

        # remove punctuations except - and '
        q = re.sub(r'[^\w\s\'-]', '', q)

        # find answer and return it
        return self.get_answer(q)
