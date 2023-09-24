import re


# Función para validar que una línea de producción esté bien escrita
def validate_production(production):
    production_regex = r'([A-Z]) → (([A-Z]|[a-z]|[0-9]|\||\s|ε)*)'
    if re.match(production_regex, production):
      return True
    else:
      return False


# Clase para representar una gramática
class Grammar:

    def __init__(self):
        self.productions = []
        self.non_terminals = []
        self.start_symbol = None

        # Método para agregar una producción
    def add_production(self, production):
        if validate_production(production):
            self.productions.append(production)
            left_symbol = production.split(' → ')[0]
            if left_symbol not in self.non_terminals:
                self.non_terminals.append(left_symbol)
            if self.start_symbol is None:
                self.start_symbol = production.split(' → ')[0]
        else:
            print("Producción inválida")

    # Método para eliminar producciones epsilon
    def remove_epsilon_productions(self):

        # Encontrar símbolos y producciones anulables
        nullable_symbols = []
        nullable_productions = []

        for production in self.productions:
            if production.endswith('ε'):
                nullable_symbols.append(production[0])
                nullable_productions.append(production)

        # Reformular producciones
        new_productions = set()

        for production in self.productions:

            if production.endswith('ε'):

                # Dividir producción
                left, body = production.split(' → ')

                # Reemplazar símbolos anulables
                body_modified = False
                for symbol in nullable_symbols:
                    if symbol in body:
                        body = body.replace(symbol, '')
                        body_modified = True

                # Reconstruir y agregar solo si hubo cambios
                if body_modified:
                    new_production = left + ' → ' + body
                    new_productions.add(new_production)

            else:

                # Agregar directamente producciones sin epsilon
                new_productions.add(production)

        # Actualizar producciones
        self.productions = []
        for production in new_productions:
            self.productions.append(production)
    def remove_unary_productions(self):

        unary_productions = []

        for production in self.productions:
            if production.count('-') == 1:
                unary_productions.append(production)

        for production in unary_productions:
            self.productions.remove(production)

    # Eliminar símbolos inútiles
    def remove_useless_symbols(self):

        if self.start_symbol is None:
            print("No se ha definido símbolo inicial")
            return


        # Inicializar símbolos alcanzables con el inicial
        reachable_symbols = [self.start_symbol]
        added = False

        print (reachable_symbols)
        # Iterar hasta que no se agreguen nuevos
        while True:

            for production in self.productions:
                left, right = production.split(' → ')
                print('para la produccion: ' + production + ', el left es: ' + left + ', el right es: ' + right + ', el reachable es ' + str(reachable_symbols) + 'y el added es ' + str(added) + '\n')

                if left in reachable_symbols:
                    right_symbols = right.split()
                    for symbol in right_symbols:
                        if symbol in self.non_terminals and symbol not in reachable_symbols:
                            reachable_symbols.append(symbol)
                            added = True
            if not added:
                break

        useless_symbols = []

        for symbol in self.non_terminals:
            if symbol not in reachable_symbols:
                useless_symbols.append(symbol)

        #símbolos inútiles
        print('simbolos inutiles: ' + str(useless_symbols) + '\n')

        to_remove = []
        for production in self.productions:
            left = production.split(' → ')[0]
            if left in useless_symbols:
                to_remove.append(production)  
        
        #producciones a eliminar 
        print('producciones a eliminar: ' + str(to_remove) + '\n')

        for production in to_remove:
            self.productions.remove(production)

        
        

# Ejemplo de uso
grammar = Grammar()

grammar.add_production("S → ABD")
grammar.add_production("A → a")
grammar.add_production("B → b")
grammar.add_production("D → d")
grammar.add_production("B → ε")

# Símbolo inicial ya definido
grammar.remove_epsilon_productions()
grammar.remove_unary_productions()
grammar.remove_useless_symbols()

print("Gramática sin producciones epsilon, operaciones unarias y sin simbolos inutiles:")
print(grammar.productions)