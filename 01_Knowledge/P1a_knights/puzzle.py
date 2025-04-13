from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

structureA = And(
    # A is a knight or a knave but not both:
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
)

structureB = And(
    # B is a knight or a knave but not both:
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
)

structureC = And(
    # C is a knight or a knave but not both:
    And(Or(CKnight, CKnave), Not(And(CKnight, CKnave))),
)

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    structureA,
    
    ### A says "I am both a knight and a knave."
    # If A is a knight, their sentence is true:
    Implication(AKnight, And(AKnight, AKnave)),
    # If A is a knave, their sentence is false:
    Implication(AKnave, Not(And(AKnight, AKnave))),
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    structureA,
    structureB,
    
    ### A says "We are both knaves."
    # If A is a knight, their sentence is true:
    Implication(AKnight, And(AKnave, BKnave)),
    # If A is a knave, their sentence is false:
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    structureA,
    structureB,
    
    ### A says "We are the same kind."
    # If A is a knight, their sentence is true:
    Implication(AKnight, Or(And(AKnave, BKnave), And(AKnight, BKnight))),
    # If A is a knave, their sentence is false:
    Implication(AKnave, Not(Or(And(AKnave, BKnave), And(AKnight, BKnight)))),
    
    ### B says "We are of different kinds."
    # If B is a knight, their sentence is true:
    Implication(BKnight, Or(And(AKnave, BKnight), And(AKnight, BKnave))),
    # If B is a knave, their sentence is false:
    Implication(BKnave, Not(Or(And(AKnave, BKnight), And(AKnight, BKnave))))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    structureA,
    structureB,
    structureC,
    
    ### A says either "I am a knight." or "I am a knave.", but you don't know which.
    # If A is a knight, their sentence is true:
    Implication(AKnight, Or(AKnave, AKnight)),
    # If A is a knave, their sentence is false:
    Implication(AKnave, Not(Or(AKnave, AKnight))),
    
    ### B says "A said 'I am a knave'."
    ##### "A said 'B is a knave'"
    ### If A is a knight, their sentence is true:
    Implication(AKnight, BKnave),
    ### If A is a knave, their sentence is false:
    Implication(AKnave, Not(BKnave)),
    ##### B says "A said 'I am a knave'."
    # If B is a knight, their sentence is true:
    Implication(BKnight, Or(Implication(AKnight, BKnave), Implication(AKnave, Not(BKnave)))),
    # If B is a knave, their sentence is false:
    # Implication(BKnave, Not(Or(Implication(AKnight, BKnave), Implication(AKnave, Not(BKnave))))),
    
    ### B says "C is a knave."
    # If B is a knight, their sentence is true:
    Implication(BKnight, CKnave),
    # If B is a knave, their sentence is false:
    Implication(BKnave, Not(CKnave)),  
    
    ### C says "A is a knight." 
    # If C is a knight, their sentence is true:
    Implication(CKnight, AKnight),
    # If C is a knave, their sentence is false:
    Implication(CKnave, Not(AKnight))  
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
