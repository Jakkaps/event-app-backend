# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class Event(scrapy.Item):
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

    types = {
        'Bedriftspresentasjon': ['bedriftspresentasjon', 'bedpress', 'bedrift', 'næringsliv'],
        'Kurs': ['kurs', 'forelesning'],
        'Fest': ['fest', 'ball'],
        'Konsert': ['album', 'spellemanspris']
    }

    @staticmethod
    def discern_type(type, title, description):
        """
        Returns the type induced from the type, title and description
        """
        # First, check the type itself
        type = Event.__check_against_keywords(type, strict=True)

        # Then the title
        if type == None:
            type = Event.__check_against_keywords(title)

        # Then the description
        if type == None:
            type = Event.__check_against_keywords(description)
 
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
        for type in Event.types:
            scores[type] = 0

        # Go through a set of the words and the keywords to see if any match
        words = [x.lower() for x in str.split()]
        for type in Event.types:
            for word in words:
                for keyword in Event.types.get(type):
                    if strict:
                        if keyword == word:
                            scores[type] = scores[type] + 1
                    else:
                        if keyword == word:
                            scores[type] = scores[type] + 10
                        elif keyword in word:
                            print(word)
                            scores[type] = scores[type] + 1
       
        # Return the type with the largest score, but only if one of them != 0
        v=list(scores.values())
        k=list(scores.keys())
        best_match = k[v.index(max(v))]
        print(scores)
        return best_match if scores[best_match] != 0 else None

title = 'Energidagen 2019'
description = '''Er du student i energi og miljø, eller nærliggende fag, og vil bli kjent med relevant fagmiljø og næringsliv? Representerer du en bedrift i energisektoren og vil komme i kontakt med studenter? Da er Energidagen årets viktigste møteplass for deg! På Energidagen møtes studenter, fagmiljø og næringsliv for å utveksle erfaring, kunnskap og inspirasjon. Bedrifter har mulighet til å profilere seg, samt delta på spennende foredrag og møte høyt motiverte og ambisiøse studenter. Energidagen arrangeres av studentene i 4. og 5. klasse på Energi og miljø-studiet i samarbeid med Energikontakten.
Program for Energidagen 2019:
10:00 – 10:00 Ballongslipp og åpning
10:00 – 16:00 Mingling på stand utover hele dagen, mulighet for speedintervju
11:00 – 12:00 Det smarte grønne skiftet og Innovative prosjekter, EL5
15:00 – 16:20 Verdiskaping i det grønne samfunnet med innlegg av våre gullsponsorer DNV GL, Statnett, GK og Siemens, EL3
Påmelding til foredragene for studenter:
Det smarte grønne skiftet og Innovative prosjekter: https://teknologiporten.no/nb/arrangement/865/
Verdiskaping i det grønne samfunnet:'''
print(Event.discern_type(None, title, description))