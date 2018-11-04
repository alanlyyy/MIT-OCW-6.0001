# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name: Alan Ly
# Collaborators: Analyzed code from Thang Tran 6.0001 github
# Time: unknown

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory(object):
    
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
    
    def get_guid(self):
        return self.guid
    
    def get_title(self):
        return self.title
    
    def get_description(self):
        return self.description
    
    def get_link(self):
        return self.link
    
    def get_pubdate(self):
        return self.pubdate
        
    

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    
    
    def __init__(self,phrase):
        
        #convert all characters to lower case
        self.phrase = phrase.lower()
    

    def is_phrase_in(self, text):

            text = text.lower()
            
            #replace all punctuations with white space
            for char in string.punctuation:
                text = text.replace(char, ' ')
            
            #split the text without punctuation by white space
            word_list = text.split(' ')
            
            #while there is white space in the list remove the elements 
            #from the list
            while '' in word_list:
                word_list.remove('')
            
            #split the phrase into a list
            phrase_split = self.phrase.split()
            
            #store the indexes of the matching words of the phrase
            test = []
            
            #for the number of words in phrase
            for ph in phrase_split:
                
                #check if the word is equal to the word in phrase
                for i, word in enumerate(word_list):
                    
                    #if word is equal to phrase add the index to the list
                    if ph == word:
                        test.append(i)
                        
            found = True
            
            #if the length of the temporary list is less than length of phrase
            #split phrase is not in the text message
            if len(test) < len(phrase_split):
                return False
            
            #loop through the index array of matched words
            for i in range(len(test) - 1):
                
                #if the index of one word - the index of another word
                #is not equal to 1 then phrase is not in text message
                
                if test[i + 1] - test[i] != 1:
                    found = False
                    
            return found

# Problem 3
# TODO: TitleTrigger
class TitleTrigger(PhraseTrigger):
        
    def evaluate(self,story):
        return self.is_phrase_in(story.get_title())


# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):
    
    def evaluate(self,story):
        return self.is_phrase_in(story.get_description())
        
    
# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):
    
    def __init__(self, time_string):
        #convert string into datetime object
        time_string = datetime.strptime(time_string, "%d %b %Y %H:%M:%S")
        
        #set the timezone of the datetime object
        time_string = time_string.replace(tzinfo=pytz.timezone("EST"))
        self.pubtime = time_string
        
# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    
    def evaluate(self,story):
        #if the trigger time is greater than the story time
        return self.pubtime > story.get_pubdate().replace(tzinfo=pytz.timezone("EST"))
    
class AfterTrigger(TimeTrigger):
    
    def evaluate(self,story):
        #if trigger time is less than story time
        return self.pubtime < story.get_pubdate().replace(tzinfo=pytz.timezone("EST"))
    
# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):
    
    def __init__(self,trigger):
        #trigger is an object of type trigger with a parameter phrase passed in
        self.trigger = trigger
        
    def evaluate(self,news_item):
        #return the inverted output of the trigger 
        #evaluated with the specified news item
        return not self.trigger.evaluate(news_item)
        

# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):
    
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    
    def evaluate(self,news_item):
        #checks to see if trigger1 and trigger2 both fire on a specific news
        #story, and returns both evaluated triggers as a tuple
        if self.trigger1.evaluate(news_item) \
                                        and self.trigger2.evaluate(news_item):
            return self.trigger1.evaluate(news_item) ,self.trigger2.evaluate(news_item)
                        
# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):
    
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    
    def evaluate(self,news_item):
        #checks to see if trigger1 and trigger2 both fire on a specific news
        #story, and returns both evaluated triggers as a tuple
        if self.trigger1.evaluate(news_item) \
                                        or self.trigger2.evaluate(news_item):
            return self.trigger1.evaluate(news_item) ,self.trigger2.evaluate(news_item)

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10

    #stores the fired stories
    triggered_stories = []
    
    for story in stories:
        for trigger in triggerlist:
            
            #if a trigger is fired for the story, append the story to a list
            #triggered stories
            if trigger.evaluate(story):
                
                #if story is not already stored in the list add to the list
                if story not in triggered_stories:
                    triggered_stories.append(story)
                    
    return triggered_stories



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # lines is the list of lines that you need to parse and for which you need
    # to build triggers
    trig_dict = {}
    trig_list = []
    
    for line in range(len(lines)):
        #split the line by commas into a list
        line_split = line.split(' , ')
        
        #if the first element is add
        if line_split[0] == 'ADD':
            
            #append all elements into a list and add the list to the dictionary
            for line in range(1,len(line_split)):
                trig_list.append(line)
            
            trig_dict[line_split[0]] = trig_list
            
            #otherwise add the trigger calls into the dictionary
        else:
            if line_split[1] == 'DESCRIPTION':
                trig_dict[line_split[0]] = DescriptionTrigger(line_split[2])
            elif line_split[1] == 'TITLE':
                trig_dict[line_split[0]] = TitleTrigger(line_split[2])
            elif line_split[1] == 'AND':
                trig_dict[line_split[0]] = AndTrigger(line_split[3],line_split[4])
            elif line_split[1] == 'OR':
                trig_dict[line_split[0]] = OrTrigger(line_split[3],line_split[4])
            elif line_split[1] == 'NOT':
                trig_dict[line_split[0]] = NotTrigger(line_split[1])
            elif line_split[1] == 'BEFORE':
                trig_dict[line_split[0]] = BeforeTrigger(' '.join(line_split[1:]))
            elif line_split[1] == 'AFTER':
                trig_dict[line_split[0]] = AfterTrigger(' '.join(line_split[1:]))
                
    
    return trig_dict



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
# =============================================================================
#         t1 = TitleTrigger("election")
#         t2 = DescriptionTrigger("Trump")
#         t3 = DescriptionTrigger("Clinton")
#         t4 = AndTrigger(t2, t3)
#         triggerlist = [t1, t4]
# =============================================================================

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = list(read_trigger_config('triggers.txt').values())
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


# =============================================================================
if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()
#     
# =============================================================================
    #Test Cases: Phrase Trigger
# =============================================================================
#     phrase_trig = PhraseTrigger("apple sauce")
#     print(phrase_trig.is_phrase_in("I like !! apple ?!@%&*sauce."))
#     
#     phrase_trig = PhraseTrigger("apple sauce")
#     print(phrase_trig.is_phrase_in("I apple log !! apple ?? sauce."))
#     
#     phrase_trig = PhraseTrigger("apple sauce")
#     print(phrase_trig.is_phrase_in("sauce log !! apple log."))
# =============================================================================
# =============================================================================
#     
#     phrase_trig = PhraseTrigger("winning is everything")
#     print(phrase_trig.is_phrase_in("I think winning is everything!"))
#    
#     
#     phrase_trig = PhraseTrigger("winning is everything")
#     print(phrase_trig.is_phrase_in("I think !! winning is not everything!"))
#         
#     phrase_trig = PhraseTrigger("winning is everything")
#     print(phrase_trig.is_phrase_in("I think !!  everything is winning!"))
#  
# 
# =============================================================================
