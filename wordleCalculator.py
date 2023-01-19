import csv
import time

# returns the result of a guess answer pair
def wordleResult(guess, answer):
    result = [0,0,0,0,0]
    i = 0
    str = {}
    for letter in guess:
        # case for green letter
        if letter == answer[i]:
            result[i] = 2
        # case for yellow or grey letter
        else:
            str[answer[i]] = str.get(answer[i], 0) + 1
        i += 1
    i = 0
    for letter in guess:
        if result[i] !=2:
            # loop through again and look at non greens
            if str.get(letter, 0) > 0:
                # if the letter is not green and is in the answer subtract from our dictionary of the non green letters
                result[i] = 1
                str[letter] = str[letter] - 1

        i += 1
    return result

# returns true if an answer is possible given a guess and result
def isPossibleAnswer(answer, guess, result):
    return wordleResult(guess, answer) == result

# returns all possible answers
def getPossibleAnswers(answerList, guess, result):
    possible = []
    for answer in answerList:
        if isPossibleAnswer(answer, guess, result):
            possible += [answer]
    return possible

# scores all answers
def scoreAnswers(validGuess, validAnswer):
    guessNumbers = []
    i = 0
    ret = []
    # for every guess assume every answer and see how many answers it would eliminate
    # sum total eliminated answers for score
    for guess in validGuess:
        guessNumbers += [0]
        for answer in validAnswer:
            result = wordleResult(guess, answer)
            for ans in validAnswer:
                if not isPossibleAnswer(ans, guess, result):
                    guessNumbers[i] += 1
        ret += [(guess[0][0] + guess[1][0] + guess[2][0] + guess[3][0] + guess[4][0], guessNumbers[i])]
        i += 1
    return ret

# scores all answers and saves to a csv to determine best starting word
def scoreAnswersAndSave():
    inFile = open('newScored.csv', 'r')
    scored = inFile.read().split('\n')
    scored.pop()
    inFile.close()
    guessNumbers = []
    i = 0
    for s in scored:
        scored[i] = s.split(',')[0]
        guessNumbers += [int(s.split(',')[1])]
        i+=1
    outFile = open('newScored.csv', 'a', newline='')
    outCSV = csv.writer(outFile)
    best = validGuess[0]
    max = 0
    i = 0
    for guess in validGuess:
        guessNumbers += [0]
        if guess in scored:
            if guessNumbers[i] > max:
                max = guessNumbers[i]
                best = guess
                print('MAX:', guess, max)
            i += 1
            continue
        for answer in validAnswer:
            result = wordleResult(guess, answer)
            for ans in validAnswer:
                if not isPossibleAnswer(ans, guess, result):
                    guessNumbers[i] += 1
        outCSV.writerow([guess[0][0] + guess[1][0] + guess[2][0] + guess[3][0] + guess[4][0], guessNumbers[i]])
        if guessNumbers[i] > max:
            max = guessNumbers[i]
            best = guess
            print('MAX:', guess, max)
        i += 1
    outFile.close()

# ranks all scores and returns the best guess
def rankScores(scoredWords):
    scoresDict = {}
    scoresList = []
    for row in scoredWords:
        currScore = float(row[1])
        while currScore in scoresList:
            currScore += 1/len(scoresList)
        scoresList += [currScore]
        scoresDict[currScore] = row[0]
    score = max(scoresList)
    return scoresDict[score]

# eliminates guesses that are deemed bad due to letter frequency
def widdle(validAnswers, validGuesses, results):
    letterFreq = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0,
               'm': 0, 'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0,
               'x': 0, 'y': 0, 'z': 0}
    for answer in validAnswers:
        for letter in answer:
            letterFreq[letter] += 1
    grey = []
    for entry in results:
        word = entry[0]
        result = entry[1]
        i = 0
        str = ''
        for number in result:
            if number == 0 and word[i] not in str:
                grey += word[i]
            else:
                str = str + word[i]
            i+=1
    i=0
    for letter, val in letterFreq.items():
        if val == 0:
            grey += [letter]
        i+=1
    ret = []
    while(len(grey) > 18):
        grey.remove(grey[len(grey)-1])
    for word in validGuesses:
        bool = True
        for letter in grey:
            if letter in word:
                bool = False
                break
        if bool:
            ret += [word]

    return ret

# eliminates more strictly based on letter frequency in remaining answers
def widdleMore(validAnswers, validGuesses):
    letterFreq = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0,
                  'm': 0, 'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0,
                  'x': 0, 'y': 0, 'z': 0}
    for answer in validAnswers:
        for letter in answer:
            letterFreq[letter] += 1
    least = 13000
    worst = ''
    for letter, val in letterFreq.items():
        if val < least and val != 0:
            least = val
            worst = letter
    ret = []
    for word in validGuesses:
        if worst not in word:
            ret += [word]
    used = [worst]
    while len(ret) > 700:
        least = 13000
        nworst = ''
        for letter, val in letterFreq.items():
            if val < least and val != 0 and letter not in used:
                least = val
                nworst = letter
        ret2 = []
        for word in ret:
            if nworst not in word:
                ret2 += [word]
        used += [nworst]
        if len(ret2) == 0:
            return ret
        ret = ret2
    return ret

def runCalc(validAnswers, validGuesses, secretAnswer):
    guess = 'roate'
    results = []
    ret = 0
    while True:
        ret += 1
        print("Guess:", guess)
        result = wordleResult(guess,secretAnswer)
        results += [(guess, result)]
        if result == [2, 2, 2, 2, 2]:
            break

        validAnswers = getPossibleAnswers(validAnswers, guess, result)
        print("Number of possible Answers:", len(validAnswers))
        if ret == 1 and len(validAnswers) > 10:
            line = firstResult[result[4] + result[3] * 3 + result[2] * 9 + result[1] * 27 + result[0] * 81]
            guess = line[-5:]
            continue

        optimalGuesses = validGuesses
        # optimalGuesses = widdle(validAnswers, validGuesses, results)
        # if len(optimalGuesses) > 700:
            # optimalGuesses = widdleMore(validAnswers, validGuesses)

        if (len(validAnswers) > 3):
            scoredAnswers = scoreAnswers(optimalGuesses, validAnswers)
            bestScore = rankScores(scoredAnswers)
        else:
            scoredAnswers = scoreAnswers(validAnswers, validAnswers)
            bestScore = rankScores(scoredAnswers)
        guess = bestScore
    print()
    return ret

def runCalcFromInput(validAnswers, validGuesses):
    guess = 'roate'
    results = []
    ret = 0
    while True:
        ret += 1
        print("Guess:", guess)
        result = []
        while(len(result) != 5):
            result = input("Enter Result: ").split(" ")
            if result == 'STOP':
                return
            try:
                for i in range(5):
                    result[i] = int(result[i])
            except:
                result = []
                print("Invalid!")
                continue
        results += [(guess, result)]
        if result == [2,2,2,2,2]:
            break



        validAnswers = getPossibleAnswers(validAnswers, guess, result)
        print("Number of possible Answers:",len(validAnswers))
        if ret == 1:
            line = firstResult[result[4] + result[3] * 3+ result[2] * 9 + result[1] * 27 + result[0] * 81]
            guess = line[-5:]
            continue

        optimalGuesses = validGuesses
        if len(validAnswers) > 9:
             optimalGuesses = widdle(validAnswers, validGuesses, results)
             if len(optimalGuesses) > 700:
                 optimalGuesses = widdleMore(validAnswers, validGuesses)

        if (len(validAnswers) > 3):
            scoredAnswers = scoreAnswers(optimalGuesses, validAnswers)
            bestScore = rankScores(scoredAnswers)
        else:
            scoredAnswers = scoreAnswers(validAnswers, validAnswers)
            bestScore = rankScores(scoredAnswers)
        guess = bestScore
    print()
    return ret

def writeBeginning(guess, validAnswers, validGuesses):

    for i in range(0, 3*3*3*3*3):
        beginningFile = open('beginning_' + guess + '.txt', 'a')
        results = []
        result = [0,0,0,0,0]

        # write code to increment through all possible results
        temp = i
        result[4] = temp % 3
        temp = temp // 3
        result[3] = temp % 3
        temp = temp // 3
        result[2] = temp % 3
        temp = temp // 3
        result[1] = temp % 3
        temp = temp // 3
        result[0] = temp % 3

        results += [(guess, result)]

        validAnswersTemp = []
        for a in validAnswers:
            validAnswersTemp += [a]
        validGuessesTemp = []
        for g in validGuesses:
            validGuessesTemp += [g]
        validAnswersTemp = getPossibleAnswers(validAnswersTemp, guess, result)
        if len(validAnswersTemp) == 0:
            beginningFile.write(
                str(result[0]) + ' ' + str(result[1]) + ' ' + str(result[2]) + ' ' + str(result[3]) + ' ' + str(
                    result[4]) + ' ' + "NOT_POSSIBLE" + '\n')
            continue
        print("Number of possible Answers:", len(validAnswersTemp))
        optimalGuesses = validGuessesTemp
        if len(validAnswers) > 80:
            optimalGuesses = widdle(validAnswersTemp, validGuessesTemp, results)
            if len(optimalGuesses) > 700:
                optimalGuesses = widdleMore(validAnswersTemp, validGuessesTemp)


        if (len(validAnswersTemp) > 3):
            scoredAnswers = scoreAnswers(optimalGuesses, validAnswersTemp)
            bestScore = rankScores(scoredAnswers)
        else:
            scoredAnswers = scoreAnswers(validAnswersTemp, validAnswersTemp)
            bestScore = rankScores(scoredAnswers)
        beginningFile.write(str(result[0]) + ' ' + str(result[1]) + ' ' + str(result[2]) + ' ' + str(result[3]) + ' ' + str(result[4]) + ' ' + bestScore + '\n')
        print('Wrote!')
        print(str(result[0]) + ' ' + str(result[1]) + ' ' + str(result[2]) + ' ' + str(result[3]) + ' ' + str(result[4]) + ' ' + bestScore)
        beginningFile.close()


# get list of words and format them
# get starting outcomes for roate
validGuessFile = open('validGuess.txt', 'r')
validAnswerFile = open('validAnswer2.txt', 'r')
firstResultFile = open('beginning_roate.txt', 'r')
firstResult = firstResultFile.read().split('\n')
validGuess = validGuessFile.read().split('\n')
validAnswer = validAnswerFile.read().split('\n')
firstResultFile.close()
validAnswerFile.close()
validGuessFile.close()

average = 0
i = 0
stri = 'y'

while stri != 'n':
    validAnswersTemp = []
    for a in validAnswer:
        validAnswersTemp += [a]
    validGuessesTemp = []
    for g in validGuess:
        validGuessesTemp += [g]
    runCalcFromInput(validAnswersTemp, validGuessesTemp)
    stri = input('Would you like to continue (y / n): ')

# validAnswerNew = []
# for a in validAnswer:
#     validAnswerNew += [a]
# for answer in validAnswer:
#     i += 1
#     average += runCalc(validAnswerNew, validGuess, answer)
#     validAnswerNew.remove(validAnswerNew[0])
# print(validAnswerNew)
# average = average / (i * 1.0)
# print(average)

# scoreAnswersAndSave()

# 2.889941453933716