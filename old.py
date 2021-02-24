from selenium import webdriver
#from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup as BS

logs = " "
def log(string):
    logs += string + "\n"

def openTest():
    # Create the selenium webdriver that doesn't output errors to the console
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)

    # Opens the Blackboard website
    driver.get("https://ucmo.blackboard.com")

    # Waits for user to navigate to the correct webpage, cba to automate this atm
    cont = input("Once you have loaded the exam, Press [ENTER]")

    #Stores handle # of the new Test window and switches to it
    testWindow = driver.window_handles[1]
    driver.switch_to.window(testWindow)
    

    # Creates a Beautiful Soup object of the Test webpage
    return BS(driver.page_source, 'html.parser')

# Asks user if they want to use a live webpage or load a sample
choice = int(input("Load webpage(1) or use premade page(2)? "))
if choice == 1:
    soupy = openTest()
elif choice == 2:
    soupy = BS(open("pageSourceCH1.html", encoding="utf-8"), 'html.parser')

# Stores the total amount of questions on the test
questionTotal = str(soupy).count('id="question_')

# Generates a dictionary that contains questions and their answer options
def generateQuestionsAnswers(soup):
    # I'm not sure if setting a limit does anything
    ansQuestion = soup.find_all('div', class_="field", limit=questionTotal)

    # No need to be fancy here, these options will always be the same
    def getTrueFalse():
        return ['True', 'False']

    # Finding the possible answers for multiple choice questions 
    def getMultChoice(block):
        var = block.find_all('label', {"for":True})
        #for i in var:
            #list.append(i.get_text()) 
        return [x.get_text() for x in var]

    d = {}
    count = 0
    for block in ansQuestion:
        # Stores question #n, later to be added to the dictionary
        question = block.find("div", class_="vtbegenerated inlineVtbegenerated").get_text().strip()
        # Adds True/False question and answer to the dictionary
        if "tf" in block.label['for']:
            d[question] = getTrueFalse()
        # Adds multiple choice question and answer to the dictionary
        elif "mc" in block.label['for']:
            d[question] = getMultChoice(block)
        # My hope is that this acts as a catch all for questions that can't be answered with this program (i.e short answer)
        else:
            log("Question type error on question " + count)
        count += 1
    return d

finalDict = generateQuestionsAnswers(soupy)

# Fancy prints the dictionary
# Adapted from sth's post on https://stackoverflow.com/questions/3229419/how-to-pretty-print-nested-dictionaries 
def displayQuestionsAnswers(d):
   counter = 1
   for key, value in d.items():
        # Prints question n
        print(str(counter) + ") " + str(key))
        # Prints answers for question n
        # chr(i + 65) is used to convert the counter to an ASCII character
        [print('\t' + chr(x + 65) + ". " + str(value[x])) for x in range(len(value))]
        counter += 1

displayQuestionsAnswers(finalDict)
