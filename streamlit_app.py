import streamlit as st
import matplotlib.pyplot as plt
from app import RedDeAmigosAI
import networkx as nx

# Inicializar la aplicación en session_state si no existe
if 'ai' not in st.session_state:
    st.session_state.ai = RedDeAmigosAI()

ai = st.session_state.ai

st.title("🌐 Red de Amigos AI")
st.markdown("**Análisis de relaciones usando grafos e inteligencia artificial**")

# Sidebar para navegación
menu = st.sidebar.selectbox("Selecciona una opción", [
    "Inicio",
    "Registrar Persona",
    "Registrar Amistad",
    "Mostrar Red",
    "Visualizar Grafo",
    "Sugerir Amistades",
    "Guardar Red"
])

if menu == "Inicio":
    st.header("Bienvenido a Red de Amigos AI")
    st.write("Esta herramienta te permite analizar relaciones sociales mediante grafos.")
    st.write(f"**Personas registradas:** {ai.G.number_of_nodes()}")
    st.write(f"**Amistades registradas:** {ai.G.number_of_edges()}")

elif menu == "Registrar Persona":
    st.header("Registrar Nueva Persona")
    nombre = st.text_input("Nombre")
    comunidad = st.text_input("Comunidad/Grupo")
    hobbies = st.text_area("Hobbies (separados por comas)").split(',')
    deportes = st.text_area("Deportes (separados por comas)").split(',')
    gustos = st.text_area("Gustos Personales (separados por comas)").split(',')
    intereses = st.text_area("Intereses Académicos/Culturales (separados por comas)").split(',')
    
    if st.button("Registrar"):
        ai.registrar_persona(nombre, comunidad, [h.strip() for h in hobbies], 
                           [d.strip() for d in deportes], [g.strip() for g in gustos], 
                           [i.strip() for i in intereses])
        st.success(f"Persona {nombre} registrada!")

elif menu == "Registrar Amistad":
    st.header("Registrar Amistad")
    persona1 = st.selectbox("Persona 1", list(ai.G.nodes()) if ai.G.nodes() else ["Ninguna persona registrada"])
    persona2 = st.selectbox("Persona 2", list(ai.G.nodes()) if ai.G.nodes() else ["Ninguna persona registrada"])
    
    if st.button("Registrar Amistad"):
        if persona1 != persona2 and persona1 != "Ninguna persona registrada":
            ai.registrar_amistad(persona1, persona2)
            st.success(f"Amistad entre {persona1} y {persona2} registrada!")
        else:
            st.error("Selecciona dos personas diferentes.")

elif menu == "Mostrar Red":
    st.header("Mostrar Red de Amigos")
    if ai.G.number_of_nodes() == 0:
        st.write("No hay personas registradas.")
    else:
        info = f"Total personas: {ai.G.number_of_nodes()}\nTotal amistades: {ai.G.number_of_edges()}\n\n"
        for nodo in ai.G.nodes():
            amigos = list(ai.G.neighbors(nodo))
            info += f"• {nodo} → Amigos: {', '.join(amigos) if amigos else 'Ninguno'}\n"
        st.text_area("Información de la Red", info, height=300)

elif menu == "Visualizar Grafo":
    st.header("Visualizar Grafo")
    if ai.G.number_of_nodes() == 0:
        st.write("No hay personas para visualizar.")
    else:
        fig, ax = plt.subplots(figsize=(10, 6))
        pos = nx.spring_layout(ai.G, seed=42)
        nx.draw(ai.G, pos, with_labels=True, node_color="skyblue", 
                node_size=2000, edge_color="gray", font_size=10, font_weight="bold", ax=ax)
        ax.set_title("Red de Amigos", fontsize=16)
        st.pyplot(fig)

elif menu == "Sugerir Amistades":
    st.header("Sugerir Nuevas Amistades")
    persona = st.selectbox("Selecciona una persona", list(ai.G.nodes()) if ai.G.nodes() else ["Ninguna persona registrada"])
    top_n = st.slider("Número de sugerencias", 1, 10, 5)
    
    if st.button("Generar Sugerencias"):
        if persona != "Ninguna persona registrada":
            sugerencias = []
            intereses_usuario = set()
            for k in ["hobbies", "deportes", "gustos", "intereses"]:
                intereses_usuario.update(ai.atributos[persona][k])
            
            for candidato in ai.G.nodes():
                if candidato == persona or ai.G.has_edge(persona, candidato):
                    continue
                amigos_comun = len(list(nx.common_neighbors(ai.G, persona, candidato)))
                intereses_cand = set()
                for k in ["hobbies", "deportes", "gustos", "intereses"]:
                    intereses_cand.update(ai.atributos[candidato][k])
                sim = len(intereses_usuario & intereses_cand) / len(intereses_usuario | intereses_cand) if intereses_usuario and intereses_cand else 0.0
                score = (amigos_comun * 3) + (sim * 10)
                sugerencias.append((candidato, round(score, 2), amigos_comun, round(sim, 2)))
            
            sugerencias.sort(key=lambda x: x[1], reverse=True)
            st.write(f"Sugerencias de amistad para {persona} (top {top_n}):")
            for cand, score, amigos_c, sim in sugerencias[:top_n]:
                st.write(f"• {cand} | Puntuación: {score} | Amigos en común: {amigos_c} | Similitud: {sim}")
        else:
            st.error("Selecciona una persona válida.")

elif menu == "Guardar Red":
    st.header("Guardar Red")
    archivo = st.text_input("Nombre del archivo", "data/red_amigos.json")
    if st.button("Guardar"):
        ai.guardar(archivo)
        st.success(f"Red guardada en {archivo}")

st.sidebar.markdown("---")
st.sidebar.write("Proyecto académico de grafos e IA")