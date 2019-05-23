from random import *
from math import *

global rate_of_selection,rate_of_crossover,rate_of_mutation,pool,size,initial_size,eps
rate_of_selection=0.5
rate_of_crossover=0.2
rate_of_mutation=0.2
pool=[randrange(-100, 100) for i in range(3000)]
size=len(pool)
initial_size=100
eps=1/(1+size/3)**2



class Individual :
    
    ##Définition d'une solution courante 
    
    def __init__(self,Chromosome):
        self.Chromosome=Chromosome
    
    # Calcul de la finesse de l'individu
    
    def evaluate_fitness(self):
        #print(len([self.Chromosome[i] for i in range(0,size-1)]))
        x=sum([pool[i]*self.Chromosome[i] for i in range(size)]) #WARNING
        y=self.Chromosome.count(1)
        return abs(x)+1/(1+y)**2

    

#test=Individual([0,0,0,0,0,0,1])
#print(test.evaluate_fitness())
#print (test.Chromosome)





class Population() :

    def __init__(self,Population):
        self.Population=Population
        

    def select_individuals(self):
        fitness=[self.Population[i].evaluate_fitness() for i in range(len(self.Population))]
        selection=[]
        n=len(self.Population)
        while len(selection)/n<rate_of_selection:
            position=fitness.index(min(fitness))
            selection.append(self.Population[position])
            del self.Population[position]
            del fitness[position]
        return Population(selection)

    def crossover_individuals(self):
        pool_crossover=[]
        while len(pool_crossover)/len(self.Population)<rate_of_crossover:
            u=randint(0,len(self.Population)-1) 
            pool_crossover.append(self.Population[u])
        if len(pool_crossover)%2!=0:
            pool_crossover.pop()
        for k in range(0,len(pool_crossover)-1,2):
            i=randint(1,size-1)
            L1=pool_crossover[k].Chromosome
            L2=pool_crossover[k+1].Chromosome
            L1,L2=L1[:i]+L2[i:],L2[:i]+L1[i:]
            pool_crossover[k].Chromosome,pool_crossover[k+1].Chromosome=L1,L2
        return Population(self.Population+pool_crossover)

    def mutate_individuals(self):
        pool_mutation=[]
        while len(pool_mutation)/len(self.Population)<rate_of_mutation:
            u=randint(0,len(self.Population)-1)
            pool_mutation.append(self.Population[u])
        for k in range(len(pool_mutation)):
            i=randint(0,size-1)
            if pool_mutation[k].Chromosome[i]==1:
                pool_mutation[k].Chromosome[i]=0
            else:
                pool_mutation[k].Chromosome[i]=1
        return Population(self.Population+pool_mutation)
    

def create_initial_population():
    
    Liste=[]
    for i in range (0,initial_size):
        Liste.append(Individual([randint(0,1) for k in range(0,size)]))
    population=Population(Liste)
    return population


def main():
    population=create_initial_population()
    inc=0
    results=[]
    while population.Population[0].evaluate_fitness()>eps and inc<size*100:
        population=population.select_individuals()
        population=population.crossover_individuals()
        population=population.mutate_individuals()
        inc+=1
    population=population.select_individuals()
    print(population.Population[0].evaluate_fitness())
    print(sum([pool[i]*population.Population[0].Chromosome[i] for i in range(size)]))
    print(population.Population[0].Chromosome.count(1))
    return 0
