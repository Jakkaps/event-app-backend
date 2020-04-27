# coding: utf-8

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
        self.english_months = [
            'january', 'february', 'march', 'april',
            'may', 'june', 'july', 'august', 'september',
            'october', 'november', 'december'
        ]
    
    def milli_as_sql_date(self, milli):
        """
        Takes millisecond and converts to date with format 'YYYY-MM-DD HH:MI:SS'
        """

        as_date = datetime.datetime.fromtimestamp(milli/1000.0)
        return as_date.strftime('%Y-%m-%d %H:%M:%S')
    
    def __month_number_norwegian(self, month_str):
        month_number = 0
        month_str = month_str.lower()
        for (index, month) in enumerate(self.norwegian_months):
            if month_str in month:
                month_number = index + 1
                break
        
        return month_number
    
    def __month_number_english(self, month_str):
        month_number = 0
        month_str = month_str.lower()
        for (index, month) in enumerate(self.english_months):
            if month_str in month:
                month_number = index + 1
                break

        return month_number 
    
    def hour_str_hour_minute(self, str):
        """
        Takes in a string om the format '9:00 PM UTC+01' and returns the hour in 24h format and minute
        """
        hour_str, minute_str, am_pm = re.findall(".*(\d+):(\d+) (\w{2})", str)[0]
        return int(hour_str) + (0 if am_pm == 'AM' or hour_str=='12' else 12), int(minute_str)

    def english_str_as_sql_date(self, str):
        """
        Converts an english string on the format 'Thursday, February 13, 2020 at 12:00 PM' 
        and converts to format 'YYYY-MM-DD HH:MI:SS' 
        """
        
        # Find all by regex
        month_str, day_str, year_str, hour_str, minute_str, am_pm = re.findall("\w+, (\w+) (\d+), (\d+) at (\d+):(\d+) (\w{2})", str)[0]
        
        month = self.__month_number_english(month_str)
        day = int(day_str)
        year = int(year_str)
        hour = int(hour_str) + (0 if am_pm == 'AM' or hour_str=='12' else 12) # Add 12 hours if start of day to get 24h format
        minute = int(minute_str)

        return self.current_date.replace(year=year, month=month, day=day, hour=hour, minute=minute, second=0) 


    def norwegian_month_as_sql_date(self, norwegian_date):
        """
        Takes a string with a norwegian date, like 'Mar 21' and retunrs as date
        """

        month_str = "".join(filter(str.isalpha, norwegian_date))
        month_number = self.__month_number_norwegian(month_str)
        
        day = int(re.findall(r'\d+', norwegian_date)[0])
        
        return self.current_date.replace(month=month_number, day=day, minute=0, second=0)
