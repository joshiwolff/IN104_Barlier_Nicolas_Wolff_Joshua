from random import *
from math import *
import matplotlib.pyplot as plt

global rate_of_selection,rate_of_crossover,rate_of_mutation,pool,size,initial_size,eps
rate_of_selection=0.5
rate_of_crossover=0.5
rate_of_mutation=0.5
size=50000
pool=[randrange(-100, 100) for i in range(size)]

initial_size=500
eps=1/(1+(size/3)**2)



# class Individual :

    
   
    
def evaluate_fitness(Chromosome):
    x=sum([pool[i]*Chromosome[i] for i in range(size)]) 
    y=Chromosome.count(1)
    return abs(x)+1/(1+y**2)







# class Population() :

        

def select_individuals(Population):
    fitness=[evaluate_fitness(Population[i]) for i in range(len(Population))]
    selection=[]
    n=len(Population)
    while len(selection)/n<rate_of_selection:
        position=fitness.index(min(fitness))
        selection.append(Population[position])
        del Population[position]
        del fitness[position]
    return selection

def crossover_individuals(Population):
    pool_crossover=[]
    while len(pool_crossover)/len(Population)<rate_of_crossover:
        u=randint(0,len(Population)-1) 
        pool_crossover.append(Population[u])
    if len(pool_crossover)%2!=0:
        pool_crossover.pop()
    for k in range(0,len(pool_crossover)-1,2):
        i=randint(1,size-1)
        L1=pool_crossover[k]
        L2=pool_crossover[k+1]
        L1,L2=L1[:i]+L2[i:],L2[:i]+L1[i:]
        pool_crossover[k],pool_crossover[k+1]=L1,L2
    Population=Population+pool_crossover
    return Population

def mutate_individuals(Population):
    pool_mutation=[]
    while len(pool_mutation)/len(Population)<rate_of_mutation:
        u=randint(0,len(Population)-1)
        pool_mutation.append(Population[u])
    for k in range(len(pool_mutation)):
        i=randint(0,size-1)
        if pool_mutation[k][i]==1:
            pool_mutation[k][i]=0
        else:
            pool_mutation[k][i]=1
    Population=Population+pool_mutation
    return Population
    

def create_initial_population():
    
    population=[]
    for i in range (0,initial_size):
        population.append([randint(0,1) for k in range(0,size)])
    return population


def main():
    population=create_initial_population()
    inc=0
    fitness=[]
    
    while evaluate_fitness(population[0])>eps:
        
        population=select_individuals(population)
        best=evaluate_fitness(population[0])
        fitness.append(best)
        if len(population)<=1:
            return "death"
        population=mutate_individuals(population)
        population=crossover_individuals(population)
        inc+=1
        print(len(population),best)
        
    fitness.append(evaluate_fitness(population[0]))
    nb_generations=[i for i in range (0,inc+1)]
    
    print(evaluate_fitness(population[0]))
    print(sum([pool[i]*population[0][i] for i in range(size)]))
    print(population[0].count(1))

    plt.plot(nb_generations,fitness)
    plt.show()
    
    return 0
