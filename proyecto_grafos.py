''' Visualizador de grafos y algoritmos con CustomTkinter y NetworkX.'''

import customtkinter as ctk
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#import pandas as pd
from collections import deque

# Configuración de la ventana principal
class GraphApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Visualizador de Grafos y Algoritmos")
        self.geometry("900x600")
        self.minsize(600, 400)  # Tamaño mínimo de ventana

        # Crear el grafo inicial
        self.G = self.create_graph()

        # Crear menú de opciones
        self.menu = ctk.CTkOptionMenu(self, values=["Original", "BFS", "DFS", "Kruskal", "Prim"], command=self.on_algorithm_select)
        self.menu.pack(pady=10)

        # Crear figura de matplotlib
        self.fig, self.ax = plt.subplots(figsize=(7,5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

        # Actualizar gráfico al redimensionar ventana
        self._resize_binding = self.bind("<Configure>", self.on_resize)

        # Mostrar el grafo original
        self.draw_graph(self.G)

        # Manejar cierre de ventana para evitar errores de comandos inválidos
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_graph(self):
        # Crear un grafo con pesos en las aristas
        G = nx.Graph()
        edges = [
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
        for u, v, w in edges:
            G.add_edge(u, v, weight=w)
        return G

    def draw_graph(self, G, highlight_edges=None, only_highlight=False):
        """
        Dibuja el grafo en el canvas de matplotlib.
        Si only_highlight=True, solo dibuja el subgrafo resultado.
        Los nodos se acomodan en grupos para evitar cruces y mejorar la visualización.
        """
        self.ax.clear()
        # Layout manual optimizado por grupos
        pos = {
            # Diagonal de A a C
            "A": (0.1, 0.1),
            "B": (0.2, 0.2),
            "C": (0.3, 0.3),
            # Más a la derecha D a G
            "D": (0.5, 0.2),
            "E": (0.6, 0.3),
            "F": (0.7, 0.4),
            "G": (0.8, 0.5),
            # Más a la derecha H a L (sin J)
            "H": (1.0, 0.1),
            "I": (1.1, 0.2),
            "K": (1.2, 0.3),
            "L": (1.3, 0.4),
            # Más a la derecha M a P
            "M": (1.5, 0.1),
            "N": (1.6, 0.2),
            "P": (1.7, 0.3)
        }

        # Si solo se quiere mostrar el subgrafo resultado
        if only_highlight and highlight_edges:
            subG = nx.Graph()
            subG.add_edges_from(highlight_edges)
            for u, v in highlight_edges:
                if G.has_edge(u, v):
                    subG[u][v]['weight'] = G[u][v]['weight']
            nx.draw_networkx_nodes(subG, pos, ax=self.ax, node_color='#1f77b4', node_size=800)
            nx.draw_networkx_edges(subG, pos, ax=self.ax, edgelist=highlight_edges, width=4, edge_color='#ff5733')
            nx.draw_networkx_labels(subG, pos, ax=self.ax, font_size=13, font_color='black')
            edge_labels = nx.get_edge_attributes(subG, 'weight')
            nx.draw_networkx_edge_labels(subG, pos, edge_labels=edge_labels, ax=self.ax, font_color='green')
        else:
            # Grafo completo con resaltado
            highlight_nodes = set()
            if highlight_edges:
                for u, v in highlight_edges:
                    highlight_nodes.add(u)
                    highlight_nodes.add(v)
            normal_nodes = [n for n in G.nodes if n not in highlight_nodes]
            if normal_nodes:
                nx.draw_networkx_nodes(G, pos, ax=self.ax, nodelist=normal_nodes, node_color='#cccccc', node_size=600, alpha=0.5)
            if highlight_nodes:
                nx.draw_networkx_nodes(G, pos, ax=self.ax, nodelist=list(highlight_nodes), node_color='#1f77b4', node_size=800)
            normal_edges = [e for e in G.edges if not highlight_edges or e not in highlight_edges and (e[1], e[0]) not in highlight_edges]
            if normal_edges:
                nx.draw_networkx_edges(G, pos, ax=self.ax, edgelist=normal_edges, width=2, edge_color='#bbbbbb', alpha=0.5)
            if highlight_edges:
                nx.draw_networkx_edges(G, pos, ax=self.ax, edgelist=highlight_edges, width=4, edge_color='#ff5733')
            nx.draw_networkx_labels(G, pos, ax=self.ax, font_size=13, font_color='black')
            edge_labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=self.ax, font_color='green')
        self.fig.tight_layout()
        self.canvas.draw()

    def on_resize(self, event):
        """Actualiza el gráfico al redimensionar la ventana, evitando errores si el canvas fue destruido."""
        try:
            # Verifica que el canvas siga existiendo antes de actualizar
            if hasattr(self, 'canvas_widget') and self.canvas_widget.winfo_exists():
                self.fig.set_size_inches(max(self.winfo_width()/120, 4), max(self.winfo_height()/120, 3))
                self.draw_graph(self.G)
        except Exception as e:
            # Ignora errores si el canvas ya no existe
            pass

    def on_close(self):
        """Desvincula eventos y destruye la ventana correctamente."""
        try:
            if hasattr(self, '_resize_binding'):
                self.unbind("<Configure>", self._resize_binding)
        except Exception:
            pass
        self.destroy()

    def on_algorithm_select(self, choice):
        """Maneja la selección del menú y ejecuta el algoritmo correspondiente."""
        # Vértice de inicio para BFS/DFS/Prim
        start_vertex = "A"
        if choice == "Original":
            self.draw_graph(self.G)
        elif choice == "BFS":
            if start_vertex in self.G:
                tree_edges = self.bfs_tree(self.G, start_vertex)
                self.draw_graph(self.G, highlight_edges=tree_edges, only_highlight=True)
            else:
                self.show_error(f"El vértice '{start_vertex}' no existe en el grafo.")
        elif choice == "DFS":
            if start_vertex in self.G:
                tree_edges = self.dfs_tree(self.G, start_vertex)
                self.draw_graph(self.G, highlight_edges=tree_edges, only_highlight=True)
            else:
                self.show_error(f"El vértice '{start_vertex}' no existe en el grafo.")
        elif choice == "Kruskal":
            mst_edges = list(nx.minimum_spanning_edges(self.G, algorithm="kruskal", data=False))
            self.draw_graph(self.G, highlight_edges=mst_edges, only_highlight=True)
        elif choice == "Prim":
            if start_vertex in self.G:
                mst_edges = list(nx.minimum_spanning_edges(self.G, algorithm="prim", data=False))
                self.draw_graph(self.G, highlight_edges=mst_edges, only_highlight=True)
            else:
                self.show_error(f"El vértice '{start_vertex}' no existe en el grafo.")

    def show_error(self, message):
        """Muestra un mensaje de error en una ventana emergente."""
        error_win = ctk.CTkToplevel(self)
        error_win.title("Error")
        error_win.geometry("300x100")
        label = ctk.CTkLabel(error_win, text=message)
        label.pack(pady=20)
        btn = ctk.CTkButton(error_win, text="Cerrar", command=error_win.destroy)
        btn.pack(pady=5)

    def bfs_tree(self, G, start):
        # Algoritmo BFS para obtener el árbol de expansión
        visited = set([start])
        queue = deque([start])
        tree_edges = []
        while queue:
            node = queue.popleft()
            for neighbor in G.neighbors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    tree_edges.append((node, neighbor))
        return tree_edges

    def dfs_tree(self, G, start):
        # Algoritmo DFS para obtener el árbol de expansión
        visited = set()
        tree_edges = []
        def dfs(u):
            visited.add(u)
            for v in G.neighbors(u):
                if v not in visited:
                    tree_edges.append((u, v))
                    dfs(v)
        dfs(start)
        return tree_edges

if __name__ == "__main__":
    app = GraphApp()
    app.mainloop()
