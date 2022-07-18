import random
import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np
import random

data = pd.read_csv("selected_food.csv")

def getReward(previousState, action):
    
    c_food = data[data['Label']==action]
    
    if len(previousState) == 0:
        return int(c_food['Utility'])
    
    p_food = data[data['Label']==previousState]
    
    p_cabohydrate = float(p_food['Carbohydrate'])
    p_fat = float(p_food['Fat'])
    p_protein = float(p_food['Protein'])
    
    c_cabohydrate = float(c_food['Carbohydrate'])
    c_fat = float(c_food['Fat'])
    c_protein = float(c_food['Protein'])
    utility = int(c_food['Utility'])
    
    #Use Euclidean distance to estimate similarity between food
    dst = math.sqrt((p_cabohydrate-c_cabohydrate)**2+(p_fat-c_fat)**2+(p_protein-c_protein)**2)
    
    if dst > 0.6:
        reward = utility
    elif dst > 0.4:
        reward = utility *0.8
    elif dst > 0.2:
        reward = utility *0.6
    else:
        reward = utility*0.4
    return reward
    

initial_lr = 1.0 
min_lr = 0.003
eps = 0.05
gamma = 0.95
# iter_max = 250000
iter_max = 100000
t_max = 21
qtable = {}
total_reward_list = []

for i in range(iter_max):

    uneaten = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U']


    state = ""
    next_state = ""
    next2_best_state = ""
    total_reward = 0
    
    ## eta: learning rate is decreased at each step
    eta = max(min_lr, initial_lr * (0.85 ** (i//2000)))
    for j in range(t_max):
        
        if np.random.uniform(0, 1) < eps:
            action = uneaten[random.randint(0, len(uneaten)-1)]
        else:
            index = 0
            highestValue = 0
            for k in range(len(uneaten)):
                temp_state = state
                temp_state += uneaten[k]
                if temp_state in qtable.keys():
                    if qtable[temp_state] > highestValue:
                        index = k
                        highestValue = qtable[temp_state]      
            action = uneaten[index]
              
        uneaten.remove(action)
        next_state += action 

        reward = getReward(state[len(state)-1:], next_state[len(next_state)-1:])
        total_reward += (gamma ** j) * reward
        
        #Find next best state
        
        next2_best_state = next_state
        index = 0
        highestValue = 0
        for k in range(len(uneaten)):
            temp_state = state
            temp_state += uneaten[k]
            if temp_state in qtable.keys():
                if qtable[temp_state] > highestValue:
                    index = k
                    highestValue = qtable[temp_state]
        
        if len(uneaten) > 0:
            next2_best_state += uneaten[index]
        
        
        # update q table
        if next_state not in qtable.keys():
            qtable[next_state] = 0
        if next2_best_state not in qtable.keys():
            qtable[next2_best_state] = 0
        
        if len(uneaten) > 0:
            qtable[next_state] = qtable[next_state] + eta * (reward + gamma *  qtable[next2_best_state] - qtable[next_state])
        
        state = next_state
        
    
    total_reward_list
    
    if i % 1000 == 0:
        total_reward_list.append(total_reward)
        print('Iteration #%d -- Total reward = %d.' %(i+1, total_reward))


uneaten = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U']
action = uneaten[random.randint(0, len(uneaten)-1)]
uneaten.remove(action)
state = action

print("Day 1 Eating Plan")
print("")

c_food = data[data['Label']==action]
print(c_food.tail(1)['Food'].values[0])

count = 2

for i in range (20):
    index = 0
    highestValue = 0
    for j in range (len(uneaten)):
        temp_state = state
        temp_state += uneaten[j]
        if temp_state in qtable.keys():
            if qtable[temp_state] > highestValue:
                index = j
                highestValue = qtable[temp_state]      
                
    if (i+1) % 3 == 0:
        print("")
        print("Day", count, "Eating Plan")
        print("")
        count += 1
    action = uneaten[index]
    c_food = data[data['Label']==action]
    print(c_food.tail(1)['Food'].values[0])
    state += action
    uneaten.remove(action)

    