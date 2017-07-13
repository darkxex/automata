import collections


class Node:
    def __init__(self, name, final):
        # Seteamos los parametros basicos del nodo
        self.name = name
        self.final = final
        self.transitions = collections.OrderedDict()

    # Metodo que agrega una transicion al nodo
    def addTransition(self, symbol, destination):
        # Si el simbolo no esta en el listado de transiciones lo creamos con una lista vacia
        if not symbol in self.transitions:
            self.transitions[symbol] = []

        # Revisamos que no hayamos agregado la transicion antes y la agregamos
        if not destination in self.transitions[symbol]:
            self.transitions[symbol].append(destination)

    # Metodo que obtiene la transicion para un simbolo en especifico
    def getTransition(self, symbol):
        # Si existen transiciones para el simbolo devolvemos el listado
        if symbol in self.transitions:
            return self.transitions[symbol]
        else:
            # En caso contrario devolvemos una lista vacia
            return []

    # Metodo que borra las transiciones para un simbolo en especifico
    def removeTransition(self, symbol):
        del self.transitions[symbol]

    # Metodo que devuelve el nombre del nodo
    def getName(self):
        return self.name

    # Metodo que devuelve el listado completo de transiciones para el nodo
    def getTransitions(self):
        return self.transitions

    # Metodo que devuelve si el nodo es final
    def isFinal(self):
        return self.final

    # Metodo que setea si el nodo es final
    def setFinal(self, isFinal):
        self.final = isFinal

    # Metodo que setea si el nodo es final
    def setName(self, name):
        self.name = name

    # Metodo que reemplaza un nodo por otro en las transiciones
    def replaceTransition(self, validNode, duplicatedNode):
        # Iteramos sobre las transiciones
        for symbol, transition in self.transitions.iteritems():
            for index, nodeName in enumerate(transition):
                # Si el nodo es el duplicado lo reemplazamos por el valido
                if nodeName == duplicatedNode:
                    transition[index] = validNode

    def __repr__(self):
        return "<Node id='%s', name='%s', isFinal='%s', transitions='%s'>\n" % (hex(id(self)), self.name, self.final, self.transitions)
