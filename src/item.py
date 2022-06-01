import json

class Item():
    def __init__(self, id, name, category, container, volume, weight, rigidity, image) -> None:
        self.id = id
        self.name = name
        self.category = category
        self.container = container
        self.volume = volume
        self.weight = weight
        self.rigidity = rigidity
        self.image = image

    
    def __eq__(self, __o: object) -> bool:
        # use id for equality check
        return isinstance(object, Item) and self.id == object.id


    def __hash__(self) -> int:
        # use id for hashcode
        return hash(self.id)


class ItemDecoder(json.JSONDecoder):
    def __init__(self, object_hook=None, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, o):
        decoded_item=  Item(
            o.get('id'), 
            o.get('name'), 
            o.get('category'),
            o.get('container'),
            o.get('volume'),
            o.get('weight'),
            o.get('rigidity'),
            o.get('image'),
        )
        return decoded_item