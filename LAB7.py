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

        # Método para agregar una producción
    def add_production(self, production):
        if validate_production(production):
            self.productions.append(production)
            left_symbol = production.split(' → ')[0]
            if left_symbol not in self.non_terminals:
                self.non_terminals.append(left_symbol)
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

        # Encontrar símbolos no terminales inalcanzables
        unreachable_symbols = set(self.non_terminals)

        for production in self.productions:
            left = production.split(' → ')[0]
            unreachable_symbols.discard(left)

        # Eliminar producciones con símbolos inalcanzables
        to_remove = []
        for production in self.productions:
            left = production.split(' → ')[0]
            if left in unreachable_symbols:
                to_remove.append(production)

        for production in to_remove:
            self.productions.remove(production)

            # Eliminar símbolos que no producen
        no_production_symbols = []
        for symbol in self.non_terminals:
            is_productive = False
            for production in self.productions:
                left, _ = production.split(' → ')
                if left == symbol:
                    is_productive = True
                    break
            if not is_productive:
                no_production_symbols.append(symbol)

        for symbol in no_production_symbols:
            self.non_terminals.remove(symbol)


# Ejemplo de uso
grammar = Grammar()
grammar.add_production("S → 0A0 | 1B1 | BB")
grammar.add_production("A → C")
grammar.add_production("B → S | A")
grammar.add_production("C → S | ε")

print("Gramática original:")
print(grammar.productions)

grammar.remove_epsilon_productions()
grammar.remove_unary_productions()
grammar.remove_useless_symbols()

print("Gramática sin producciones epsilon, operaciones unarias y sin simbolos inutiles:")
print(grammar.productions)