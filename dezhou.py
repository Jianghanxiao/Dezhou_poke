import itertools

ALL_SYMBOL = ('a', 'b', 'c', 'd')
ALL_CARD_SYMBOL = ('0','A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
ALL_CARDS = [symbol+ALL_CARD_SYMBOL[number] for symbol in ALL_SYMBOL for number in range(2, 15)]
ORDER_LIST = ["hjths", "ths", "sitiao", "hl", "th", "sz", "santiao", "ld", "yd", "gp"]


def convertSymbol(x):
    m = x[0]
    n = x[1:]
    if m == "a":
       symbol = "红桃"
    if m == "b":
       symbol = "方片"
    if m == "c":
       symbol = "黑桃"
    if m == "d":
       symbol = "草花"
    return symbol+n

def shunzi(x, n):
    if n == 0 or n > 10:
        raise ValueError("Coding Bug")
    cards = []
    for i in range(5):
        cards.append(x+ALL_CARD_SYMBOL[n+i])
    return tuple(cards)

def printPrior(symbol, number):
    print(f"{symbol}: {number} / 311875200 = {number / 311875200.0}\n")    

def leftHJTHS(pool):
    all_hjths = []
    for symbol in ALL_SYMBOL:
        all_hjths.append(shunzi(symbol, 10))

    min_left = 5
    left = 0
    for hjths in all_hjths:
        left = 0
        for i in range(5):
            if hjths[i] not in pool:
                left += 1
        min_left = min(left, min_left)

    return min_left

def leftTHS(pool):
    all_ths = []
    for symbol in ALL_SYMBOL:
        for number in range(1, 11):
            all_ths.append(shunzi(symbol, number))
    min_left = 5
    left = 0
    for ths in all_ths:
        left = 0
        for i in range(5):
            if ths[i] not in pool:
                left += 1
        min_left = min(left, min_left)

    return min_left

def statNum(pool):
    numbers = {}
    for i in pool:
        n = i[1:]
        if n not in numbers:
            numbers[n] = 0
        numbers[n] += 1
    return numbers

def leftTIAO(n,pool):
    numbers = statNum(pool)
    return max(n - max(numbers.values()), 0)

def leftHULU(pool):
    numbers = statNum(pool)
    values = list(numbers.values())
    values.sort()
    first = values[-1]
    if len(values) == 1:
        second = 0
    else:
        second = values[-2]
    
    return max(3-first, 0) + max(2-second, 0)

def leftTONGHUA(pool):
    symbols = {}
    for i in pool:
        n = i[0]
        if n not in symbols:
            symbols[n] = 0
        symbols[n] += 1
    return 5 - max(symbols.values())

def leftSZ(pool):
    all_ths = []
    for number in range(1, 11):
        all_ths.append(shunzi('a', number))

    modified_pool = []
    for i in pool:
        modified_pool.append("a" + i[1:])

    min_left = 5
    left = 0
    for hjths in all_ths:
        left = 0
        for i in range(5):
            if hjths[i] not in modified_pool:
                left += 1
        min_left = min(left, min_left)
    return min_left

def leftLD(pool):
    numbers = statNum(pool)
    values = list(numbers.values())
    values.sort()
    first = values[-1]
    if len(values) == 1:
        second = 0
    else:
        second = values[-2]
    
    return max(2-first, 0) + max(2-second, 0)

def leftGAOPAI(pool):
    for i in pool:
        if "A" in i:
            return 0
    
    return 1

def calculateCombinartion(x, n):
    prob = 1.0
    for i in range(n):
        prob *= (x-i)
        prob /= (i+1)
    return prob

def calculateProb(pool):
    current_size = len(pool)
    max_left = 7 - current_size
    cards_unknown = 52 - current_size
    prob = {}
    prob["皇家同花顺"] = leftHJTHS(pool)
    prob["同花顺"] = leftTHS(pool)
    prob["四条"] = leftTIAO(4, pool)
    prob["葫芦"] = leftHULU(pool)
    prob["同花"] = leftTONGHUA(pool)
    prob["顺子"] = leftSZ(pool)
    prob["三条"] = leftTIAO(3, pool)
    prob["两对"] = leftLD(pool)
    prob["一对"] = leftTIAO(2, pool)
    prob["高牌"] = leftGAOPAI(pool)

    for k, v in prob.items():
        if v > max_left:
            prob[k] = -100
    print("Currently the total possibilities of the left cards")
    print(calculateCombinartion(cards_unknown, max_left))
    print("The left cards for each case")
    print(prob)

if __name__ == "__main__":
    print("Game Start\n\n")
    print("Prior Probability:\n")
    printPrior("皇家同花顺", 4)
    printPrior("同花顺", 40)
    printPrior("四条", 624)
    printPrior("葫芦", 3744)
    printPrior("同花", 5148)
    printPrior("顺子", 10240)
    printPrior("三条", 45864)
    printPrior("两对", 269568)
    printPrior("一对", 1528800)
    printPrior("高牌", 999600) 
    
    print("######################################################################")
    print("Please input your two cards: (a: 红桃, b: 方片, c:黑桃, d:草花)")
    a, b = input().split(" ")
    print(f"Your cards are {convertSymbol(a)} {convertSymbol(b)}\n\n")

    mypool = [a, b]
    otherpool = []
    print("Below is the stats of my current cards:\n")
    calculateProb(mypool)
    print("\n\n")
    
    print("######################################################################")
    print("Round 1: Please input your three cards: (a: 红桃, b: 方片, c:黑桃, d:草花)")
    d, e, f = input().split(" ")
    print(f"New cards are {convertSymbol(d)} {convertSymbol(e)} {convertSymbol(f)}\n\n")
    mypool += [d, e, f]
    otherpool = [d, e, f]
    print("Below is the stats of my current cards:")
    calculateProb(mypool)
    print("\n\n")
    print("Below is the stats of other people:")
    calculateProb(otherpool)
    print("\n\n")

    print("######################################################################")
    print("Round 2: Please input your three cards: (a: 红桃, b: 方片, c:黑桃, d:草花)")
    g = input()
    print(f"New cards are {convertSymbol(g)}\n\n")
    mypool += [g]
    otherpool += [g]
    print("Below is the stats of my current cards:")
    calculateProb(mypool)
    print("\n\n")
    print("Below is the stats of other people:")
    calculateProb(otherpool)
    print("\n\n")

    print("######################################################################")
    print("Round 3: Please input your three cards: (a: 红桃, b: 方片, c:黑桃, d:草花)")
    h = input()
    print(f"New cards are {convertSymbol(h)}\n\n")
    mypool += [h]
    otherpool += [h]
    print("Below is the stats of my current cards:")
    calculateProb(mypool)
    print("\n\n")
    print("Below is the stats of other people:")
    calculateProb(otherpool)
    print("\n\n")