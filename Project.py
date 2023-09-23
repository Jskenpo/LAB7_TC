''' 
Universidad del Valle de Guatemala
Facultad de Ingeniería
Ingeniería en Ciencia de la Computación y Tecnologías de la Información

Teoria de la Computación 
SECCION - 20

Autores:
    Jose Santisteban 21553
    Sebastian Solorzano 21826
    Manuel Rodas 21509
'''

import graphviz

def convert_optional(regex):
    return regex.replace('?', '|E')


def convertir_expresion(expresion):
    lista = list(expresion)
    alfabeto = []
    operandos = ['+','.','*','|','(',')','[',']','{','}','?']

    for i in lista:
        if i not in operandos:
            if i not in alfabeto:
                alfabeto.append(i)

    alfabeto.append('')
    
        
    for i in range(len(lista)):
        if i > 0:
            before = lista[i - 1]
            if lista[i] == '+':
                if before not in ')]}':
                    lista[i - 1] = lista[i - 1] + lista[i - 1] + '*'
                else:
                    almacen = []
                    aperturas = 0
                    for j in range(i - 1, -1, -1):
                        if lista[j] in ')]}':
                            aperturas += 1
                            almacen.append(lista[j])
                        elif lista[j] in '([{':
                            aperturas -= 1
                            almacen.append(lista[j])
                        else:
                            almacen.append(lista[j])
                        if aperturas == 0:
                            break
                    almacen.reverse()
                    lista[i] = ''.join(almacen) + '*'
    if '+' in lista:
        lista.remove('+')
    return ''.join(lista), alfabeto


def infix_postfix(infix):
    caracteres_especiales = {'*': 60, '.': 40, '|': 20}
    exp_postfix, stack = "", ""  

    for c in infix:        
        if c == '(':
            stack = stack + c 
        elif c == ')':
            while stack[-1] != '(':  
                exp_postfix = exp_postfix + stack[-1]  
                stack = stack[:-1]  
            stack = stack[:-1]  
        elif c in caracteres_especiales:
            while stack and caracteres_especiales.get(c, 0) <= caracteres_especiales.get(stack[-1], 0):
                exp_postfix, stack = exp_postfix + stack[-1], stack[:-1]
            stack = stack + c
        else:
            exp_postfix = exp_postfix + c

    while stack:
        exp_postfix, stack = exp_postfix + stack[-1], stack[:-1]

    return exp_postfix


class estado:
    label = None
    transicion1 = None 
    transicion2 = None 
    id = None


class afn:
    inicial, accept = None, None

    def __init__(self, inicial, accept):
        self.inicial, self.accept = inicial, accept

    def get_all_transitions(self):
        transitions = []
        estados = 0 
        transiciones = []

        def visit(estado):
            nonlocal transitions
            nonlocal estados 
            nonlocal transiciones
            estados += 1
            if estado.transicion1 is not None:
                transition = (estado, estado.label, estado.transicion1)
                transiciones.append((estados,estado.label, estado.transicion1))
                if transition not in transitions:
                    transitions.append(transition)
                    visit(estado.transicion1)
            if estado.transicion2 is not None:
                transition = (estado, estado.label, estado.transicion2)
                transiciones.append((estados,estado.label, estado.transicion2))
                if transition not in transitions:
                    transitions.append(transition)
                    visit(estado.transicion2)
        visit(self.inicial)
        self.transitions = transitions
        self.transiciones = transiciones
        return transiciones
   

def postfix_afn(exp_postfix):
    afnstack = []
    epsilon = 'E'

    for c in exp_postfix:
        if c == '*':
            afn1 = afnstack.pop()
            inicial, accept = estado(), estado()
            inicial.transicion1, inicial.transicion2 = afn1.inicial, accept
            afn1.accept.transicion1, afn1.accept.transicion2 = afn1.inicial, accept
            afnstack.append(afn(inicial, accept))
        elif c == '.':
            afn2, afn1 = afnstack.pop(), afnstack.pop()
            afn1.accept.transicion1 = afn2.inicial
            afnstack.append(afn(afn1.inicial, afn2.accept))
        elif c == '|':
            afn2, afn1 = afnstack.pop(), afnstack.pop()
            inicial = estado()
            inicial.transicion1, inicial.transicion2 = afn1.inicial, afn2.inicial
            accept = estado()
            afn1.accept.transicion1, afn2.accept.transicion1 = accept, accept
            afnstack.append(afn(inicial, accept))
        
        elif c == 'E':
            accept, inicial = estado(), estado()
            inicial.transicion1 = accept
            afnstack.append(afn(inicial, accept))
        else:
            accept, inicial = estado(), estado()
            inicial.label, inicial.transicion1 = c, accept
            afnstack.append(afn(inicial, accept))

    return afnstack.pop()


def graficar_afn(afn):
    dot = graphviz.Digraph(format='png')
    estados = 0  

    def add_estados_edges(node, visited):
        nonlocal estados
        if node in visited:
            return
        visited.add(node)
        estados += 1

        dot.node(str(id(node)), label=f'q{estados}')

        if node.transicion1:
            label = node.transicion1.label if node.transicion1.label else 'ε'
            dot.edge(str(id(node)), str(id(node.transicion1)), label=label)
            add_estados_edges(node.transicion1, visited)
        if node.transicion2:
            label = node.transicion2.label if node.transicion2.label else 'ε'
            dot.edge(str(id(node)), str(id(node.transicion2)), label=label)
            add_estados_edges(node.transicion2, visited)

    #agregar estado inicial

    add_estados_edges(afn.inicial, set())

    dot.render('afn_graph', view=True)


def seguimiento(estado):
    estados = set()
    estados.add(estado)

    if estado.label is None:
        if estado.transicion1 is not None:
            estados |= seguimiento(estado.transicion1)
        if estado.transicion2 is not None:
            estados |= seguimiento(estado.transicion2)
    return estados


class AFD:
    def __init__(self):
        self.estados = set()
        self.transitions = {}
        self.inicial = None
        self.accept = set()


def afn_to_afd(afn, alphabet):
    afd = AFD()
    estado_inicial = frozenset(seguimiento(afn.inicial))
    afd.inicial = estado_inicial
    afd.estados.add(estado_inicial)
    stack = [estado_inicial]

    while stack:
        actual_estado = stack.pop()
        for char in alphabet:
            next_estados = set()
            for afn_estado in actual_estado:
                if afn_estado.label == char:
                    next_estados |= seguimiento(afn_estado.transicion1)
            next_estado = frozenset(next_estados)
            if next_estado:
                afd.transitions[(actual_estado, char)] = next_estado
                if next_estado not in afd.estados:
                    afd.estados.add(next_estado)
                    stack.append(next_estado)
    
    for estado in afd.estados:
        if afn.accept in estado:
            afd.accept.add(estado)
    
    return afd


def label_estados(estados):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    estado_labels = {}

    for i, estado in enumerate(estados):
        if i < len(alphabet):
            estado_labels[estado] = alphabet[i]
        else:
            estado_labels[estado] = str(i)

    return estado_labels


def graficar_afd(afd):
    dot = graphviz.Digraph(format='png')
    estado_labels = label_estados(afd.estados)  
  
    for estado in afd.estados:
        label = estado_labels[estado]
        if estado in afd.accept:
            dot.node(label, shape='doublecircle')
        else:
            dot.node(label)

    inicial_label = estado_labels[afd.inicial]
    dot.node('inicial', shape='none')
    dot.edge('inicial', inicial_label)

    for (estado1, char), estado2 in afd.transitions.items():
        dot.edge(estado_labels[estado1], estado_labels[estado2], label=char)

    return dot


def minimizar_afd(afd):
    marcados = {}
    for estado1 in afd.estados:
        for estado2 in afd.estados:
            if estado1 != estado2 and ((estado1 in afd.accept and estado2 not in afd.accept) or (estado1 not in afd.accept and estado2 in afd.accept)):
                marcados[(estado1, estado2)] = True
            else:
                marcados[(estado1, estado2)] = False

    cambiado = True
    while cambiado:
        cambiado = False
        for estado1 in afd.estados:
            for estado2 in afd.estados:
                if not marcados[(estado1, estado2)]:
                    for char in alfabeto:
                        siguiente_estado1 = afd.transitions.get((estado1, char), None)
                        siguiente_estado2 = afd.transitions.get((estado2, char), None)
                        if siguiente_estado1 is not None and siguiente_estado2 is not None and marcados[(siguiente_estado1, siguiente_estado2)]:
                            marcados[(estado1, estado2)] = True
                            cambiado = True

    afd_minimizado = AFD()
    mapeo_estados = {}

    for estado in afd.estados:
        if estado not in mapeo_estados:
            mapeo_estados[estado] = frozenset([estado])
            if estado in afd.accept:
                afd_minimizado.accept.add(mapeo_estados[estado])
            afd_minimizado.estados.add(mapeo_estados[estado])

        for char in alfabeto:
            siguiente_estado = afd.transitions.get((estado, char), None)
            if siguiente_estado is not None:
                if siguiente_estado not in mapeo_estados:
                    mapeo_estados[siguiente_estado] = frozenset([siguiente_estado])
                    if siguiente_estado in afd.accept:
                        afd_minimizado.accept.add(mapeo_estados[siguiente_estado])
                    afd_minimizado.estados.add(mapeo_estados[siguiente_estado])
                afd_minimizado.transitions[(mapeo_estados[estado], char)] = mapeo_estados[siguiente_estado]

    afd_minimizado.inicial = mapeo_estados[afd.inicial]

    return afd_minimizado


def simulacion_afn(string, afn):   
    actual = set()
    siguiente = set()
    actual |= seguimiento(afn.inicial)

    for s in string:
        for c in actual:
            if c.label == s:
                siguiente |= seguimiento(c.transicion1)
        actual = siguiente
        siguiente = set()
    return (afn.accept in actual)


def simulacion_afd(afd, w):
    estado_labels = label_estados(afd.estados)
    actual = afd.inicial

    for char in w:
        actual = afd.transitions[(actual, char)]
    
    return actual in afd.accept


def simulacion_afd_minimizado(afd_minimizado, w):
    actual = afd_minimizado.inicial

    for char in w:
        actual = afd_minimizado.transitions.get((actual, char), None)
        if actual is None:
            return False

    return actual in afd_minimizado.accept


def leer_expresion_y_cadena(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        lineas = archivo.readlines()
        expresion = lineas[0].strip()
        cadena = lineas[1].strip()
    return expresion, cadena

nombre_archivo = 'expresion_cadena.txt'
expresion, cadena = leer_expresion_y_cadena(nombre_archivo)

infix = convert_optional(expresion)
infix,alfabeto = convertir_expresion(infix)
postfix = infix_postfix(infix)
afn = postfix_afn(postfix)
graficar_afn(afn)
afd = afn_to_afd(afn, alfabeto)
estado_labels = label_estados(afd.estados)
graficar_afd(afd).render('afd_graph', view=True)
afd_min = minimizar_afd(afd)
graficar_afd(afd_min).render('afd_minimizado_graph', view=True)
print('el resultado de la simulación del afn  es:',simulacion_afn(cadena, afn))
print('el resultado de la simulación del afd  es:',simulacion_afd(afd, cadena))
print('El resultado de la simulación del AFD minimizado es:', simulacion_afd_minimizado(afd_min, cadena))