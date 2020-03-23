import datetime
import re

class DateHelper:

    def __init__(self):
        self.current_date = datetime.datetime.now()
        self.norwegian_months = [
            'januar', 'februar', 'mars', 'april',
            'mai', 'juni', 'juli', 'august', 'september'
            'oktober', 'november', 'desember'
            ]

    def format_to_sql(self, date):
        pass
    
    def milli_as_sql_date(self, milli):
        """
        Takes millisecond and converts to date with format YYYY-MM-DD HH:MI:SS""
        """

        as_date = datetime.datetime.fromtimestamp(milli/1000.0)
        return as_date.strftime('%Y-%m-%d %H:%M:%S')

    def norwegian_month_as_sql_date(self, norwegian_date):
        """
        Takes a string with a norwegian date, like 'Mar 21' and retunrs as date
        """


        norwegian_date = norwegian_date.lower()

        month_str = "".join(filter(str.isalpha, norwegian_date))
        month_number = 0
        for (index, month) in enumerate(self.norwegian_months):
            if month_str in month:
                month_number = index + 1
                break
        
        day = int(re.findall(r'\d+', norwegian_date)[0])
        
        return self.current_date.replace(month=month_number, day=day)
        