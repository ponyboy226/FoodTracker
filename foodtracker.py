import csv
import sys
import time
import os
import datetime



# Allows you to easily change the file or directory for this food journal
directory = '~/pythonCoding/'
filename = 'tracker.csv'
fullPath = directory + filename
KEY = 'GLUTENFREE,FOOD,NOTES,TIME,REACTION'

# Create the time stamp
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M')

# Set up colors for the terminal output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

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
    
    with open(fullPath, 'a') as f:
        temp = []
        w = csv.writer(f) # quoting=csv.QUOTE_ALL
        food = raw_input("Which food item would you like to add? ").capitalize()
        
        f = open(fullPath, 'r')
        
        # Get the user's input and data
        status = raw_input('Is this supposed to be Gluten Free?: ').lower()
        reaction = raw_input('Did you have a negative reaction?  Yes or No ').lower()
        notes = raw_input('Add notes here: ').capitalize()
        
        # Write the data to to separate file in CSV format 
        w.writerow([status, food, ' - ' + notes, st, reaction])

# Parse CSV file for all entries that were labeled as Not GF
def show_not_gluten():
    f = open(fullPath, 'r+')
    print 'The following entries have food containing {0}Gluten{1}:\n'.format(bcolors.WARNING, bcolors.ENDC) + '-'*30
    for row in csv.DictReader(f):
        tsn = str(row['TIME'])
        if row['GLUTENFREE'] == 'no':
            print ' >  ' + tsn + ' : {0}'.format(bcolors.WARNING) + row['FOOD'] + '{0}'.format(bcolors.ENDC) + row['NOTES'] 
    print '-'*30

# Parse CSV file for all entries that were labeled as GF
def show_yes_gluten():
    f = open(fullPath, 'r+')
    print 'The following entries have food that is {0}Gluten Free{1}:\n'.format(bcolors.OKGREEN, bcolors.ENDC) + '-'*30
    for row in csv.DictReader(f):
        tsn = str(row['TIME'])
        if row['GLUTENFREE'] == 'yes':
            print ' >  ' + tsn + ' : {0}'.format(bcolors.OKGREEN) + row['FOOD'] + '{0}'.format(bcolors.ENDC) + row['NOTES']
    print '-'*30

# Parse CSV file for all entries that were reported to have a negative side effect
def negative_reaction():
    f = open(fullPath, 'r+')
    print 'The following foods have given you a {0}negative reaction{1}:\n'.format(bcolors.FAIL, bcolors.ENDC) + '-'*30
    for row in csv.DictReader(f):
        tsn = str(row['TIME'])
        if row['REACTION'] == 'yes':
            print ' >  ' + tsn + ' : {0}'.format(bcolors.FAIL) + row['FOOD'] + '{0}'.format(bcolors.ENDC) + row['NOTES']
    print '-'*30

# Search for entries by food type.  Will output any prior reactions 
def search_for_food():
    search_word = str(raw_input('Which food entry would you like to search for? ').capitalize())
    f = open(fullPath, 'r+') 
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
                        print '{0}'.format(bcolors.OKGREEN) + search_word + '{1} are GF and you had a {0}bad reaction{1}'.format(bcolors.FAIL, bcolors.ENDC)
                    if reaction == 'no':
                        print '{0}'.format(bcolors.OKGREEN) + search_word + '{1} are GF and you were {0}fine!{1}'.format(bcolors.OKGREEN, bcolors.ENDC) 
                    break
                    
                if i == 'no':
                    if reaction == 'yes':
                        print '{0}'.format(bcolors.FAIL) + search_word + '{1} are NOT GF and you had a {0}bad reaction{1}'.format(bcolors.FAIL, bcolors.ENDC)
                    if reaction == 'no':
                        print '{0}'.format(bcolors.FAIL) + search_word + '{1} are NOT GF and you were {0}fine!{1}'.format(bcolors.OKGREEN, bcolors.ENDC) 
                    #print search_word + ' is not GF ' + reaction
                    break
        else:
            continue
    print '-'*30 + '\n' 

start()
