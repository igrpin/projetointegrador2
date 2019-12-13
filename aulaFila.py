# Verifica se a lista tem elementos

def temGente(fila):
    if (len(fila) <= 0):
        return False
    else:
        return True

# Inserir elemento na fila

def inserir(fila, valor):
    aux = {len(fila):valor}
    fila.update(aux)

# Retorna quantidade de elementos na fila

def qtdeElem(fila):
    return len(fila)
    print('Fila vazia')

# Retorna o primeiro elemento da fila
xp = 76
def firstElement(fila):
    return fila[0]

# Retorna o último elemento da fila

def lastElement(fila):
    return fila[len(fila)-1]

# Move a fila removendo o último elemento

def moveFila(fila):
    # fila.pop(0) # del fila[x]
    if (temGente(fila)):
        for i in range(len(fila)-1):
            fila[i] = fila[i+1]
        del fila[len(fila) - 1]
        return fila
    else:
        return False
        
fila = {0:'Elemento1',1:'Elemento2',2:'Elemento3'}
