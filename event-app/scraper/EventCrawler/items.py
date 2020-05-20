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

    hosts = {
        'Abakus': ['abakus', 'linjeforeningen abakus', 'datateknologi og kommunikasjonsteknologi'],
        'Samfundet': ['studentersamfundet', 'samfundet'],
        'EMIL': ['energi og miljø', 'emil'],
        'Omega': ['omega'],
        'NTNU': ['ntnu', 'norges teknisk-naturvitenskapelige universitet']
    }

    study_programs = {
        'Datateknologi': ['data', 'datateknologi', 'mtdt', 'abakus'],
        'Kommunikasjonsteknologi': ['komtek', 'kommunikasjonsteknologi', 'mtkom', 'abakus'],
        'EMIL': ['energi og miljø', 'emil', 'mtenerg'],
    }

    @staticmethod
    def discern_host(host):
        return EventItem.__check_against_keywords(EventItem.hosts, host, strict=True, allow_many=True)

    @staticmethod
    def discern_study_program(study_program, host, description):
        """
        Returns the study program induced from the study program, host and description
        """

        # First, check the study program itself
        study_program = EventItem.__check_against_keywords(EventItem.study_programs, study_program, strict=True, allow_many=True)

        # Then the host
        if study_program == None:
            study_program = EventItem.__check_against_keywords(EventItem.study_programs, host, strict=True, allow_many=True)

        # Then the description
        if study_program == None:
            study_program = EventItem.__check_against_keywords(EventItem.study_programs, description, allow_many=True)
 
        return study_program if study_program != None else "Ukjent" 



    @staticmethod
    def discern_type(type, title, description):
        """
        Returns the type induced from the type, title and description
        """
        # First, check the type itself
        type = EventItem.__check_against_keywords(EventItem.types, type, strict=True)

        # Then the title
        if type == None:
            type = EventItem.__check_against_keywords(EventItem.types, title, strict=True)

        # Then the description
        if type == None:
            type = EventItem.__check_against_keywords(EventItem.types, description)
 
        return type if type != None else "Ukjent" 
    
    @staticmethod
    def __check_against_keywords(keywords, str, strict=False, allow_many=False):
        """
        Takes a list of words and returns the type with a matching keyword. 
        If the boolean strict is true, the search will require an excact match. If allow_many is true, then a comma seperated string of all matches is returend
        """

        # If nothing is passed, theres no need to do anything
        if str == None:
            return None
        
        # Need to track how well it matches any given type
        scores = {}
        for type in keywords:
            scores[type] = 0

        # Go through a set of the words and the keywords to see if any match
        words = [x.lower() for x in str.split()]
        for type in keywords:
            for word in words:
                for keyword in keywords.get(type):
                    word = word.replace(',', '')
                    if strict:
                        if keyword == word:
                            scores[type] = scores[type] + 1
                    else:
                        if keyword == word:
                            scores[type] = scores[type] + 10
                        elif keyword in word:
                            scores[type] = scores[type] + 1
       

        if allow_many:
            # Return all keys that had some sort of match
            hosts = ''
            for item in scores.items():
                if item[1] > 0:
                    hosts += item[0] + ','
            return hosts[:-1] # Take away last comma

        else:
            # Return the type with the largest score, but only if one of them != 0
            v=list(scores.values())
            k=list(scores.keys())
            best_match = k[v.index(max(v))]
            return best_match if scores[best_match] != 0 else None