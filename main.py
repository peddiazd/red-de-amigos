from app import crear_grafo_amigos, visualizar_grafo

if __name__ == "__main__":
    print("Ejecutando Red de Amigos AI")
    grafo = crear_grafo_amigos()
    print(f"Grafo creado con {len(grafo.nodes)} nodos y {len(grafo.edges)} aristas")
    # Para evitar mostrar gráfico en terminal, comentar la siguiente línea si es necesario
    # visualizar_grafo(grafo)