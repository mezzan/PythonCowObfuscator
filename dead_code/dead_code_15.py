def bsort(lista, a, z):

  for j in range(a, z):
    for k in range(j+1, z+1):
      if lista[k] < lista[j]:
        scambio = lista[k]
        lista[k] = lista[j]
        lista[j] = scambio

lista = sys.argv[1:]
bsort(lista, 0, len(lista)-1)
for elemento in lista:
  print(elemento)
