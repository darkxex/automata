import collections
from node import Node
import sys
import copy


class AF:
    def __init__(self):
        self.nodes = collections.OrderedDict()
        self.symbols = []
        self.first = None

    def getNodes(self):
        return self.nodes

    def getFirst(self):
        return self.first

    # Metodo que agrega un nodo al AF
    def addNode(self, node):
        # Agregamos el nodo al AF usando el nombre del nodo como llave
        self.nodes[node.getName()] = node
        # Si es el primer nodo guardamos el nombre en self.first
        if self.first is None:
            self.first = node.getName()
        # Actualizamos el listado de simbolos validos
        self.updateSymbols()

    # Metodo que actualiza el listado de simbolos validos
    def updateSymbols(self):
        # Iteramos sobre los nodos
        for nodeName, node in self.nodes.iteritems():
            # Iteramos sobre las transiciones del nodo para obtener los simbolos
            for symbol, transition in node.getTransitions().iteritems():
                # Si el simbolo aun no ha sido ingresado y no es "palabra vacia" lo agregamos a la lista
                if (not symbol in self.symbols) and symbol != "E":
                    self.symbols.append(symbol)
                    # Ordenamos la lista
                    self.symbols.sort()

    # Metodo que revisa si el AF es AFD
    def isAFD(self):
        # Iteramos sobre los nodos del AF
        for nodeName, node in self.nodes.iteritems():
            # Obtenemos las transiciones del nodo
            transitions = node.getTransitions()
            # Si tiene transiciones para menos simbolos que los validos es un AFND
            if len(transitions) < len(self.symbols):
                return False

            # Revisamos cada transicion
            for symbol, destinations in transitions.iteritems():
                # Si el simbolo tiene mas de un caracter es un AFND
                if len(str(symbol)) > 1:
                    return False
                # Si para un simbolo tiene mas de una transicion es un AFND
                if len(destinations) > 1:
                    return False

        #Si ninguna de las condiciones anteriores fue verdadera, es un AFD
        return True

    # Obtiene la clausura para un listado de nodos
    def _getClausura(self, nodes):
        # Creamos una copia de los nodos para verificar cambios al final
        newNodes = nodes[:]

        # Iteramos sobre los nodos
        for nodeName in nodes:
            # Obtenemos todas las transiciones que se pueden hacer con la palabra vacia
            newNodes += self.nodes[nodeName].getTransition("E")

        # Eliminamos los nodos repetidos
        newNodes = list(set(newNodes))

        # Verificamos si hemos agregado nodos al listado inicial
        if sorted(nodes) != sorted(newNodes):
            # Si la lista es distinta llamamos nuevamente a la funcion con los nuevos nodos
            return self._getClausura(sorted(newNodes))
        else:
            # Si la lista es igual ya tenemos todos los nodos necesarios
            return sorted(newNodes)

    # Obtiene todas las transiciones para un grupo de nodos usando cierto simbolo
    def _getTransitions(self, nodes, symbol):
        transitions = []
        # Iteramos sobre el listado de nodos
        for nodeName in nodes:
            # Buscamos todas las transiciones para el nodo usando el simbolo dado
            # y lo agregamos al listado de transiciones anteriores
            transitions += self.nodes[nodeName].getTransition(symbol)

        # Eliminamos los nodos duplicados
        transitions = list(set(transitions))

        # Devolvemos la clausura de los nodos encontrados
        return self._getClausura(transitions)

    # Determinamos si un "nuevo nodo" es final
    def _newNodeIsFinal(self, nodes):
        # Iteramos sobre los nodos, revisando si alguno de estos es final
        for nodeName in nodes:
            if self.nodes[nodeName].isFinal():
                # Si alguno es final entonces el nuevo nodo tambien lo es
                return True

        # En caso contrario no es un nodo final
        return False

    # Metodo que transforma un AFND a un AFD
    def toAFD(self):
        # Si el AF ya es un AFD devolvemos la instancia
        if self.isAFD():
            return self

        # Iniciamos un contador para los nodos que usaremos para eliminar
        # las secuencias con longitud mayor que 1
        tempNodeID = 1

        # Iteramos sobre los nodos
        for nodeName, node in self.nodes.iteritems():
            # Obtenemos las transiciones de cada nodo
            for symbol, transition in node.getTransitions().iteritems():
                # Revisamos si a secuencia tiene longitud mayor que 1
                if len(symbol) > 1:
                    # Invertimos la secuencia
                    reverseSymbol = symbol[::-1]

                    # Cada nodo que vayamos creando apuntara al ultimo creado
                    # en el primer caso es a la transicion completa del simbolo
                    lastNode = transition

                    # Seteamos una variable con el nombre del ultmo nodo temporal creado
                    # para usarlo en la transicion del nodo inicial
                    tempNodeName = None

                    # Leemos la secuencia invertida caracter a caracter, excepto por el ultimo
                    # (o sea, el primero de la secuencia) ya que ese lo usaremos en el nodo inicial
                    for i in range(0, (len(reverseSymbol) - 1)):
                        # Obtenemos el caracter de la secuencia
                        singleSymbol = reverseSymbol[i]

                        # Creamos un nodo temporal de nombre "tempID", donde ID lo obtenemos 
                        # de un contador incremental. El nodo no es final.
                        tempNodeName = "temp%s" % (tempNodeID)
                        tempNode = Node(tempNodeName, False)

                        # Si es la primera iteracion haremos la transicion desde el nodo
                        # a todos los que apuntaba la secuencia inicial, si es un una iteracion mayor
                        # apuntaremos el nodo al ultimo nodo temporal creado
                        for nextNode in lastNode:
                            tempNode.addTransition(singleSymbol, nextNode)

                        # Agregamos el nodo al AF
                        self.addNode(tempNode)

                        # Seteamos la variable lastNode con el nodo recien creado para la siguiente iteracion
                        lastNode = [tempNodeName]

                        #Aumentamos el contador del nodo intermedio
                        tempNodeID += 1

                    # Luego de desarmar la secuencia eliminamos la transicion del nodo original
                    # y creamos una transicion al ultimo nodo temporal creado
                    node.removeTransition(symbol)
                    node.addTransition(symbol[0], tempNodeName)

        # Actualizamos el listado de simbolos validos
        self.symbols = []
        self.updateSymbols()

        # Instanciamos un nuevo AF para el AFD
        newAF = AF()
        # Creamos un contados para los nombres de los nodos
        nodesCounter = 0
        # Creamos diccionarios para asociar grupos de nodos con su nombre y vice-versa
        nodeNameByTransitions = {}  # Get nodeName using the group of nodes
        transitionsByNodeName = {}  # Get group of Nodes using the nodeName
        # Creamos un directorio de nodos
        nodes = {}
        # Creamos una lista con los nuevos nodos que crearemos, como solo agregaremos
        # nodos no hay problemas en modificarlo mientras iteramos
        nodesToIterate = []

        # Asumimos que el primer nodo del AFD es el nodo inicial (Premisa)
        firstNode = self.nodes.itervalues().next()

        # Obtenemos la clausura del nodo inicial
        transitions = self._getClausura([firstNode.getName()])
        # Creamos un string con los nodos obtenidos en la clausura, porque las llaves de los
        # diccionarios no pueden ser mutables
        transitionString = '|'.join(str(v) for v in transitions)

        # Seteamos el nombre del nodo inicial
        nodeName = "Q" + str(nodesCounter)
        # Asociamos el nombre del nuevo nodo con los nodos primitivos que lo componen
        nodeNameByTransitions[transitionString] = nodeName
        transitionsByNodeName[nodeName] = transitions
        # Agregamos el nodo al listado de nodos por iterar
        nodesToIterate.append(nodeName)
        # Determinamos si el nuevo nodo sera final
        isFinal = self._newNodeIsFinal(transitions)

        # Creamos un nuevo nodo y lo agregamos al AFD
        node = Node(nodeName, isFinal)
        newAF.addNode(node)

        # Agregamos el nodo al listado de nodos usango el nombre como llave
        nodes[nodeName] = node

        # Aumentamos el contador de nodos
        nodesCounter += 1

        # Iteramos sobre los nodos que vamos creando
        for nodeToIterate in nodesToIterate:
            # Iteramos sobre los simbolos validos
            for symbol in self.symbols:
                # Obtenemos las transiciones de los nodos primitivos que componen el nuevo nodo
                # usando un simbolo especifico. Este metodo tambien devuelve la clausura.
                transitions = self._getTransitions(transitionsByNodeName[nodeToIterate], symbol)
                transitionString = '|'.join(str(v) for v in transitions)

                # Verificamos si tenemos un "nuevo nodo" compuesto por el listado
                # de "nodos primitivos" que obtuvimos
                if transitionString in nodeNameByTransitions:
                    # Si ya hemos creado el nuevo nodo solo agregamos la transicion
                    nodes[nodeToIterate].addTransition(symbol, nodeNameByTransitions[transitionString])
                else:
                    # Si no tenemos un "nodo nuevo" compuesto por el listado de nodos primitivos lo creamos
                    # Creamos el nombre del nodo usando el iterador
                    nodeName = "Q" + str(nodesCounter)
                    # Asociamos el nombre del nodo al listado de nodos primitivo y vice-versa
                    nodeNameByTransitions[transitionString] = nodeName
                    transitionsByNodeName[nodeName] = transitions
                    # Agregamos el nuevo nodo al listado de nodos por iterar
                    nodesToIterate.append(nodeName)
                    # Verificamos si el nuevo nodo va a ser final
                    isFinal = self._newNodeIsFinal(transitions)

                    # Creamos el nuevo nodo y lo agregamos al AFD
                    node = Node(nodeName, isFinal)
                    newAF.addNode(node)

                    # Agregamos el nuevo nodo al listado de nodos
                    nodes[nodeName] = node

                    # Aumentamos el contador de nuevos nodos
                    nodesCounter += 1

                    # Agregamos la transicion al nodo recien creado
                    nodes[nodeToIterate].addTransition(symbol, nodeName)

        # Actualizamos los simbolos validos en el AFD
        newAF.updateSymbols()

        # Devolvemos el AFD
        return newAF

    # Metodo que minimiza un AFD
    def minimize(self):
        # Verificamos que estamos minimizando un AFD
        if self.isAFD():
            # Creamos los grupos iniciales donde separaremos los nodos por finales y no finales
            groups = {}
            groupByName = {}

            # Iteramos sobre los nodos
            for nodeName, node in self.nodes.iteritems():

                # Si el nodo es no-final estara en el primer grupo
                groupID = 1
                # Si es final estara en el segundo
                if node.isFinal():
                    groupID = 2

                # Si aun no creamos el grupo lo creamos con lista vacia
                if not groupID in groups:
                    groups[groupID] = []

                # Asociamos el nodo a un grupo en especifico y vice-versa
                groups[groupID].append(node)
                groupByName[node.getName()] = groupID

            # Ejecutamos el metodo recursivo que minimiza el AFD
            self._minimize(groups, groupByName)
        else:
            print "No se puede minimizar un AFND, para esto debe ejecutar %s afd %s %s minimo" % (sys.argv[0], sys.argv[2], sys.argv[3])
            sys.exit()

    # Metodo que minimiza recursivamente un AFD
    def _minimize(self, groups, groupByName):
        nextGroupID = 1

        # Creamos 2 diccionarios para los nuevos grupos de esta iteracion
        newGroups = {}
        newGroupByName = {}

        # Iteramos sobre los grupos recibidos como parametros
        for gID, group in groups.iteritems():
            # Creamos un diccionario para asociar un listado de transiciones a un grupo
            # Lo reseteamos cada vez que iteramos sobre un nuevo grupo
            groupByTransitions = {}

            # Iteramos sobre los nodos en un grupo
            for node in group:
                # Obtenemos las transiciones de un grupo
                transitions = node.getTransitions()

                # Creamos 2 listas para asociar las transiciones a los grupos
                # recibidos como parametro
                sortedTransitions = []
                transitionGroups = []

                # Iteramos sobre los simbolos validos
                for symbol in self.symbols:
                    # Obtenemos la transicion asociada al simbolo
                    sortedTransitions.append(transitions[symbol][0])

                # Por cada transicion obtenida identificamos a que grupo pertenece
                for transition in sortedTransitions:
                    transitionGroups.append(groupByName[transition])

                # Creamos un string con los grupos asociados a las transiciones
                transitionString = '|'.join(str(v) for v in transitionGroups)

                # Si el strig ya existe buscamos el id del nuevo grupo
                if transitionString in groupByTransitions:
                    groupID = groupByTransitions[transitionString]
                else:
                    # En caso contrario creamos un nuevo grupo
                    groupID = nextGroupID
                    groupByTransitions[transitionString] = groupID
                    newGroups[groupID] = []

                    nextGroupID += 1

                # Asociamos el nodo al nuevo grupo y vice-versa
                newGroups[groupID].append(node)
                newGroupByName[node.getName()] = groupID

        # Si el grupo recibido como parametro es igual al obtenido en la iteracion
        # solo nos queda eliminar los duplicados
        if groups == newGroups:
            self._deleteDuplicates(newGroups)
        else:
            # En caso contrario hacemos una nueva iteracion con los nuevos grupos
            self._minimize(newGroups, newGroupByName)

    # Metodo que elimina los nodos equivalentes despues de minimizar
    def _deleteDuplicates(self, groups):
        # Iteramos sobre los grupos recibidos
        for groupId, group in groups.iteritems():
            # Si el grupo tiene mas de un nodo es un duplicado
            if len(group) > 1:
                validNode = None

                for duplicatedNode in group:
                    # Si es el primer nodo del grupo diremos que es el valido
                    if validNode is None:
                        validNode = duplicatedNode
                    else:
                        # En caso contrario lo eliminaremos del listado de nodos
                        del self.nodes[duplicatedNode.getName()]
                        # Y reemplazamos la transicion en todos los nodos del AFD
                        for nodeName, node in self.nodes.iteritems():
                            node.replaceTransition(validNode.getName(), duplicatedNode.getName())

    # Metodo que valida una secuencia para el Automata Finito
    def validateSecuence(self, secuence):
        # Para evitar tener que recorrer un arbol con mas de una rama valida
        # nos aseguramos que trabajaremos sobre un AFD
        afd = self.toAFD()
        # Llamamos al metodo de analisis recursivo entregando el nombre
        # del nodo inicial del AFD y la secuencia
        start = afd.getFirst()
        return afd.doValidateSecuence(secuence, start)

    # Metodo que analiza recursivamente si una secuencia pertenece a un AFD
    # partiendo desde un nodo dado
    def doValidateSecuence(self, secuence, start):
        # Verificamos que estamos trabajando sobre un AFD
        if self.isAFD():
            # Si el largo es 0 significa que estamos en el fin de la recusion
            # por lo que solo analizamos si el nodo "actual" es un estado final
            if len(secuence) == 0:
                return self.nodes[start].isFinal()

            # Sacamos el valor del proximo simbolo a analizar
            nextSymbol = secuence[0]

            # Buscamos la transicion del AFD para el siguiente simbolo
            transitions = self.nodes[start].getTransition(nextSymbol)

            # Si tiene transicion obtenemos el nombre del siguiente nodo
            if len(transitions) > 0:
                nextStart = transitions[0]

                # Llamamos al metodo de analisis recursivo con el resto de la palabra (sin el
                # simbolo que acabamos de analizar) y el siguiente nodo
                return self.doValidateSecuence(secuence[1:], nextStart)
        return False

    # Metodo para complementar un AFD
    def complement(self):
        # Verificamos que estamos trabajando sobre un AFD
        if self.isAFD():
            for nodeName, node in self.nodes.iteritems():
                node.setFinal(not node.isFinal())
            return True

        return False

    # Metodo para concatenar otro AF al actual
    def concat(self, af):
        currentNodes = copy.copy(self.getNodes().keys())
        extraNodes = af.getNodes()

        nodesCounter = 1

        renames = {}

        # Renombramos los nodos del nuevo AF que existen en el primero
        for nodeName, node in extraNodes.iteritems():
            if nodeName in currentNodes:
                newNodeName = "Q" + str(nodesCounter)

                while newNodeName in currentNodes:
                    nodesCounter += 1
                    newNodeName = "Q" + str(nodesCounter)

                renames[nodeName] = newNodeName
                node.setName(newNodeName)
                nodesCounter += 1

        for oldNodeName, newNodeName in renames.iteritems():
            for nodeName, node in extraNodes.iteritems():
                node.replaceTransition(newNodeName, oldNodeName)

        firstNode = af.getFirst()

        if renames.has_key(firstNode):
            firstNode = renames[firstNode]

        for nodeName, node in extraNodes.iteritems():
            self.addNode(node)

        for nodeName in currentNodes:
            node = self.nodes[nodeName]
            if node.isFinal():
                node.addTransition("E", firstNode)
                node.setFinal(False)

    def kleene(self):
        first = self.getFirst()

        # Buscamos un nombre valido para el nuevo nodo
        nodesCounter = 0
        newNodeName = "Q" + str(nodesCounter)

        while self.nodes.has_key(newNodeName):
            nodesCounter += 1
            newNodeName = "Q" + str(nodesCounter)

        # Seteamos el nuevo nodo como final y agregamos la transicion al inicial actual
        node = Node(newNodeName, True)
        node.addTransition("E", first)

        # Reiniciamos el listado de nodos (No podemos agregar una entrada al inicio en un orderecDict)
        newNodes = collections.OrderedDict()

        # Agregamos el nodo al AF usando el nombre del nodo como llave
        newNodes[node.getName()] = node
        self.first = node.getName()

        # Agregamos el resto de los elementos al nuevo listado de nodos
        for nodeName, node in self.nodes.iteritems():
            newNodes[nodeName] = node

            # Si es final agregamos la transicion vacia al nodo inicial
            if node.isFinal():
                node.addTransition("E", first)

        # Reemplazamos el listado de nodos
        self.nodes = newNodes

    # Metodo que se asegura que el primero nodo es final, para aceptar la palabra vacia
    def aceptarVacia(self):
        # Verificamos que el AFD no acepta una palabra vacia
        if not self.validateSecuence(""):
            self.nodes[self.getFirst()].setFinal(True)

    # Metodo que evita que el AFD acepte la palabra vacia
    def noAceptarVacia(self):
        # Verificamos que el AFD acepta una palabra vacia
        if self.validateSecuence(""):
            # Transiciones que tenemos que agregar al nuevo nodo inicial
            transitions = self.nodes[self.getFirst()].getTransitions()

            # Buscamos un nombre valido para el nuevo nodo
            nodesCounter = 0
            newNodeName = "Q" + str(nodesCounter)

            while self.nodes.has_key(newNodeName):
                nodesCounter += 1
                newNodeName = "Q" + str(nodesCounter)

            # Seteamos el nuevo nodo como final y agregamos la transicion al inicial actual
            node = Node(newNodeName, True)
            for symbol, transitionsToAdd in transitions.iteritems():
                for destination in transitionsToAdd:
                    node.addTransition(symbol, destination)

            # Reiniciamos el listado de nodos (No podemos agregar una entrada al inicio en un orderecDict)
            newNodes = collections.OrderedDict()

            # Agregamos el nodo al AF usando el nombre del nodo como llave
            newNodes[node.getName()] = node
            self.first = node.getName()

            # Agregamos el resto de los elementos al nuevo listado de nodos
            for nodeName, node in self.nodes.iteritems():
                newNodes[nodeName] = node

            # Reemplazamos el listado de nodos
            self.nodes = newNodes

    # Metodo que une el AF a otro
    def union(self, af):
        currentNodes = copy.copy(self.getNodes().keys())
        extraNodes = af.getNodes()

        nodesCounter = 1

        renames = {}

        # Renombramos los nodos del nuevo AF que existen en el primero
        for nodeName, node in extraNodes.iteritems():
            if nodeName in currentNodes:
                newNodeName = "Q" + str(nodesCounter)

                while newNodeName in currentNodes:
                    nodesCounter += 1
                    newNodeName = "Q" + str(nodesCounter)

                renames[nodeName] = newNodeName
                node.setName(newNodeName)
                nodesCounter += 1

        for oldNodeName, newNodeName in renames.iteritems():
            for nodeName, node in extraNodes.iteritems():
                node.replaceTransition(newNodeName, oldNodeName)

        firstNodeAF = af.getFirst()

        if renames.has_key(firstNodeAF):
            firstNodeAF = renames[firstNodeAF]

        # Buscamos un nombre valido para el nuevo nodo
        newNodeName = "Q" + str(nodesCounter)

        while self.nodes.has_key(newNodeName) or renames.has_key(newNodeName):
            nodesCounter += 1
            newNodeName = "Q" + str(nodesCounter)

        # Seteamos el nuevo nodo como no-final y agregamos la transicion al inicial de cada AF
        node = Node(newNodeName, False)
        node.addTransition("E", self.getFirst())
        node.addTransition("E", firstNodeAF)

        # Reiniciamos el listado de nodos (No podemos agregar una entrada al inicio en un orderecDict)
        newNodes = collections.OrderedDict()

        # Agregamos el nodo al AF usando el nombre del nodo como llave
        newNodes[node.getName()] = node
        self.first = node.getName()

        # Agregamos los elementos del AF actual al nuevo listado de nodos
        for nodeName, node in self.nodes.iteritems():
            newNodes[nodeName] = node

        # Agregamos los elementos del nodo que se une al nuevo listado de nodos
        for nodeName, node in af.nodes.iteritems():
            # Tenemos que reescribir la variable, cuando cambiamos el nombre no cambiamos
            # el indice en el listado de nodos
            nodeName = node.getName()
            newNodes[nodeName] = node

        # Reemplazamos el listado de nodos
        self.nodes = newNodes

        # Actualizamos el listado de simbolos validos
        self.updateSymbols()

    def __repr__(self):
        return "<AF symbols: '%s', nodes: '\n%s'>" % (self.symbols, self.nodes)
