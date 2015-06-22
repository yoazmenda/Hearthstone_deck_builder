import json
from hearthbreaker.agents.basic_agents import RandomAgent
from hearthbreaker.cards.heroes import hero_for_class
from hearthbreaker.constants import CHARACTER_CLASS
from hearthbreaker.engine import Game, Deck, card_lookup
from hearthbreaker.cards import *
import timeit
from random import choice, uniform
from run_games import load_deck
from hearthbreaker.agents.basic_agents import DoNothingAgent
from tests.agents.testing_agents import SelfSpellTestingAgent, EnemySpellTestingAgent, OneCardPlayingAgent, \
    EnemyMinionSpellTestingAgent, CardTestingAgent, PlayAndAttackAgent
from math import pow, log2, floor
from hearthbreaker.agents.trade_agent import TradeAgent
from locale import currency

def fight(deck1, deck2):
    'battle between two decks and return the winner using the trade bot'
    d1 = deck1.copy()
    d2 = deck1.copy()
    game = Game([d1, d2], [RandomAgent(), RandomAgent()])
    game.start()
    winner = game.players[0].deck
    if game.players[0].hero.dead == True:
        winner = game.players[1].deck 
    
    if list(map(lambda card :card.name, winner.cards[0:30])) == list(map(lambda card :card.name, deck1.cards[0:30])):
        return deck1
    elif list(map(lambda card :card.name, winner.cards[0:30])) == list(map(lambda card :card.name, deck2.cards[0:30])):
        return deck2
    else:
        print("---------errror compareing decks in fight")
        print(list(map(lambda card :card.name, winner.cards)))
        print(list(map(lambda card :card.name, deck1.cards)))
        print(list(map(lambda card :card.name, deck2.cards)))
    return -1

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
    decks = []
    for _i in range(0,pop_size):
        decks.append(create_random_deck())  
    print("population initialized: %d individuals " %len(decks))
    return decks
  
def evaluate(population):
    'run a single elimination tournament on the entire population'       
    n = len(population)
    current_players = list(population) #don't want to lose original it's a different list with same pointers
    #single elimination tournament
    while n > 1:           
        winners = []                
        for _i in range(0,1+int(floor((n-1)/2))): #run n/2 battles            
            #this is a single battle
            #take the first two players and make them fight
            deck1 = current_players[0]
            deck2 = current_players[1]
            winner = fight(deck1, deck2)
            if winner == deck1:
                deck2.fitness = 1/float(n)
                winners.append(deck1)    
            else:
                deck1.fitness = 1/float(n)
                winners.append(deck2)                              
            #remove both players from the contestants
            current_players.remove(deck1)                
            current_players.remove(deck2)
        
        #after all the n/2 battles are over, the players for the next round are this round's winners
        current_players = winners       
        n = n / 2
    winner = winners[0]
    winner.fitness = 1
    return population

def select_parents(population):    
    mating_pool = []
    n = len(population)    
    population.sort(key=lambda deck:-deck.fitness)    
    for _i in range(0, n):               
        num = uniform(0.000001,1+(log2(n))/2)
        #print("range: [0, %f]" %(1+(log2(n))/2))    
        individual = 0
        left = 0
        
        while  not (num > left and num <= left+population[individual].fitness):
         #   print("num: %f, current: %f" %(num, current))
            left += population[individual].fitness
            individual += 1  
          #  print ("individual: %d" %individual)
        mating_pool.append(population[individual])        
        print("adding parent %d" %individual) 
    return mating_pool
  
def do_crossover(population):
    return population

def do_mutate(population):
    return population

def start():
    init_system()
    k=6
    pop_size = int(pow(2,k)) #population size - a power of two
    generation_limit = 1 # stopping condition
    
    #Genetic Algorithm
    population = init_population(pop_size) #list of N randomized individuals (decks) with fitness = 0
    generation = 0  
    while generation < generation_limit: #stopping condition
        population = evaluate(population) #make a single-elimination-tournament and assign fitness to each individual
        mating_pool = select_parents(population) #use fitness proportioned selection (roulette wheel technique) to select parents
        population = do_crossover(mating_pool) #create next generation from mating pool with crossover. survivor selection: children replace parents
        population = do_mutate(population) #choose some individuals and mutate them
        generation += 1
        
cards = []
if __name__ == "__main__":
    print(timeit.timeit(start, 'gc.enable()', number=1))
    print("Done")