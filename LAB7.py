import re

EPSILON = "EPSILON" 

def validar_gramatica(archivo):
  """Valida formato de cada línea en el archivo de gramática"""
  
  with open(archivo) as f:
    lineas_validas = []
    for linea in f:
      if re.match(r"^[A-Z] -> [A-Z]+$", linea):
        lineas_validas.append(linea)
      else:
        print(f"Línea inválida: {linea}")
        return False

  return lineas_validas

def encontrar_anulables(gramatica):
  """Encuentra símbolos anulables en la gramática"""
  
  anulables = []
  
  for produccion in gramatica:
    if produccion.endswith(EPSILON +"\n"):
      anulables.append(produccion.split("->")[0])

  return anulables

def generar_nuevos_casos(simbolos, anulables):
  """Genera nuevas producciones reemplazando símbolos anulables"""

  nuevas_prods = []

  parte_izq = simbolos.split("->")[0]
  parte_der = simbolos.split("->")[1].split()

  for anulable in anulables:
    if anulable in parte_der:
      indice = parte_der.index(anulable)
      for i in range(len(parte_der) - indice):
        # Generar todas las sublistas a partir del índice
        sublista = parte_der[indice+i:] 
        nueva_prod = parte_izq + "->" + " ".join(sublista)
        nuevas_prods.append(nueva_prod)

  return nuevas_prods
  
def remover_epsilon(gramatica):
  """Elimina producciones epsilon y genera nuevos casos"""

  sin_epsilon = []
  anulables = encontrar_anulables(gramatica)
  
  for produccion in gramatica:
    if not produccion.endswith(EPSILON + "\n"):
      sin_epsilon.append(produccion)

  for i, prod in enumerate(sin_epsilon):
    if any(s in prod for s in anulables):
      simbolos = prod.split("->")[1]
      nuevas = generar_nuevos_casos(simbolos, anulables)  
      sin_epsilon.extend(nuevas)
      sin_epsilon.pop(i)

  return sin_epsilon

def main():
  
  gram = validar_gramatica("gramatica1.txt")
  
  if gram:
    sin_ep = remover_epsilon(gram)
    print(sin_ep)
  else:
    print("Gramática inválida")
    
main()