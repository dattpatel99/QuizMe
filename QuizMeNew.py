import random
import datetime


# main Menu Working
def main():
    print("Welcome to QuizMe!")
    # Prints Menu Options and Instructions
    print("What would like to do? \n0) Add more questions to an old Set \n1) Create question Sets \n2) Pop Quiz mode "
          "\n3) Exam Mode \n4) Results \n5) Exit")

    # Takes integer input only and stores in variable mainOption
    mainOption = int(input())

    # Loops until a valid option not input
    while not 0 <= mainOption <= 5:
        mainOption = int(input("Enter a valid option.\n"))
    if mainOption == 0:
        file_name = str(input("Enter set name you want to append to:\n"))
        name = file_name + ".txt"
        appendQuestions(name)
    elif mainOption == 1:
        setName = str(input("What is the name for these set of questions?\n"))
        fileName = setName + ".txt"
        createSets(fileName)
    elif mainOption == 2:
        popQuiz()
    elif mainOption == 3:
        examMode()
    elif mainOption == 4:
        result()
    elif mainOption == 5:
        print("Thank You for Using QuizMe!")


'''----------------------------------------------Start of Create Sets---------------------------------------------'''

'''
This Function asks user to enter a set of questions(either Multiple choice or Single word) and answers, and a section 
name for those questions.
Then it stores them in Question File.
When finished will push user back to main menu
'''


def appendQuestions(file_name):
    # Checks for existing file and if not present gives options to user and acts accordingly
    # Test Run = Success
    status = checkFileStatus(file_name)
    if status:
        file_append = open(file_name, "a")
    else:
        while not status:
            print("No such file exists.")
            print("Would like to re-enter name or would you like  to create a new set with that name?")
            choice = int(input("Enter 1 for first option or 2 for second option:\n"))
            while 1 < choice < 2:
                choice = int(input("Please choose either 1 or 2:\n"))
            if choice == 1:
                file_name = str(input("Enter a new file name: ")) + ".txt"
                status = checkFileStatus(file_name)
            else:
                createSets(file_name)
        file_append = open(file_name, "a")

    done = False
    while not done:
        # Checks the type of question user is entering
        typeQues = str(input("Is it an MCQ question or Single word (Enter MCQ or S)?\n")).upper()
        if typeQues == "MCQ":
            # Creates MCQ question, correct answer by asking user to enter
            stringEnter = createMcq()
            file_append.write(stringEnter)
        elif typeQues == "S":
            stringEnter = createSingleQues()
            file_append.write(stringEnter)
        finished = str(input("Are you done entering new questions? (Y/N)\n")).upper()
        if finished == "Y":
            done = True
        else:
            done = False
    file_append.close()
    # Goes back to main Menu
    main()


def createSets(fileName):
    # Should open a file if it is in folder otherwise will create new one with that name
    # COULD BE CHANGED TO STORE FILE IN BETTER DIRECTORY THAT USER CHOOSES
    # CHANGE THIS TO ONLY START A NEW SET FILE

    status = checkFileStatus(fileName)
    # Checks for existing file and ensures that sure enters new set name not same one
    if not status:
        file_write = open(fileName, "w")
    else:
        status = True
        # In event of a user who is pretty dumb or unlucky
        while status:
            print("Set with that name exists.")
            print("Would you like to make a new set with different name or add questions to the set you named?")
            choice = int(input("Enter 1 for first option or 2 for second option:\n"))
            while 1 < choice < 2:
                choice = int(input("Please choose either 1 or 2:\n"))
            if choice == 1:
                fileName = str(input("Enter name of new set: ")) + ".txt"
                status = checkFileStatus(fileName)
            else:
                appendQuestions(fileName)
        file_write = open(fileName, "w")

    # Holds whether user is done entering questions or not
    done = False
    # Test Run = Success
    while not done:
        # Checks the type of question user is entering
        typeQues = str(input("Is it an MCQ question or Single word (Enter MCQ or S)?\n")).upper()
        if typeQues == "MCQ":
            # Creates MCQ question, correct answer by asking user to enter
            stringEnter = createMcq()
            file_write.write(stringEnter)
        elif typeQues == "S":
            stringEnter = createSingleQues()
            file_write.write(stringEnter)
        finished = str(input("Are you done entering new questions? (Y/N)\n")).upper()
        if finished == "Y":
            done = True
        else:
            done = False
    file_write.close()
    # Goes back to main Menu
    main()


'''----------------------------------------------End of Create Sets-------------------------------------------------'''

'''-------------------------------------------Start of Pop-Quiz Function--------------------------------------------'''
'''
    # Asks for unique quiz name
    quizName = str(input("Please enter an unique name for this quiz session.\n"))
    # MAKE UNIQUE BY ADDING DATE AND TIME
    labelQuiz = "Quiz Name: " + quizName + "\n"
'''


# Status: In Development
# Test Run: Yet to do

def popQuiz():
    setName = str(input("Enter name for set:\n")) + ".txt"
    status = checkFileStatus(setName)
    while not status:
        mainChoice = str(input("Set not found return to main menu? (Y/N)")).upper()
        if mainChoice == "Y":
            main()
        else:
            setName = str(input("Your set was not found, re-enter the set name:\n")) + ".txt"
            status = checkFileStatus(setName)
    fileRead = open(setName, "r")
    data = fileRead.readlines()
    fileRead.close()
    # Create a list of questions and answer
    quesArray = arrayCreate(data)
    tempQuesArray = arrayCreate(data)
    # In event of questions more than 10 create list of random ques
    toRemove = len(tempQuesArray) - 10
    if len(tempQuesArray) > 10:
        for i in range(0, toRemove):
            pickedQues = random.choice(tempQuesArray)
            tempQuesArray.remove(pickedQues)
    # I have no idea how this program works. BUT it works.
    # I wrote it one day and forgot my thought process on this, lol
    userAnswerDict, correctAnswerList = printQues_inputAnswers(tempQuesArray)

    # Check the answers output: result, list of wrong answer with questions
    # Param format: User answer, questions, correct answers
    result, incorrectList = checkAnswer(userAnswerDict, tempQuesArray, correctAnswerList)

    # Adds the result in file
    addResult(result, "P", setName)

    print("The questions you got incorrect, your answer and the correct answer are: \n")
    if len(incorrectList) == 0:
        print("None!!")
    else:
        for i in incorrectList:
            print("You got question:", i[0], "incorrect.")
            print("The answer you gave for this was:", i[1])
            print("The correct answer was:", i[2], "\n")
    print("Your result in this pop-quiz is....(drum-roll!!)")
    print("Result = ", result, "\n")
    print("Goodluck for the next Quiz!")
    main()


'''------------------------------------------End of Pop-Quiz Function-----------------------------------------------'''

'''-------------------------------------------------Exam Function-------------------------------------------------'''


def examMode():
    setName = str(input("Enter name for set:\n")) + ".txt"
    status = checkFileStatus(setName)
    while not status:
        mainChoice = str(input("Set not found return to main menu? (Y/N)")).upper()
        if mainChoice == "Y":
            main()
        else:
            setName = str(input("Your set was not found, re-enter the set name:\n")) + ".txt"
            status = checkFileStatus(setName)
    fileRead = open(setName, "r")
    data = fileRead.readlines()
    fileRead.close()
    # Create a list of questions and answer
    quesArray = arrayCreate(data)

    # I have no idea how this program works. BUT it works.
    # I wrote it one day and forgot my thought process on this, lol
    tempArrayOfQues = arrayCreate(data)
    userAnswerDict, correctAnswerList = printQues_inputAnswers(tempArrayOfQues)

    # Check the answers output: result, list of wrong answer with questions
    # Param format: User answer, questions, correct answers

    resultGot, incorrectList = checkAnswer(userAnswerDict, quesArray, correctAnswerList)

    # Adds the result in file
    addResult(resultGot, "E", setName)

    print("The questions you got incorrect, your answer and the correct answer are: \n")
    if len(incorrectList) == 0:
        print("None!!")
    else:
        for i in incorrectList:
            print("You got question:", i[0], "incorrect.")
            print("The answer you gave for this was:", i[1])
            print("The correct answer was:", i[2], "\n")
    print("Your result in this pop-quiz is....(drum-roll!!)")
    print("Result = ", resultGot, "\n")
    print("Goodluck for the next Quiz!")
    main()


'''----------------------------------------------Get result funciton-------------------------------------------------'''


def result():
    fileName = "result.txt"
    file_result = open(fileName, "r")
    data = file_result.readlines()
    date = str(input("Enter the date of the result in format [mm/dd/yyyy]: \n"))
    setName = str(input("Enter the set name: \n"))
    examType = input("Enter the mode of quiz you took [P for popquiz and E for exam]: \n")
    stringCheck = date + "\t" + examType + "\t" + setName
    for i in data:
        if stringCheck in i:
            found = True
            listTemp = i.split("\t")
            print("Result of that quiz is: " + listTemp[3])
            break
    if found:
        print("Quiz result not found please try again from start")
    main()


'''----------------------------------------------End result function-------------------------------------------------'''

'''------------------------------------------------Sub Functions-----------------------------------------------------'''

'''
Param: question Number
Returns: string for question and answer
'''


def createMcq():
    fullString = ""
    inputQues = str(input("Enter the MCQ question:\n"))
    question = inputQues + "\t"
    fullString += question
    inputAns = str(input("Enter the correct answer option:\n"))
    answer = inputAns + "\t"
    fullString += answer

    # Creates the incorrect options for MCQ by asking user to enter
    for i in range(1, 4):
        incorrectOpt = str(input("Enter an incorrect answer option: \n"))
        if i != 3:
            option = incorrectOpt + "\t"
        else:
            option = incorrectOpt + "\n"
        fullString += option
    return fullString


'''
Param: question Number
Returns: string for question and answer
'''


def createSingleQues():
    # Creates the single word answer questions
    # Asks for the question and answer
    fullString = ""
    inputQues = str(input("Enter the question: \n"))
    question = inputQues + "\t"
    inputAns = str(input("Enter the correct answer: \n"))
    answer = inputAns + "\n"
    fullString = fullString + question + answer
    return fullString


'''
Param: set name
Return: Boolean whether named set exists
'''


def checkFileStatus(fileName):
    try:
        file_check = open(fileName, "r")
        file_check.close()
        return True
    except FileNotFoundError:
        return False


'''
Takes in array of lines from document
Returns dictionary of data: Single 2d array of each [[question, answer], [q, a, i, i, i]] 
'''


def arrayCreate(data):
    fixedArray = []
    for i in data:
        fixedArray.append(i.split("\t"))
    # Removes new line character from the end of last option
    for i in range(0, len(fixedArray)):
        for j in range(0, len(fixedArray[i])):
            if "\n" in fixedArray[i][j]:
                fixedArray[i][j] = fixedArray[i][j].replace("\n", '')
    finalArray = fixedArray
    return finalArray


'''
Param: array of questions
Return: User answer for each question and correct answer list
'''


def printQues_inputAnswers(tempQuesArray):
    answerDict = {}
    correct_answerList = []
    for i in range(0, len(tempQuesArray)): #FIXME: IT is removing the question from question list
        print("Q" + str(i + 1) + ") " + tempQuesArray[i][0] + "\n")
        # For printing MCQ options and taking answer
        if len(tempQuesArray[i]) == 5:
            tempQuesArray[i].remove(tempQuesArray[i][0]) #Remove cause we print options using this
            answerList = tempQuesArray[i]
            # Fixed way to set correct option so we can check later
            correctOpt = answerList[0]
            # prints the choices randomly
            for j in range(0, 4):
                option = random.choice(answerList)
                # Checks if the option value is correct if it is then we store the option
                if option == correctOpt:
                    correct_answerList.append(str(j + 1))
                print(str(j + 1) + ") " + str(option))
                answerList.remove(option)
            answerUser = str(input("Enter your answer option(between 1-4):\n"))
            answerDict[str(i)] = answerUser
        # For taking single work answers
        elif len(tempQuesArray[i]) == 2:
            correct_answerList.append(tempQuesArray[i][1])
            answerUser = str(input("Enter your answer:\n"))
            answerDict[str(i)] = answerUser
    return answerDict, correct_answerList


'''
Param: user answers dict, question list, correct answer list
Return: the result, list of wrong answer and their questions 
'''


def checkAnswer(userAns, quesList, correctAns):
    wrongAnswerList = []
    tempQuesArray = quesList
    # Total questions = len(quesList)
    right_counter = 0
    for i in range(0, len(tempQuesArray)):
        if userAns[str(i)] == correctAns[i]:
            right_counter += 1
        else:
            tempArray = [tempQuesArray[i][0], userAns[str(i)], correctAns[i]]
            wrongAnswerList.append(tempArray)
    resultCalculated = float(right_counter / len(tempQuesArray)) * 100.0
    return resultCalculated, wrongAnswerList


def addResult(resultValue, examType, setName):
    fileName = "result.txt"
    if checkFileStatus(fileName):
        file_result = open(fileName, "a")
    else:
        file_result = open(fileName, "w")
    resultDate = currentDate()
    finalString = resultDate + "\t" + examType + "\t" + setName + "\t" + str(resultValue) + "\n"
    file_result.write(finalString)
    file_result.close()


def currentDate():
    x = datetime.datetime.now()
    monthDate = x.strftime("%m")
    dayDate = x.strftime("%d")
    yearDate = x.strftime("%Y")
    resultDate = monthDate + "/" + dayDate + "/" + yearDate
    return resultDate


'''--------------------------------------------------Sub Functions end-----------------------------------------------'''

'''----------------------------------------------------GUI Program---------------------------------------------------'''

main()
