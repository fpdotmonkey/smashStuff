import random
import pprint

heroMenuRollNumbers = { "Sizz" : 16, "Sizzle" : 20,
                        "Bang" : 16, "Kaboom" : 20,
                        "Snooze" : 17,
                        "Flame Slash" : 18,
                        "Kacrackle Slash" : 18,
                        "Metal Slash" : 7,
                        "Hatchet Man" : 18,
                        "Whack" : 8, "Thwack" : 12,
                        "Magic Burst" : 5,
                        "Kamikaze" : 5,
                        "Psyche Up" : 16,
                        "Oomph" : 16,
                        "Accelerate" : 16,
                        "Kaclang" : 5,
                        "Bounce" : 16,
                        "Heal" : 7,
                        "Hocus Pocus" : 3,
                        "Zoom" : 15
}
blastZoneZoomNumber = 45
nearMetalOpponentMetalSlashNumber = 45

menuMovePairs = { "Sizz" : "Sizzle", "Sizzle" : "Sizz",
                  "Bang" : "Kaboom", "Kaboom" : "Bang",
                  "Whack" : "Thwack", "Thwack" : "Whack"
}

def generateMovePool(psycheUpEquipped=False,
                     oomphEquipped=False,
                     accelerateEquipped=False,
                     bounceEquipped=False,
                     healAvailable=True,
                     inLastThirtySeconds=False):
    
    movePool = []
    for move in heroMenuRollNumbers:
        if not ((psycheUpEquipped and move == "Psyche Up")
                or (oomphEquipped and move == "Oomph")
                or (accelerateEquipped and move == "Accelerate")
                or (bounceEquipped and move == "Bounce")
                or (not healAvailable and move == "Heal")
                or (inLastThirtySeconds and move == "Kaclang")):
                
            movePool.append(move)

    return movePool
            
def rollMenu(movePool, previousRolledMoves,
             nearBlastZone=False, nearMetalOpponent=False):
    rolledMoves = []
    numberOfMovesInMenu = 4
    
    rollNumbers = {}
    for move in movePool:
        if (previousRolledMoves is None) or (move not in previousRolledMoves):
            rollNumbers[move] = heroMenuRollNumbers[move]

    if nearBlastZone and "Zoom" in rollNumbers:
        rollNumbers["Zoom"] = nearBlastZoneZoomNumber

    if nearMetalOpponent and "Metal Slash" in rollNumbers:
        rollNumbers["Metal Slash"] = nearMetalOpponentMetalSlashNumber

    for i in range(numberOfMovesInMenu):

        rollNumbersAccumulated = {}
        accumulated = 0
        for move, number in rollNumbers.items():
            accumulated = accumulated + number
            rollNumbersAccumulated[accumulated] = move
        
        roll = random.randint(0, accumulated-1)
        for number, move in rollNumbersAccumulated.items():
            if number > roll:
                rolledMoves.append(move)
                break

        del rollNumbers[rolledMoves[-1]]

        try:
            del rollNumbers[menuMovePairs[rolledMoves[-1]]]
        except KeyError:
            pass

    return rolledMoves


def recordMoveFrequency(rolledMoves, frequencyDictionary):
    frequencies = frequencyDictionary
    if len(frequencies) == 0:
        for move in heroMenuRollNumbers:
            if move in rolledMoves:
                frequencies[move] = 1
            else:
                frequencies[move] = 0
    else:
        for move in rolledMoves:
            frequencies[move] = frequencies[move] + 1

    return frequencies
            
            

if "__main__" == __name__:
    sampleMovePool = generateMovePool()

    previousRolledMoves = None
    frequencyDictionary = {}
    numberOfSamples = 10000
    
    for _ in range(numberOfSamples):
        previousRolledMoves = rollMenu(sampleMovePool, previousRolledMoves)
        frequencyDictionary = recordMoveFrequency(previousRolledMoves,
                                                  frequencyDictionary)
        print(previousRolledMoves)

    for (move, frequency) in frequencyDictionary.items():
        frequencyDictionary[move] = frequency / numberOfSamples
        
    pprint.pprint(frequencyDictionary)
