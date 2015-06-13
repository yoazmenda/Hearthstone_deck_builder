import json
from hearthbreaker.agents.basic_agents import RandomAgent
from hearthbreaker.cards.heroes import hero_for_class
from hearthbreaker.constants import CHARACTER_CLASS
from hearthbreaker.engine import Game, Deck, card_lookup
from hearthbreaker.cards import *
import timeit
import run_games

POPULATION = 100 # population size
generation_limit = 20 # stopping condition - adter 20 generations
Pmutate = 0.1 #probability of mutation

def init_population():
  print("initializing population")
  
def evaluate(population):
  print("evaluating")

def select_parents(population):
  print("selecting parents")
  
def do_crossover(population):
  print("performing crossover")

def mutate(population):
  print("performing mutation")

if __name__ == "__main__":
  generation = 0  
  population = init_population() #list of N randomized individuals (decks) with fittness = 0
  
  #Genetic Algorithm
  while generation < generation_limit: #stopping condition
    population = evaluate(population) #make a single-elimination-tournament and assign fittness to n individuals
    mating_pool = select_parents(population) #use fittness proportionate selection (roulette wheel technique) to select parents
    population = do_crossover(mating_pool) #create next generation from mating pool with crossover. survivor selection: children replace parents
    population = mutate(population) #choose some individuals and mutate them
    generation += 1
  
  
  #return some individual from final population
  #winner = population[0]
  print("-------------------------------------------------------")
  print ("Winner is: %s" %"winner")
  print("-------------------------------------------------------")
  
  
  
  
  
  
  