"""Aprendiendo customtkinter"""
import customtkinter
#mostrar el grafo con el boton y vista grafica con networkx y matplotlib
import networkx as nx
import matplotlib.pyplot as plt


customtkinter.set_appearance_mode("System") # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green") # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk() # create CTk window like you do with the Tk window
app.geometry("400x240")

def button_function():
    '''Function to be called when button is clicked'''
    nx.draw(G, pos, with_labels=True)
    plt.show()


G = nx.Graph()
# Add nodes and edges to the graph as tuples, con peso de aristas
G.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 4), (4, 5)])


pos = nx.spring_layout(G)  # positions for all nodes

# use CTkButton instead of tkinter Button
button = customtkinter.CTkButton(master=app, text="grafo", command=button_function)
button.pack(pady=20, padx=60, fill="both") # place the button on the window
button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

app.mainloop()
