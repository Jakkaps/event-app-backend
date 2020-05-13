from event.filter_operator import FilterOperator
class EventFilter():
    def __init__(self, key:str, value:str, operator:FilterOperator):
        self.key = key
        self.value = value
        self.operator = operator
        

