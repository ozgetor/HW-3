import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel(r'END507_HW3_instance.xlsx')
datas = df.to_numpy()

number_of_items = int(datas[0][1])
max_weight = int(datas[0][0])
population_limit = 20
mutation_ratio = 0.0005

current_generation = 0
score_of_generation = 0

max_number_of_generation = 1000

best_score_of_generations = np.zeros(max_number_of_generation)

item_val = datas[:,4]
item_weight = datas[:,5]

def getFitness(gene):
    sum = 0
    for i in range(len(gene)):
        sum = sum + gene[i]*item_val[i]
    
    return sum


def mutation(gene):
    for i in range(len(gene)):
        if not np.random.uniform(0,1) > mutation_ratio:
            gene[i] = np.abs(1 - gene[i])
    
    return gene


def crossover(gene1, gene2):
    gene = gene1
    for i in range(len(gene1)):
        if np.random.uniform(0,1) > 0.5:
            gene[i] = gene1[i]
        else:
            gene[i] = gene2[i]
    
    return gene
    

def canLive(gene):
    total_weight = 0
    for i in range(len(gene)):
        total_weight = total_weight + gene[i]*item_weight[i]
    if total_weight > max_weight:
        return False
    else:
        return True
    

def getParent(genes):
    total_value = 0
    parent_values = np.zeros(population_limit)
    
    for i in range(population_limit):
        total_value = total_value + getFitness(genes[i])
        parent_values[i] = total_value
        
    parent = np.random.randint(0, total_value, 1)
    
    for i in range(population_limit):
        if parent < parent_values[i]:
            return genes[i]
        
def createNewGeneration(genes):
    n = 0
    new_generation = np.zeros((population_limit, len(genes[0])))
    
    while n != population_limit:
        gene1 = getParent(genes)
        gene2 = getParent(genes)
        
        new_gene = crossover(gene1, gene2)
        new_gene = mutation(new_gene)
        
        if canLive(new_gene):
            new_generation[n] = new_gene
            n = n + 1
            
    return new_generation

def create_starting_generation():
    new_generation = np.zeros((population_limit, number_of_items))
    n = 0
    
    while n != population_limit:
        gene = np.random.randint(0,2,number_of_items)
        if canLive(gene):
            new_generation[n] = gene
            n = n+1
    
    return new_generation

def score_of_generation(genes):
    score = 0
    for i in range(population_limit):
        score = score + getFitness(genes[i])
        
    return score

def get_best_score(genes):
    score = 0
    index = 0
    for i in range(population_limit):
        if score < getFitness(genes[i]):
            score = getFitness(genes[i])
            index = i
    return score, index


best_score_of_instance = np.zeros(10)
for i in range(10):
    current_generation = np.zeros((population_limit, number_of_items))
    current_generation = create_starting_generation()
    
    
    for j in range(1, max_number_of_generation):
        current_generation = createNewGeneration(current_generation)
        best_score_of_generations[j], index = get_best_score(current_generation)
    
    best_score_of_instance[i] = np.amax(best_score_of_generations)  
    

starting_generation = create_starting_generation()
best_score_of_generations_30 = np.zeros(max_number_of_generation)
for i in range(30):
    current_generation = starting_generation
    
    for j in range(1, max_number_of_generation):
        current_generation = createNewGeneration(current_generation)
        current_best_score , index = get_best_score(current_generation)
        best_score_of_generations_30[j] = best_score_of_generations_30[j] + current_best_score
    
    best_score_of_generations_30 = best_score_of_generations_30 / 30;   
    

plt.plot(best_score_of_generations_30)
plt.ylabel('En uygun uyenin ortalama uygunlugu')
plt.show()

print(best_score_of_instance)
        