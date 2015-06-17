import json
from hearthbreaker.cards.heroes import hero_for_class
from hearthbreaker.constants import CHARACTER_CLASS
from hearthbreaker.engine import Deck, card_lookup
import timeit
import random

cards = []

def create_random_deck():
    neutrals = random.choice(range(0,31))
    character_class = random.choice(range(1,10)) #only normal heroes and must be one of them
    deck = [] #result
    count = 0
    naturals_cards = list(filter(lambda card: card.character_class == CHARACTER_CLASS.ALL, cards)) #filter out hero cards
    class_cards = list(filter(lambda card: card.character_class == character_class, cards)) 
    while count < neutrals:
        card = random.choice(naturals_cards)
        prev_count = 0
        for prev in deck:  #count previous occurrences
            if prev.name == card.name:
                prev_count += 1
        if prev_count == 2:
            #naturals_cards.remove(card)
            continue                
        deck.append(card)
        count += 1

    while count < 30:
        card = random.choice(class_cards)
        prev_count = 0
        for prev in cards:  #count previous occurrences
            if prev.name == card.name:
                prev_count += 1
        if prev_count == 2:
            #class_cards.remove(card)
            continue                
        deck.append(card)
        count += 1
    return Deck(deck, hero_for_class(character_class))
     

     
def init_system():
    create_cards()

def create_cards():
    with open("card_defs.json", "r") as file:
        json_cards = json.load(file)
        for card in json_cards:
            cards.append(card_lookup(card['name']))
  
def init_population(pop_size):  
    print("initializing population")
    decks = []
    for _i in range(0,pop_size):
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

def start():
    init_system()  
    pop_size = 8 # population size
    generation_limit = 20 # stopping condition
    generation = 0  
    population = init_population(pop_size) #list of N randomized individuals (decks) with fitness = 0
    
    #Genetic Algorithm
    while generation < generation_limit: #stopping condition
        population = evaluate(population) #make a single-elimination-tournament and assign fitness to n individuals
        mating_pool = select_parents(population) #use fitness proportioned selection (roulette wheel technique) to select parents
        population = do_crossover(mating_pool) #create next generation from mating pool with crossover. survivor selection: children replace parents
        population = mutate(population) #choose some individuals and mutate them
        generation += 1
  



if __name__ == "__main__":
    print(timeit.timeit(start, 'gc.enable()', number=1))
    print("Done")