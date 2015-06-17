import json
from hearthbreaker.agents.basic_agents import RandomAgent
from hearthbreaker.cards.heroes import hero_for_class
from hearthbreaker.constants import CHARACTER_CLASS
from hearthbreaker.engine import Game, Deck, card_lookup
from hearthbreaker.cards import *
import timeit
from random import choice
from run_games import load_deck
from hearthbreaker.agents.basic_agents import DoNothingAgent
from tests.agents.testing_agents import SelfSpellTestingAgent, EnemySpellTestingAgent, OneCardPlayingAgent, \
    EnemyMinionSpellTestingAgent, CardTestingAgent, PlayAndAttackAgent


def fight(deck1, deck2):
    'battle between two decks and return the winner'
    game = Game([deck1, deck2], [PlayAndAttackAgent(), PlayAndAttackAgent()])
    game.start()
    winner = game.players[0].deck
    if game.players[0].hero.dead == True:
        winner = game.players[1].deck
    del game     
    return winner

def create_random_deck():
    neutrals = choice(range(0,31))
    character_class = choice(range(1,10)) #only normal heroes and must be one of them
    deck = [] #result
    count = 0
    naturals_cards = list(filter(lambda card: card.character_class == CHARACTER_CLASS.ALL, cards)) #filter out hero cards
    class_cards = list(filter(lambda card: card.character_class == character_class, cards)) 
    while count < neutrals:
        card = choice(naturals_cards)
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
        card = choice(class_cards)
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
    'run a single elimination tournament on the entire population'
    
    
    
    
    
    return population

def select_parents(population):
    return population
  
def do_crossover(population):
    return population

def mutate(population):
    return population

def start():
    init_system()  
    pop_size = 8 # population size
    generation_limit = 20 # stopping condition
    generation = 0  
    population = init_population(pop_size) #list of N randomized individuals (decks) with fitness = 0
    
    #Genetic Algorithm
    while generation < generation_limit: #stopping condition
        population = evaluate(population) #make a single-elimination-tournament and assign fitness to each individuals
        mating_pool = select_parents(population) #use fitness proportioned selection (roulette wheel technique) to select parents
        population = do_crossover(mating_pool) #create next generation from mating pool with crossover. survivor selection: children replace parents
        population = mutate(population) #choose some individuals and mutate them
        generation += 1
        
   
    zoo_c = 0;
    bad_c = 0;
    for _i in range(0,100):
        zoo = load_deck("example.hsdeck")
        bad = load_deck("zoo.hsdeck")
        winner = fight(zoo, bad)
        if winner == zoo:
            zoo_c += 1
        else:
            bad_c += 1;
        
    print ("zoo wins: %d" %zoo_c)
    print ("bad wins: %d" %bad_c)
    #print winner:    
    #print(winner.hero) 
    #for card in winner.cards:
    #    print(card.name)
        
        
    


cards = []
if __name__ == "__main__":
    print(timeit.timeit(start, 'gc.enable()', number=1))
    print("Done")