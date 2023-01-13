from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as BS

class Exam:
    def __init__(self, type = 0):
        self.type = type

        if type == 1:
            self.soup = self.debugPage()
        else:
            self.soup = self.loadLivePage()
        
        self.questionTotal = self.getQuestionTotal()
        #Generates the Question and Answer databank
        self.dict = self.generateQuestionsAnswers()

    def loadLivePage(self):
        self.options = webdriver.ChromeOptions()
        #options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # self.driver = webdriver.Chrome(options=options)

        self.driver = webdriver.Chrome()

        # Opens the Blackboard website
        self.driver.get("https://ucmo.blackboard.com")

        # Waits for user to navigate to the correct webpage, cba to automate this atm
        self.cont = input("Once you have loaded the exam, Press [ENTER]")

        #Stores handle # of the new Test window and switches to it
        testWindow = self.driver.window_handles[1]
        self.driver.switch_to.window(testWindow)
        
        # Creates a Beautiful Soup object of the Test webpage
        return BS(self.driver.page_source, 'html.parser')
    
    def debugPage(self, source="pageSourceCH1.html"):
        return BS(open(source, encoding="utf-8"), 'html.parser')
        
    
    def getQuestionTotal(self):
        return str(self.soup).count('id="question_')
    
    def generateQuestionsAnswers(self):
        # I'm not sure if setting a limit does anything
        # Holds block of code that contains html for a question with its answers
        ansQuestion = self.soup.find_all('div', class_="field", limit=self.questionTotal)

        # No need to be fancy here, these options will always be the same
        def getTrueFalse():
            return ['True', 'False']

        # Finding the possible answers for multiple choice questions 
        def getMultChoice(block):
            #var = block.find_all('label', {"for":True})
            #for i in var:
                #list.append(i.get_text()) 
            return [x.get_text() for x in block.find_all('label', {"for":True})]
            # return [x.get_text() for x in var]

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
                self.log("Question type error on question " + count)
            count += 1
        return d
        
        # Pretty prints the dictionary
        # Adapted from sth's post on https://stackoverflow.com/questions/3229419/how-to-pretty-print-nested-dictionaries 
    def displayQuestionsAnswers(self):
        counter = 1
        for key, value in self.dict.items():
            # Prints question n
            print(str(counter) + ") " + str(key))
            # Prints answers for question n
            # chr(i + 65) is used to convert the counter to an ASCII character
            [print('\t' + chr(x + 65) + ". " + str(value[x])) for x in range(len(value))]
            counter += 1
    # logs are broken atm
    logs = ""      
    @staticmethod
    def log(cls, string):
        logs += string + "\n"

test1 = Exam()
test1.displayQuestionsAnswers()
print(test1.questionTotal)
print(Exam.questionTotal)

#note to self to fix logs, maybe define logs in the init funcition, then use self.logs?
