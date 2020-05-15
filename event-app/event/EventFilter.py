from event.filter_operator import FilterOperator
class EventFilter():
    def __init__(self, key:str, values:[str], operator:FilterOperator):
        self.key = key
        self.values = values
        self.operator = operator
        

