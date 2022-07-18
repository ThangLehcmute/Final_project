import random
import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame

data = pd.read_excel("food.xlsx")
print(data['Food'])
weeklyCalories = 1832 * 7

food = data['Food']
calories = data['Calories']
utility = data['Utility']
carbo = data['Carbohydrate']
fat = data['Fat']
protein = data['Protein']


populationSize = 50
numberOfGenerations = 100
rateOfMutation = 0.1
tournamentSize = 10

currentGen = []
currentBestSolution = []
highestScoreList = []
averageScoreList = []

#Initialise a Population
listofones = [1]*21
listofzeros = [0]*(len(food)-21)

for i in range (populationSize):
    currentGen. append(listofones + listofzeros)
    random.shuffle(currentGen[i])


for g in range (numberOfGenerations):
    
    fitnessScore = [0]*populationSize
    normalisedFitnessScore = [0]*populationSize
    totalPolulationFitnessScore = 0
    highestScore = 0
    nextGen = []
    newGen = []

    # Perform Evaluation of Fitness Score
    for i in range (populationSize):
        totalCalories = 0
        for j in range (len(food)):
            fitnessScore[i] += currentGen[i][j] * utility[j]
            totalCalories += currentGen[i][j] * calories[j]
        if totalCalories > weeklyCalories:
            fitnessScore[i] += weeklyCalories - totalCalories
        if fitnessScore[i] > highestScore:
            currentBestSolutionIndex = i
            highestScore = fitnessScore[i]

        totalPolulationFitnessScore += fitnessScore[i]
        
    highestScoreList.append(highestScore)
    averageScoreList.append(totalPolulationFitnessScore/populationSize)    
    currentBestSolution = currentGen[currentBestSolutionIndex].copy()

    for i in range (populationSize):
        normalisedFitnessScore[i] = fitnessScore[i]/totalPolulationFitnessScore

    #Perform Selection
    for i in range (populationSize):
        cumulativeNormalisedFitnessScore = 0
        rwScore = random.uniform(0, 1)
        for j in range (populationSize):
            cumulativeNormalisedFitnessScore += normalisedFitnessScore[j]
            if cumulativeNormalisedFitnessScore >= rwScore:
                nextGen.append(currentGen[j].copy())
                break    

    #Perform Mutation
    for i in range (populationSize):
        for j in range (len(food)):
            if rateOfMutation > random.uniform(0, 1):
                nextGen[i][j] = abs(nextGen[i][j] - 1)

    #Adjust bits back to zero
    for i in range (populationSize):
        bitsToAdjust = sum(nextGen[i]) - 21

        if bitsToAdjust > 0:
            for j in range (bitsToAdjust):
                index = random.randint(0, len(food)-1)
                notFound = True
                while notFound:
                    if nextGen[i][index] == 1:
                        nextGen[i][index] = 0
                        notFound = False
                    else:
                        index += 1
                        index  = index%len(food)
        elif bitsToAdjust < 0:
            for j in range (abs(bitsToAdjust)):
                index = random.randint(0, len(food)-1)
                notFound = True
                while notFound:
                    if nextGen[i][index] == 0:
                        nextGen[i][index] = 1
                        notFound = False
                    else:
                        index += 1
                        index  = index%len(food) 
    
    #Form a new Generation by using N-tournament. Randomly draw N parents and N offspring and select the best for new generation
    
    #Compute fitness score for offspring
    fitnessScore2 = [0]*populationSize 
    for i in range (populationSize):
        totalCalories = 0
        for j in range (len(food)):
            fitnessScore2[i] += nextGen[i][j] * utility[j]
            totalCalories += nextGen[i][j] * calories[j]
        if totalCalories > weeklyCalories:
            fitnessScore2[i] += weeklyCalories - totalCalories
            
    for i in range (populationSize):
        
        highest_fitness_score = 0
        index = 0
        parent_selected = True
        
        for j in range (tournamentSize):
            index_p = int(random.uniform(0, populationSize-1))
            index_o = int(random.uniform(0, populationSize-1))
            
            if highest_fitness_score < fitnessScore[index_p]:
                parent_selected = True
                index = index_p
                highest_fitness_score = fitnessScore[index_p]
                
            if highest_fitness_score < fitnessScore2[index_o]:
                parent_selected = False
                index = index_o
                highest_fitness_score = fitnessScore[index_o]
            
        if parent_selected:
            newGen.append(currentGen[index].copy())
        else:
            newGen.append(nextGen[index].copy())
              
    currentGen = newGen.copy()
    
    #Reduce rate of Mutation as search progresses
    if (g+1)%(numberOfGenerations/10) == 0:
        rateOfMutation *= 0.9
        

label = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U']
s_food = []
s_utility = []
s_carbo = []
s_fat = []
s_protein = []
s_calories = []
for i in range (len(food)):
    if currentBestSolution[i] == 1:
        s_food.append(food[i])
        s_utility.append(utility[i])
        s_carbo.append(carbo[i])
        s_fat.append(fat[i])
        s_protein.append(protein[i])
        s_calories.append(calories[i])
        
Selected_Food = {'Label':label, 'Food':s_food, 'Calories':s_calories,'Utility': s_utility, 'Carbohydrate': s_carbo,'Fat': s_fat, 'Protein': s_protein}
df = DataFrame(Selected_Food, columns=['Label','Calories','Food','Utility','Carbohydrate','Fat','Protein'])
export_csv = df.to_csv('selected_food.csv', index = None)
        