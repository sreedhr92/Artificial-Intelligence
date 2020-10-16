import copy
def get_symbol(symbol):
    if len(symbol) == 2:
        return len(symbol),symbol[1]
    else:
        return len(symbol),symbol


def get_pure_symbol(clauses,symbols,model):
    for i in symbols:
        flag = 0
        for j in clauses:
            for k in j:
                l,s = get_symbol(k)
                if l == 2 and s == i:
                    flag = 1
        if flag == 0:
            return i,True
    
    for i in symbols:
        flag = 0
        for j in clauses:
            for k in j :
                l,s = get_symbol(k)
                if l == 1 and s == i:
                    flag = 1
        if flag == 0:
            return i,False

    return None,None


def get_unit_clause(clauses):
    for i in clauses:
        if len(i)==1:
            l,symbol = get_symbol(i[0])
            if l == 1:
                return symbol,True
            else:
                return symbol,False
    return None,None


def simplify_clauses(clauses,symbol,value):
    new_clauses = copy.deepcopy(clauses)
    for i in new_clauses:
        for j in i:
            l,symb = get_symbol(j)
            if symb == symbol:
                if value == True:
                    if l == 1:
                        new_clauses.remove(i)
                    else:
                        i.remove(j)
                else:
                    if l == 1:
                        i.remove(j)
                    else:
                        new_clauses.remove(i)
    return new_clauses


def reduce_symbols(symbols,symbol):
    new_symbols = copy.deepcopy(symbols)
    new_symbols.remove(symbol)
    return new_symbols


def contruct_model(model,p,value):
    model[p]=value
    return model


def DPLL(clauses,symbols,model):
    print("Clauses  |",clauses)
    print("Symbols  |",symbols)
    print("Model    |",model)
    print()
    # Base Condition for termination
    # If all the clauses are true,return true
    if len(clauses) == 0:
        return True
    # If some of the clauses are false,return false
    for i in clauses:
        if len(i) == 0:
            return False
    # Removing literals to reduce the search space......
    p,value = get_pure_symbol(clauses,symbols,model)
    if p != None:
        print("---Pure literal Elimination---",p)
        new = reduce_symbols(symbols,p)
        return DPLL(simplify_clauses(clauses, p, value),
             new , contruct_model(model, p, value))

    p,value = get_unit_clause(clauses)
    if p != None:
        print("---Unit literal Elimination---",p)
        new = reduce_symbols(symbols, p)
        return DPLL(simplify_clauses(clauses, p, value),
             new , contruct_model(model, p, value))

    # Selecting first symbol(may be selected any at random) but to improve the search by heuristic
    # select the most occuring symbol to arrive at unit clause or to get pure symbols

    p = symbols[0]
    rest = reduce_symbols(symbols,p)
    print(rest)
    return DPLL(simplify_clauses(clauses, p, True), rest, contruct_model(model, p, True)) or DPLL(simplify_clauses(clauses, p, False), rest, contruct_model(model, p, False))



# The Sentence is represented as Clauses CNF form
clauses = [['~a','~b','c'],['~c','d','~e'],['~a','~b','~e'],['~d','b'],['e','a','~c']]
# other cases clauses = [['~b','c'],['~c'],['a','~b','e'],['d','b'],['e','a','~c']]
symbols = ['a','b','c','d','e']
model = dict()

if DPLL(clauses,symbols,model):
    print("The Sentence is satisfiable")
else :
    print("The Sentence is not satisfiable")

print(model)
'''Output:
Clauses  | [['a', '~b', 'c'], ['~c', 'd', '~e'], ['~a', '~b', 'e'], ['~d', 'b'], ['e', 'a', '~c']]
Symbols  | ['a', 'b', 'c', 'd', 'e']
Model    | {}

['b', 'c', 'd', 'e']
Clauses  | [['~c', 'd', '~e'], ['~b', 'e'], ['~d', 'b']]
Symbols  | ['b', 'c', 'd', 'e']
Model    | {'a': True}

---Pure literal Elimination--- c
Clauses  | [['~b', 'e'], ['~d', 'b']]
Symbols  | ['b', 'd', 'e']
Model    | {'a': True, 'c': False}

---Pure literal Elimination--- e
Clauses  | [['~d', 'b']]
Symbols  | ['b', 'd']
Model    | {'a': True, 'c': False, 'e': True}

---Pure literal Elimination--- b
Clauses  | []
Symbols  | ['d']
Model    | {'a': True, 'c': False, 'e': True, 'b': True}

The Sentence is satisfiable
{'a': True, 'c': False, 'e': True, 'b': True}'''



