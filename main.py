import re

from Atom import Atom
from Clause import Clause
from Formula import Formula

file = open('sentence.txt')
lines = file.readlines()

operators = {
    '|': 1,
    '&': 2,
    '>': 3,
    '=': 4,
    '-': 5,
    '(': -1,
    ')': -2
}
def infijo2postfijo(infijo):
    postfijo = []
    pila = []
    for ch in infijo:
        p=get_prioridad(ch)
        if p == -1:
            pila.append(ch)
        elif p == -2:
    #Extraer el elemento del tope de la pila e introducir a postfijo,
    # hasta encontrar (  pero no introducir el paréntesis a postfijo.
            while (len(pila) > 0):
                tope = pila.pop()
                if (tope != "("):
                    postfijo.append(tope)
                else:
                    break
        elif p > 0:
    # la pila esta vacı́a or ch tiene
    # más alta prioridad que el elemento del tope de la pila
            if len(pila) == 0 or p > get_prioridad(pila[-1]):
                pila.append(ch)
    # Extraer el elemento del tope de la pila e introducir a postfijo.
    # Y repetir la comparación con el nuevo tope
            else:
                while len(pila)>0 and p < get_prioridad(pila[-1]):
                    tope = pila.pop()
                    postfijo.append(tope)
                pila.append(ch)
        else:
            postfijo.append(ch)
    while len(pila) > 0:
        postfijo.append(pila.pop())
    return postfijo

def get_prioridad(operator):
    return 0 if not operator in operators else operators[operator]


def evaluar(postfijo):
    pila = []
    for ch in postfijo:
        print(f'ch: {ch}')
        p = get_prioridad(ch)
        if p == 0: #Si es igual a 0 es un operando y se convierte en formula y mete a pila
            a = Atom(ch)
            c = Clause()
            f = Formula()
            c = c.or_atom(a)
            f = f.and_clause_formula(c)
            pila.append(f)
        elif p == 1: #Si es igual a 1 es or y se convierte en formula y mete a pila
            b = pila.pop()
            a = pila.pop()

            print(f'or a:{a} b:{b}\n')
            c = a.or_formula(b)
            pila.append(c)
        elif p == 2: #2 es igual a And y se convierte en formula y mete a pila
            b = pila.pop()
            a = pila.pop()
            print(f'and a:{a} b:{b}\n')
            c = a.and_formula(b)
            pila.append(c)
        elif p == 3: #3 es entonces y se convierte en formula y mete a pila
            b = pila.pop()
            a = pila.pop()
            a = a.not_formula()
            c = a.or_formula(b)
            pila.append(c)
        elif p == 4: #4 es Si solo Si y se convierte en formula y mete a pila
            b = pila.pop()
            a = pila.pop()
            an = a.not_formula()
            bn = b.not_formula()
            c = a.or_formula(bn)
            d = b.or_formula(an)
            c = c.and_formula(d)
            pila.append(c)
            # pila.append(c) #No esta completo
        elif p == 5: #5 es Not y convierte en formula y mete a pila
            a = pila.pop()
            c = a.not_formula()  #Falta por hacer
            pila.append(c)
    return pila.pop() #No esta completo

for linea in lines:
    print(f'{linea}')
    infijo = re.findall("(\\w+|\\||\\&|\\>|\\-|\\(|\\)|\\=)",linea)
    postfijo = infijo2postfijo(infijo)
    fnc = evaluar(postfijo)
    print(f'FNC: \n{fnc}\n')


# sinTautologia = fnc.delete_tautologia()
# print(f'{sinTautologia}\n')
# david_putnam = sinTautologia.get_david_putman()
# print(f'{david_putnam}')

# print(fnc.get_david_putman())

