# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class EventItem(scrapy.Item):
    name = scrapy.Field()
    description = scrapy.Field()
    start = scrapy.Field()
    end = scrapy.Field()
    host = scrapy.Field()
    location = scrapy.Field()
    url = scrapy.Field()
    type = scrapy.Field()
    study_program = scrapy.Field()
    class_year = scrapy.Field()
    image_source = scrapy.Field()

    types = {
        'Bedriftspresentasjon': ['bedriftspresentasjon', 'bedpress', 'bedrift', 'næringsliv'],
        'Kurs': ['kurs', 'forelesning'],
        'Fest': ['fest', 'imball', 'immatrikuleringsball'],
        'Konsert': ['album', 'spellemanspris'],
        'Foredrag': ['foredrag', 'samtale', 'presentasjon'],
        'Konkurranse': ['quiz', 'konkurranse', 'premie', 'vinne', 'hackathon']
    }

    @staticmethod
    def discern_type(type, title, description):
        """
        Returns the type induced from the type, title and description
        """
        # First, check the type itself
        type = EventItem.__check_against_keywords(type, strict=True)

        # Then the title
        if type == None:
            type = EventItem.__check_against_keywords(title, strict=True)

        # Then the description
        if type == None:
            type = EventItem.__check_against_keywords(description)
 
        return type if type != None else "Unknown" 
        
    
    @staticmethod
    def __check_against_keywords(str, strict=False):
        """
        Takes a list of words and returns the type with a matching keyword. If the boolean strict is true, the search will require an excact match
        """

        # If nothing is passed, theres no need to do anything
        if str == None:
            return None
        
        # Need to track how well it matches any given type
        scores = {}
        for type in EventItem.types:
            scores[type] = 0

        # Go through a set of the words and the keywords to see if any match
        words = [x.lower() for x in str.split()]
        for type in EventItem.types:
            for word in words:
                for keyword in EventItem.types.get(type):
                    if strict:
                        if keyword == word:
                            scores[type] = scores[type] + 1
                    else:
                        if keyword == word:
                            scores[type] = scores[type] + 10
                        elif keyword in word:
                            scores[type] = scores[type] + 1
       
        # Return the type with the largest score, but only if one of them != 0
        v=list(scores.values())
        k=list(scores.keys())
        best_match = k[v.index(max(v))]
        return best_match if scores[best_match] != 0 else None
