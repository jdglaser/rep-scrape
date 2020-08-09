class SubItem:
    def __init__(self, name: str, in_stock: bool):
        self.name = name
        self.in_stock = in_stock
    
    def __repr__(self):
        return f"\tSub-Item: {self.name} - In Stock: {self.in_stock}"
    
    def to_json(self):
        return {
            "name": self.name,
            "in_stock": self.in_stock
        }