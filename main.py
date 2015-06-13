import json
from hearthbreaker.agents.basic_agents import RandomAgent
from hearthbreaker.cards.heroes import hero_for_class
from hearthbreaker.constants import CHARACTER_CLASS
from hearthbreaker.engine import Game, Deck, card_lookup
from hearthbreaker.cards import *
import timeit
import run_games
import random


card_names = []


def create_random_deck():
   neutrals = random.choice(range(0,31))
   cards = []
   count = 0
   character_class = CHARACTER_CLASS.ALL   
   #select neutrals:
   while count < neutrals:
     card = card_lookup(random.choice(card_names))
     if card.character_class != CHARACTER_CLASS.ALL:
       continue
     prev_count = 0
     for prev in cards:       
       if prev.name == card.name:
         prev_count += 1
     if prev_count == 2:
       continue          
     cards.append(card)
     count += 1
    
    
   #select class specific:
   character_class = random.choice(range(1,10))
   while count < 30:
     card = card_lookup(random.choice(card_names))
     if card.character_class != character_class:
       continue
     prev_count = 0
     for prev in cards:       
       if prev.name == card.name:
         prev_count += 1
     if prev_count == 2:
       continue          
     cards.append(card)
     count += 1
   return Deck(cards, hero_for_class(character_class))
     

     
def init_system():
  create_all_card_names()

def create_all_card_names():
  with open("card_defs.json", "r") as file:
    all_cards = json.load(file)
    for card in all_cards:
      card_names.append(card['name']) 
  
def init_population():  
  print("initializing population")
  decks = []
  for i in range(0,pop_size):
    decks.append(create_random_deck())
  
  print("finish initializing population")
  return decks
  
def evaluate(population):
  pass

def select_parents(population):
  pass
  
def do_crossover(population):
  pass

def mutate(population):
  pass

if __name__ == "__main__":
  init_system()
  
  pop_size = 8 # population size
  generation_limit = 20 # stopping condition - adter 20 generations
  Pmutate = 0.1 #probability of mutation
  
  
  
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

  
  
  
  