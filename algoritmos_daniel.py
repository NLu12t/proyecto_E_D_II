import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

class Grafo:
    def __init__(self):
        self.grafo = {}
        self.pesos = {}

    def agregar_vertice(self, vertice):
        if vertice not in self.grafo:
            self.grafo[vertice] = []

    def agregar_arista(self, vertice1, vertice2, peso=None):
        if vertice1 in self.grafo and vertice2 in self.grafo:
            self.grafo[vertice1].append(vertice2)
            self.grafo[vertice2].append(vertice1)
            if peso is not None:
                self.pesos[(vertice1, vertice2)] = peso
                self.pesos[(vertice2, vertice1)] = peso

    def bfs(self, inicio):
        visitados = set()
        cola = deque([inicio])
        visitados.add(inicio)
        arbol_bfs = Grafo()
        arbol_bfs.agregar_vertice(inicio)
        padres = {inicio: None}
        orden = {inicio: 0}

        while cola:
            vertice = cola.popleft()
            for vecino in self.grafo[vertice]:
                if vecino not in visitados:
                    visitados.add(vecino)
                    cola.append(vecino)
                    padres[vecino] = vertice
                    orden[vecino] = orden[vertice] + 1
                    arbol_bfs.agregar_vertice(vecino)
                    arbol_bfs.agregar_arista(vertice, vecino)

        # Visualizar el árbol BFS
        self.dibujar_arbol(arbol_bfs, f"BFS desde {inicio}")
        return arbol_bfs

    def dfs(self, inicio):
        visitados = set()
        pila = [inicio]
        visitados.add(inicio)
        arbol_dfs = Grafo()
        arbol_dfs.agregar_vertice(inicio)
        padres = {inicio: None}

        while pila:
            vertice = pila.pop()
            for vecino in self.grafo[vertice]:
                if vecino not in visitados:
                    visitados.add(vecino)
                    pila.append(vecino)
                    padres[vecino] = vertice
                    arbol_dfs.agregar_vertice(vecino)
                    arbol_dfs.agregar_arista(vertice, vecino)

        # Visualizar el árbol DFS
        self.dibujar_arbol(arbol_dfs, f"DFS desde {inicio}")
        return arbol_dfs

    def kruskal(self):
        arbol = Grafo()
        for vertice in self.grafo:
            arbol.agregar_vertice(vertice)

        # Ordenar aristas por peso
        aristas = []
        for (u, v), peso in self.pesos.items():
            if u < v:  # Evitar duplicados
                aristas.append((peso, u, v))
        aristas.sort()

        # Algoritmo de Kruskal
        padre = {vertice: vertice for vertice in self.grafo}

        def encontrar(vertice):
            if padre[vertice] != vertice:
                padre[vertice] = encontrar(padre[vertice])
            return padre[vertice]

        for peso, u, v in aristas:
            raiz_u = encontrar(u)
            raiz_v = encontrar(v)
            if raiz_u != raiz_v:
                padre[raiz_v] = raiz_u
                arbol.agregar_arista(u, v, peso)

        # Visualizar el árbol de Kruskal
        self.dibujar_arbol_con_pesos(arbol, "Árbol generador mínimo (Kruskal)")
        return arbol

    def prim(self, inicio):
        arbol = Grafo()
        arbol.agregar_vertice(inicio)
        aristas = []
        for vecino in self.grafo[inicio]:
            peso = self.pesos[(inicio, vecino)]
            aristas.append((peso, inicio, vecino))
        aristas.sort()

        while len(arbol.grafo) < len(self.grafo):
            peso, u, v = aristas.pop(0)
            if v not in arbol.grafo:
                arbol.agregar_vertice(v)
                arbol.agregar_arista(u, v, peso)
                for vecino in self.grafo[v]:
                    if vecino not in arbol.grafo:
                        peso_nuevo = self.pesos[(v, vecino)]
                        aristas.append((peso_nuevo, v, vecino))
                aristas.sort()

        # Visualizar el árbol de Prim
        self.dibujar_arbol_con_pesos(arbol, f"Árbol generador mínimo (Prim desde {inicio})")
        return arbol

    def dibujar_arbol(self, arbol, titulo):
        G = nx.Graph()
        for vertice in arbol.grafo:
            G.add_node(vertice)
            for vecino in arbol.grafo[vertice]:
                if vertice < vecino:  # Evitar duplicados
                    G.add_edge(vertice, vecino)

        pos = nx.spring_layout(G)
        plt.figure()
        plt.title(titulo)
        nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=700, font_size=10, font_weight='bold')
        plt.show()

    def dibujar_arbol_con_pesos(self, arbol, titulo):
        G = nx.Graph()
        for vertice in arbol.grafo:
            G.add_node(vertice)
            for vecino in arbol.grafo[vertice]:
                if vertice < vecino:  # Evitar duplicados
                    peso = arbol.pesos.get((vertice, vecino), 1)
                    G.add_edge(vertice, vecino, weight=peso)

        pos = nx.spring_layout(G)
        plt.figure()
        plt.title(titulo)
        nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=700, font_size=10, font_weight='bold')
        etiquetas = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=etiquetas)
        plt.show()

def main():
    grafo = Grafo()
    # Ejemplo de grafo (modificar según necesidad)
    vertices = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P']
    for v in vertices:
        grafo.agregar_vertice(v)

    aristas = [
            ("N", "M", 1),
            ("F", "G", 1),
            ("D", "E", 1),
            ("E", "I", 2),
            ("I", "N", 2),
            ("I", "D", 2),
            ("K", "P", 2),
            ("G", "L", 2),
            ("E", "F", 3),
            ("F", "I", 3),
            ("D", "H", 3),
            ("B", "C", 3),
            ("A", "E", 4),
            ("K", "L", 4),
            ("B", "F", 4),
            ("A", "D", 5),
            ("C", "G", 6),
            ("E", "B", 7),
            ("A", "B", 8),
            ("G", "K", 9),
            ("F", "C", 11),
            ("H", "M", 11),
            ("I", "H", 13),
            ("M", "I", 16),
            ("I", "K", 16),
            ("L", "P", 16),
            ("P", "I", 20),
            ("F", "K", 20),
            ("P", "N", 22)
    ]
    for u, v, peso in aristas:
        grafo.agregar_arista(u, v, peso)

    while True:
        print("\nMenú de opciones:")
        print("a) Recorrido en anchura (BFS)")
        print("b) Recorrido en profundidad (DFS)")
        print("c) Árbol generador mínimo (Kruskal)")
        print("d) Árbol generador mínimo (Prim)")
        print("e) Salir")
        opcion = input("Seleccione una opción: ").lower()

        if opcion == 'a':
            inicio = input("Ingrese el vértice inicial (ej. A): ").upper()
            grafo.bfs(inicio)
        elif opcion == 'b':
            inicio = input("Ingrese el vértice inicial (ej. A): ").upper()
            grafo.dfs(inicio)
        elif opcion == 'c':
            grafo.kruskal()
        elif opcion == 'd':
            inicio = input("Ingrese el vértice inicial (ej. A): ").upper()
            grafo.prim(inicio)
        elif opcion == 'e':
            break
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    main()