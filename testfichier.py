from random import *
from math import *
import matplotlib.pyplot as plt


global rate_of_selection,rate_of_crossover,rate_of_mutation,pool,size,initial_size

pool=[]
fichier=open("extralarge.txt","r")
fichier.readline()
contenu=fichier.read()
contenu.replace(" ","")

num=""
for i in range(len(contenu)):
    if contenu[i]!=",":
        num+=contenu[i]
    if contenu[i]==",":
        pool.append(int(num))
        num=""
fichier.close()



###

rate_of_selection=0.28  #parameters for the selection/crossovers/mutations, they are calculated in order to increase the population by 2% at each generation
rate_of_crossover=0.9
rate_of_mutation=0.9
size=len(pool)
initial_size=100 #initial size of the population


### Creation of epsilon, the stop condition of our algorithm and cration of the initial population


def epsilon(pool):
    neg=0
    pos=0
    for k in range (len(pool)):
        if pool[k]>0:
            pos+=1
        if pool[k]<0:
            neg+=1
    mean_size_best_indiv=min(pos,neg)
    epsilon=1/(1+mean_size_best_indiv)
    return epsilon


def create_initial_population():
    
    popu=[]
    for i in range (0,initial_size):
        individual=Individual([randint(0,1) for k in range(0,size)])
        popu.append(list(individual.Chromosome))
    return popu


### Class Individual, contains the Chromosome of the individual and the method to calculate its fitness
    

class Individual :
    
    def __init__(self,Chromosome):
        self.Chromosome=Chromosome
        
        
    def evaluate_fitness(self):
        x=sum([pool[i]*self.Chromosome[i] for i in range(size)]) 
        y=self.Chromosome.count(1)
        return abs(x)+1/(1+y)
    
### Class Population
     
        
class Population :
    
    def __init__(self,Population):
        self.Population=Population
        
        
    
    def select_individuals(self):
        fitness=[evaluate_fitness(self.Population[i]) for i in range(len(self.Population))]
        selection=[]
        n=len(self.Population)
        while len(selection)/n<rate_of_selection:
            position=fitness.index(min(fitness))
            selection.append(self.Population[position])
            del self.Population[position]
            del fitness[position]
        return selection



    def crossover_individuals(self):
        pool_crossover=[]
        while len(pool_crossover)/len(self.Population)<rate_of_crossover:
            u=randint(0,len(self.Population)-1) 
            pool_crossover.append(self.Population[u])
        if len(pool_crossover)%2!=0:
            pool_crossover.pop()
        for k in range(0,len(pool_crossover)-1,2):
            i=randint(1,size-1)
            L1=pool_crossover[k]
            L2=pool_crossover[k+1]
            L1,L2=L1[:i]+L2[i:],L2[:i]+L1[i:]
            pool_crossover[k],pool_crossover[k+1]=L1,L2
        self.Population=self.Population+pool_crossover
        return self.Population



    def mutate_individuals(self):
    
        pool_mutation=[]
    
        while len(pool_mutation)/len(self.Population)<rate_of_mutation:
            n=randint(0,len(self.Population)-1)
            new=list(self.Population[n])
            pool_mutation.append(new)
    
        for k in range(len(pool_mutation)):
            i=randint(0,size-1)
            if pool_mutation[k][i]==1:
                pool_mutation[k][i]=0
            else:
                pool_mutation[k][i]=1  
        self.Population=self.Population+pool_mutation
        return self.Population



    def plague (self):
        if len(self.Population)>200:
            self.Population=list(self.Population[:50]+self.Population[150:])
        return self.Population

    def surprise(self):
        self.Population.append([randint(0,1) for k in range(0,size)])
        return self.Population



### Main loop
        
    
    
    
def main2():
    popu=Population(create_initial_population())
    inc=0
    eps=epsilon(pool)
    fitness=[]
    repetition=0
    best_previous_generation=list(popu.Population[0])
    
    while evaluate_fitness(best_previous_generation)>eps:
        
        popu.mutate_individuals()
        popu=Population.crossover_individuals(popu)
        popu=Population.select_individuals(popu)
        popu=Population.plague(popu)
        popu=Population.surprise(popu)
        
        best=evaluate_fitness(popu.Population[0])
        fitness.append(best)
        inc+=1
        print(len(popu.Population),best)
        
        if popu.Population[0]==best_previous_generation:
            repetition+=1
        
        if popu.Population[0]!=best_previous_generation:
            repetition=0
            
        best_previous_generation=list(popu.Population[0])
        
        if repetition > 20 :
            popu.Population=create_initial_population()
            repetition=0
        
        
        
    fitness.append(evaluate_fitness(popu.Population[0]))
    nb_generations=[i for i in range (0,inc+1)]
    
    print(" ")
    print(evaluate_fitness(popu.Population[0]))
    print(sum([pool[i]*population[0][i] for i in range(size)]))
    print(population[0].count(1))

    plt.plot(nb_generations,fitness)
    plt.show()
    
    return 0













