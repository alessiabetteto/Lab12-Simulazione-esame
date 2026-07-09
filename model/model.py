import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()  # semplice e pesato
        self._actors = []
        self._idMapActors = {}
        self._bestPath = []


    def getRatings(self):
        return DAO.getAllRatings()

    def buildGraph(self, rat1, rat2):
        self._graph.clear()
        self._actors = DAO.getAllNodes(rat1, rat2)

        for a in self._actors:
            self._idMapActors[a.id] = a

        self._graph.add_nodes_from(self._actors)

        edges = DAO.getAllEdges(rat1, rat2, self._idMapActors)
        for e in edges:
            self._graph.add_edge(e.a1, e.a2, weight=e.peso)



    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)


    def getTop5Archi(self):
        return sorted(self._graph.edges(data=True), key= lambda x: x[2]['weight'], reverse=True)[:5]

    def getConnessaInfo(self):
        # prendere tt componenti connesse
        components = list(nx.connected_components(self._graph))  # connected_components saranno una lista di nodi connessi tra di loro

        # identificare la componente connessa di dimensione maggiore, e stamparne tutti i nodi, ordinati in senso
        # decrescente secondo il grado dei nodi.

        largest = max(components, key=len)

        subgraph = self._graph.subgraph(largest).copy()  # qual è il sottografo costituito dalla componente maggiore

        orderedNodes = sorted(subgraph.nodes(), key=lambda n: self._graph.degree(n), reverse=True)  # ordiniamo secondo il grado dei nodi1

        # mi faccio una lista di tuple in cui il primo elemento è il nodo e il secondo il grado
        details = [(n, self._graph.degree(n)) for n in orderedNodes]

        return len(components), largest, details








    # PUNTO 2
    # a. Facendo click sul pulsante “Cerca percorso”, individuare il percorso più lungo dato il grafo costruito al punto  1.
    # b. Trovare un cammino semplice di lunghezza massima tale che ogni nodo successivo abbia un età
    # strettamente decrescente.

    def calcolaPercorso(self):
        self._bestPath = []
        self._maxLen = 0

        # Provo a far partire un percorso da OGNI nodo del grafo
        for nodo_iniziale in self._graph.nodes():
            parziale = [nodo_iniziale]

            # Chiamo la funzione ricorsiva per esplorare le strade
            self._ricorsione(nodo_iniziale, parziale)

        # Alla fine di tutti i cicli, restituisco il percorso vincente
        return self._bestPath

    def _ricorsione(self, nodo_corrente, parziale):
        # A. Controllo del Record

        # Se il percorso che ho in mano ora è più lungo del record precedente, aggiorno il record!
        if len(parziale) > self._maxLen:
            self._maxLen = len(parziale)
            # ATTENZIONE AL TRUCCHETTO: uso deepcopy() per fare una COPIA della lista.
            # Se facessi solo self._bestPath = parziale, Python copierebbe il riferimento
            # e al primo pop() mi svuoterebbe anche il record!
            self._bestPath = copy.deepcopy(parziale)

            # B. Trovo i vicini del nodo su cui mi trovo
        vicini = self._graph.neighbors(nodo_corrente)

        # C. Esploro i vicini validi
        for vicino in vicini:
            # FILTRO: il vicino deve essere più GIOVANE
            # (quindi data di nascita > data di nascita corrente)
            if vicino.date_of_birth > nodo_corrente.date_of_birth:  # ricordati che per le date la logica è inversa!!
                # 1. AGGIUNGO il vicino al percorso
                parziale.append(vicino)

                # 2. VADO IN PROFONDITÀ (chiamata ricorsiva)
                self._ricorsione(vicino, parziale)

                # 3. BACKTRACKING: torno indietro!
                # Rimuovo l'ultimo vicino aggiunto per provare un'altra strada
                parziale.pop()





