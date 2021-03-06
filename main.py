import json
from hearthbreaker.agents.basic_agents import RandomAgent
from hearthbreaker.cards.heroes import hero_for_class
from hearthbreaker.constants import CHARACTER_CLASS
from hearthbreaker.engine import Game, Deck, card_lookup
from hearthbreaker.cards import *
import timeit
from random import choice, uniform, shuffle
from run_games import load_deck
from hearthbreaker.agents.basic_agents import DoNothingAgent
from tests.agents.testing_agents import SelfSpellTestingAgent, EnemySpellTestingAgent, OneCardPlayingAgent, \
    EnemyMinionSpellTestingAgent, CardTestingAgent, PlayAndAttackAgent
from math import pow, log2, floor
from hearthbreaker.agents.trade_agent import TradeAgent
from locale import currency
from functools import reduce

def fight(deck1, deck2):
    'battle between two decks and return the winner using an AI bot'
    d1 = deck1.copy()
    d2 = deck2.copy()
    game = Game([d1, d2], [RandomAgent(), RandomAgent()])
    game.start()
    winner = game.players[0].deck
    if game.players[0].hero.dead == True:
        winner = game.players[1].deck 
    if winner.compare(deck1) == True:
        #print("match deck1")
        return deck1
    elif winner.compare(deck2) == True:
        return deck2
    else:
        print("error in fight - returning deck2")
        return deck2
    return -1
    

def create_random_deck():
    neutrals = choice(range(0,31))
    character_class = choice(range(1,10)) #only normal heroes and must be one of them
    deck = [] #result
    count = 0
    naturals_cards = list(filter(lambda card: card.character_class == CHARACTER_CLASS.ALL, cards)) #filter out hero cards
    class_cards = list(filter(lambda card: card.character_class == character_class, cards)) 
    #create neutrals
    while count < neutrals:
        card = choice(naturals_cards)
        prev_count = 0
        for prev in deck:  #count previous occurrences
            if prev.name == card.name:
                prev_count += 1
        if prev_count == 2:            
            continue                
        deck.append(card)
        count += 1
    #create class specific    
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
    while len(decks) != pop_size:
        newDeck = create_random_deck()
        if isDeckLegal(newDeck) == True:
            decks.append(newDeck)          
    print("population initialized: %d individuals " %len(decks))
    return decks
  
def evaluate(population,battleAmount):
    for individual in population:
        individual.fitness = 0
        individual.drawn = False
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
            
            
            deck1Wins = 0
            deck2Wins = 0
            for _i in range(0,battleAmount):
                fightOk = False
                countStop = 20
                iters = 0
                while fightOk == False:  
                    iters += 1                  
                    try:
                        fightOk = True
                        if iters == countStop:
                            winner = deck1
                        else:
                            winner = fight(deck1, deck2)
                    except:
                        print("fight failed - trying again")
                        fightOk = False
                if winner == deck1:
                    deck1Wins += 1
                else:
                    deck2Wins += 1
            
            
            if deck1Wins >= deck2Wins:
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
        individual = 0
        left = 0        
        while  not (num > left and num <= left+population[individual].fitness):         
            left += population[individual].fitness
            individual += 1            
        mating_pool.append(population[individual])        
    return mating_pool

def isDeckLegal(deck):    
    if len(deck.cards)!=30:
        return "deck more than 30"
    for card in deck.cards:
        if card.character_class != deck.hero.character_class and card.character_class != CHARACTER_CLASS.ALL :#                
                return "deck two heroes"
        count = 0
        for other in deck.cards:
            if card.name == other.name:
                count += 1
                if count == 3:
                    return "deck more than two of same card"
    return True

def crossover(deck1, deck2, prob):
    child1 = deck1.copy()
    child2 = deck2.copy()        
    for i in  range(0,30):
        if uniform(0,1) <= prob:                            
            backup1 = list(child1.cards)
            backup2 = list(child2.cards) 
            temp_swp = child1.cards[i]
            child1.cards[i] = child2.cards[i]
            child2.cards[i] = temp_swp                
            if isDeckLegal(child1) != True or isDeckLegal(child2) != True:
                child1.cards = backup1
                child2.cards = backup2                                                    
    return [child1, child2]
                              
def do_crossover(population, prob):        
    probabilityToSwap = 0.2 #the chance a cards will !*try*! swap between parents
#     shuffle(population)
    for _i in range(0,len(population)-1,2):
        if uniform(0,1) <= prob: #else: parents will leave to next generation
            children = crossover(population[_i], population[_i+1], probabilityToSwap)           
            population[_i] = children[0]
            population[_i+1] = children[1]                               
    return population

def mutate(deck, prob):
    newDeck = deck.copy()    
    for i in range(0,30):
        if uniform(0,1) <=prob:
            mutate_ok = False
            while mutate_ok == False:
                newCard = choice(cards)
                newCard.drawn = False
                newDeck.cards[i] = choice(cards)
                if isDeckLegal(newDeck) == True:
                    mutate_ok= True
    return newDeck                        
    
        
def do_mutate(population,prob):    
    probabilityToChange = 0.2
    for deck in population:
        if uniform(0,1) <= prob:
            mutated_deck = mutate(deck,probabilityToChange)
            population.remove(deck)
            population.append(mutated_deck)
    return population

def test1(gereration_player, population,battleAmount):
    winrate = []
    deck1 = gereration_player                                                
    for deck2 in population:                                          
        deck1Wins = 0
        deck2Wins = 0
        for _i in range(0,battleAmount):
            fightOk = False
            countStop = 20
            iters = 0
            while fightOk == False:  
                iters += 1                  
                try:
                    fightOk = True
                    if iters == countStop:
                        winner = deck1
                    else:
                        winner = fight(deck1, deck2)
                except:
                    print("fight failed - trying again")
                    fightOk = False
            if winner == deck1:
                deck1Wins += 1
            else:
                deck2Wins += 1        
        winrate.append(deck1Wins/(deck1Wins+deck2Wins+0.000001))
    print(reduce(lambda x, y: x + y, winrate) / len(winrate))

            

def start():
    init_system()
    k=5
    battleAmount = 10 #how many battles a pair is fighting - only one fight can be just luck
    xover_prob = 0.2 #should be number in (0,1)
    mutation_prob = 0.4 #should be number in (0,1)
    pop_size = int(pow(2,k)) #population size - a power of two
    generation_limit = 40# stopping condition    
    #Genetic Algorithm    
    population = init_population(pop_size) #list of N randomized individuals (decks) with fitness = 0
    test1_population = init_population(pop_size)                
    generation = 0  
    while generation < generation_limit: #stopping condition
        print("generation: %d" %generation)   
        test1(population[0],test1_population, battleAmount)     
        population = evaluate(population, battleAmount) #make a single-elimination-tournament and assign fitness to each individual
        mating_pool = select_parents(population) #use fitness proportioned selection (roulette wheel technique) to select parents
        population = do_crossover(mating_pool, xover_prob) #create next generation from mating pool with crossover. survivor selection: children replace parents
        population = do_mutate(population, mutation_prob) #choose some individuals and mutate them
        generation += 1        
               
cards = []
if __name__ == "__main__":
    print(timeit.timeit(start, 'gc.enable()', number=1))
    print("Done")
