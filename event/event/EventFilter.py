class EventFilter():
    def __init__(self, key:str, value:str, operator:FilterOperator):
        self.key = key
        self.value = value
        self.operator = operator
        

class FilterOperator():
    LIKE = "LIKE"
    LESS_THAN = "<"
    GREATER_THAN = ">"
