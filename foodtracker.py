import csv
import sys
from xml.etree.ElementTree import parse
import time
import os
import datetime



# Allows you to easily change the file or directory for this food journal
directory = '/Users/tonygardella/Desktop/pythonCoding/'
filename = 'csv.csv'
fullPath = directory + filename
KEY = 'GLUTENFREE,FOOD,NOTES,TIME,REACTION'

# Create the time stamp
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M')

# Checks to see if file exists and creates it if it doesn't
if not os.path.exists(fullPath):
    open(fullPath, 'w').close()
    
# writing the .csv header if the file doesn't already contain them
if KEY in open(fullPath).read():
    pass
else:
    with open(os.path.join(directory, filename), 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = ['GLUTENFREE', 'FOOD', 'NOTES', 'TIME', 'REACTION'], delimiter = ',')
        writer.writeheader()

# Control center of the program is here
def start():
    print' What would you like to do?\n\
    1  Add an entry\n\
    2  Show NON Gluten Free things you\'ve eaten\n\
    3  Show Gluten Free things you\'ve eaten\n\
    4  Search food entries to see if you\'ve had a reaction\n\
    5  Search your negative reactions\n\
    >  Type \'Exit\' to quit'
    choice = raw_input('Enter your selection here (1-5):  ')
    
    if choice == '1':
        add()
        start()
    if choice == '2':
        show_not_gluten()
        start()
    if choice == '3':
        show_yes_gluten()
        start()
    if choice == '4':
        search_for_food()
        start()
    if choice == '5':
        negative_reaction()
        start()
    else:
       sys.exit() 

# Function that adds new entries
def add():
    
    with open('/Users/tonygardella/Desktop/pythonCoding/gluten.csv', 'a') as f:
        temp = []
        w = csv.writer(f) # quoting=csv.QUOTE_ALL
        food = raw_input("Which food item would you like to add? ").capitalize()
        
        f = open('/Users/tonygardella/Desktop/pythonCoding/gluten.csv', 'r')
        
        # Get the user's input and data
        status = raw_input('Is this supposed to be Gluten Free?: ').lower()
        reaction = raw_input('Did you have a negative reaction?  Yes or No ').lower()
        notes = raw_input('Please add your notes here: ').capitalize()
        
        # Write the data to to separate file in CSV format 
        w.writerow([status, food, ' - ' + notes, st, reaction])

# Parse CSV file for all entries that were labeled as Not GF
def show_not_gluten():
    f = open('/Users/tonygardella/Desktop/pythonCoding/gluten.csv', 'r+')
    print 'The following foods are NOT Gluten Free:\n' + '-'*30
    for row in csv.DictReader(f):
        tsn = str(row['TIME'])
        if row['GLUTENFREE'] == 'no':
            print ' >  ' + tsn + ' : ' + row['FOOD'] + row['NOTES']
    print '-'*30

# Parse CSV file for all entries that were labeled as GF
def show_yes_gluten():
    f = open('/Users/tonygardella/Desktop/pythonCoding/gluten.csv', 'r+')
    print 'The following foods are ARE Gluten Free:\n' + '-'*30
    for row in csv.DictReader(f):
        tsn = str(row['TIME'])
        if row['GLUTENFREE'] == 'yes':
            print ' >  ' + tsn + ' : ' + row['FOOD'] + row['NOTES']
    print '-'*30

# Parse CSV file for all entries that were reported to have a negative side effect
def negative_reaction():
    f = open('/Users/tonygardella/Desktop/pythonCoding/gluten.csv', 'r+')
    print 'The following foods have given you a negative reaction:\n' + '-'*30
    for row in csv.DictReader(f):
        tsn = str(row['TIME'])
        if row['REACTION'] == 'yes':
            print ' >  ' + tsn + ' : ' + row['FOOD'] + row['NOTES']
    print '-'*30

# Search for entries by food type.  Will output any prior reactions 
def search_for_food():
    search_word = str(raw_input('Which food would you like to search for? ').capitalize())
    f = open('/Users/tonygardella/Desktop/pythonCoding/gluten.csv', 'r+') 
    searching = list(csv.DictReader(f))
    temp = []
    print '-'*30
    
    # Parsing CSV for needed data
    for i in searching:
        food = i['FOOD']
        status = i['GLUTENFREE']
        reaction = str(i['REACTION'])
        
        # Looking to see if searched word exists in CSV file
        if food == search_word:
            temp.append(status)
            for i in temp:
                
                # Determining if searched word was supposed to be GF or not
                if i == 'yes':
                    
                    # Checking if there was a negative reaction 
                    if reaction == 'yes':
                        print search_word + ' are GF and you had a bad reaction'
                    if reaction == 'no':
                        print search_word + ' are GF and you did not have a bad reaction' 
                    break
                    
                if i == 'no':
                    if reaction == 'yes':
                        print search_word + ' are NOT GF and you had a bad reaction'
                    if reaction == 'no':
                        print search_word + ' are NOT GF and you did not have a bad reaction'
                    #print search_word + ' is not GF ' + reaction
                    break
        else:
            continue
    print '-'*30 + '\n' 

start()
