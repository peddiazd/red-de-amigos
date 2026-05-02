import networkx as nx
import matplotlib.pyplot as plt
import json
from collections import defaultdict

class RedDeAmigosAI:
    def __init__(self):
        self.G = nx.Graph()
        self.atributos = {}  # nombre -> diccionario de atributos
    
    def registrar_persona(self, nombre, comunidad, hobbies, deportes, gustos, intereses):
        nombre = nombre.strip().title()
        if nombre in self.G:
            print(f"⚠️ {nombre} ya existe.")
            return
        self.G.add_node(nombre)
        self.atributos[nombre] = {
            "comunidad": comunidad,
            "hobbies": set(hobbies),
            "deportes": set(deportes),
            "gustos": set(gustos),
            "intereses": set(intereses)
        }
        print(f"✅ {nombre} registrado correctamente.")
    
    def registrar_amistad(self, persona1, persona2):
        p1, p2 = persona1.strip().title(), persona2.strip().title()
        if p1 not in self.G or p2 not in self.G:
            print("❌ Una o ambas personas no están registradas.")
            return
        self.G.add_edge(p1, p2)
        print(f"✅ Amistad entre {p1} y {p2} registrada.")
    
    def mostrar_red(self):
        print("\n🌐 RED DE AMIGOS")
        print(f"Total personas: {self.G.number_of_nodes()}")
        print(f"Total amistades: {self.G.number_of_edges()}")
        for nodo in self.G.nodes():
            print(f"• {nodo} → Amigos: {list(self.G.neighbors(nodo))}")
    
    def visualizar(self, titulo="Red de Amigos"):
        pos = nx.spring_layout(self.G, seed=42)
        plt.figure(figsize=(12, 8))
        nx.draw(self.G, pos, with_labels=True, node_color="skyblue", 
                node_size=2500, edge_color="gray", font_size=10, font_weight="bold")
        plt.title(titulo, fontsize=16)
        plt.show()
    
    def sugerir_amistades(self, persona, top_n=5):
        persona = persona.title()
        if persona not in self.G:
            print("❌ Persona no encontrada.")
            return
        
        sugerencias = []
        intereses_usuario = set()
        for k in ["hobbies", "deportes", "gustos", "intereses"]:
            intereses_usuario.update(self.atributos[persona][k])
        
        for candidato in self.G.nodes():
            if candidato == persona or self.G.has_edge(persona, candidato):
                continue
            amigos_comun = len(list(nx.common_neighbors(self.G, persona, candidato)))
            intereses_cand = set()
            for k in ["hobbies", "deportes", "gustos", "intereses"]:
                intereses_cand.update(self.atributos[candidato][k])
            sim = len(intereses_usuario & intereses_cand) / len(intereses_usuario | intereses_cand) if intereses_usuario and intereses_cand else 0.0
            score = (amigos_comun * 3) + (sim * 10)
            sugerencias.append((candidato, round(score, 2), amigos_comun, round(sim, 2)))
        
        sugerencias.sort(key=lambda x: x[1], reverse=True)
        print(f"\n🤖 Sugerencias de amistad para {persona} (top {top_n}):")
        for cand, score, amigos_c, sim in sugerencias[:top_n]:
            print(f"• {cand} | Puntuación: {score} | Amigos en común: {amigos_c} | Similitud: {sim}")
    
    def guardar(self, archivo="data/red_amigos.json"):
        data = {"nodos": list(self.G.nodes()), "aristas": list(self.G.edges()), "atributos": self.atributos}
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"💾 Red guardada en {archivo}")

# Ejemplo de uso
if __name__ == "__main__":
    ai = RedDeAmigosAI()
    print("🚀 Red de Amigos AI lista para usar")