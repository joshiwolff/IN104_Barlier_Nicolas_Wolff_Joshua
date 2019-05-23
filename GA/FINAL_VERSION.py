from random import *
from math import *
import matplotlib.pyplot as plt

### Global variables 

global rate_of_selection,rate_of_crossover,rate_of_mutation,pool,size,initial_size

###

### Creation of the list with relative integers

file="extraLarge.txt"
pool=[]
fichier=open(file,"r")
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

### Inititialization of the main parameters of the problem

rate_of_selection=0.4  #parameters for the selection/crossovers/mutations, they are calculated in order to increase the population by 2% at each generation
rate_of_crossover=0.9
rate_of_mutation=0.9

size=len(pool) 
initial_size=100 #initial size of the population (number of individuals)

###

### Creation of epsilon, the stop condition of our algorithm and creation of the initial population


def epsilon(pool): # We consider the repartition of the relative integers around zero in the construction of epsilon
    neg=0
    pos=0
    for k in range (len(pool)): 
        if pool[k]>0:
            pos+=1
        if pool[k]<0:
            neg+=1
    print(pos,neg)
    mean_size_best_indiv=min(pos,neg)
    epsilon=1/(1+2*mean_size_best_indiv) 
    return epsilon

###
    
### Function that returns the initial population (its size is initial_size), which is randomly generated

def create_initial_population():
    
    popu=[]
    for i in range (0,initial_size):
        popu.append([randint(0,1) for k in range(0,size)])
    return popu

###

### Class Individual, contains the Chromosome of the individual and the method to calculate its fitness
    

class Individual :
    
    def __init__(self,Chromosome):
        self.Chromosome=Chromosome # A chromosome is a list of 0 and 1 of length size (which is the size of the list studied) that represent a subset of the list studied
        
        
    def evaluate_fitness(self):
        x=sum([pool[i]*self.Chromosome[i] for i in range(size)]) 
        y=self.Chromosome.count(1)
        return abs(x)+1/(1+y) # Fitness function that we chose, x is the absolute distance of the subset sum to zero, y is the length of the subset
    
###
    
### Class Population
        
# Population is the list of the chromosomes of all the individuals
# select_individuals selects the elements of the population with the best fitness (the rate of selection is rate_of_selection)
# crossover_individuals returns the population (type is Population) plus a part of the population where crossovers were applied  
# mutate_individuals returns the population (type is Population) plus a part of the population where crossovers were applied
# plague simulates an epidemia, when the population is too big (more than 500 elements, chosen empirically) we kill 80% of the population to limit the divergence of the populatio size       
# migration simulates (as its name suggest it) a migration, at each generation between 5% and 10% of randomly chosen 
    
class Population :
    
    def __init__(self,Population):
        self.Population=Population
        
        
    
    def select_individuals(self):
        
        
        fitness=[Individual(self.Population[i]).evaluate_fitness() for i in range(len(self.Population))]
        selection=[]
        
        while len(selection)/len(self.Population)<rate_of_selection:
            position=fitness.index(min(fitness))
            selection.append(self.Population[position])
            del self.Population[position]
            del fitness[position]
        
        return Population(selection) # The population is sorted in ascending order of fitness, thereby the best individual is the first element of the population



    def crossover_individuals(self):
        pool_crossover=[]
        while len(pool_crossover)/len(self.Population)<rate_of_crossover:
            u=randint(0,len(self.Population)-1) 
            pool_crossover.append(list(self.Population[u]))
        if len(pool_crossover)%2!=0:
            pool_crossover.pop()
        for k in range(0,len(pool_crossover)-1,2):
            i=randint(1,size-1)
            L1=pool_crossover[k]
            L2=pool_crossover[k+1]
            L1,L2=L1[:i]+L2[i:],L2[:i]+L1[i:]
            pool_crossover[k],pool_crossover[k+1]=L1,L2
        
        return Population(self.Population+pool_crossover)



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
        
        return Population(self.Population+pool_mutation)



    def plague (self):
        pop=Population(self.Population)
        if len(self.Population)>500:
            pop=Population(list(self.Population[:100]))
        return pop
    

    def migration(self): 
        pop=self.Population
        for i in range (0,10):
            pop.append([randint(0,1) for k in range(0,size)])
        return Population(pop)

###

### Main loop
        
# Print epsilon, the size of the population and the best fitness at each generation
# At the end print epsilon, the best fitness, the sum of the elments of the subset, the number of elements of the subset and a graph showing the fitness depending on the generation
            
def main():
    popu=Population(create_initial_population()) # Creation of the initial population
    inc=0 # Counter of generations
    eps=epsilon(pool) # Calculation of epsilon
    print("epsilon :",eps)
    fitness=[] # List of the best fitness of each generation 
    repetition=0 # Counter of the successive occurences of the best element of the population
    best_previous_generation=list(popu.Population[0]) 
    
    while Individual(best_previous_generation).evaluate_fitness()>eps: # Stop condition of the genetic algorithm
        
        popu=popu.mutate_individuals() # Genectic evolution of a generation
        popu=popu.crossover_individuals()
        popu=popu.migration()
        popu=popu.select_individuals()
        popu=popu.plague()
        
        best=Individual(popu.Population[0]).evaluate_fitness() # fitness of the best individual
        fitness.append(best)
        inc+=1
        print("Size of the pop :", len(popu.Population),"/ fitness :",best)
        
        if popu.Population[0]==best_previous_generation: # We check if the best individual is the same as in the previous generation
            repetition+=1
        
        if popu.Population[0]!=best_previous_generation:
            repetition=0
            
        best_previous_generation=list(popu.Population[0])
        
        if repetition > 100 : 
            if best<1: # If we exceed 50 repetitions and if the sum of the elments equals 0, we consider that this individual is a decent solution of the problem
                break
            else: # If we exceed 50 repetitions and if the sum of the elments is different from 0, we consider that it's better to rebuild a new population and to erase the previous one (empirical choice)
                popu=Population(create_initial_population())
                repetition=0
            
        
        
        
    
    nb_generations=[i for i in range (0,inc)]
    
    print(" ")
    print("epsilon :",eps)
    print("best fitness :",Individual(popu.Population[0]).evaluate_fitness())
    print("sum of the elements :", sum([pool[i]*popu.Population[0][i] for i in range(size)]))
    print("number of elements :", popu.Population[0].count(1))

    plt.plot(nb_generations,fitness,'-o')
    plt.xlabel("Number of generations")
    plt.ylabel("Fitness")
    plt.show()
    
    return 0













