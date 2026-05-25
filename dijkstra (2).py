import heapq
import time
import math
import random


def crear_grafo_desde_lista(num_nodos, aristas):
    grafo = {i: [] for i in range(num_nodos)}
    for u, v, w in aristas:
        grafo[u].append((v, w))
    return grafo


def generar_grafo_completo(num_nodos, peso_min=1, peso_max=20, semilla=99):
    random.seed(semilla)
    aristas = []
    for u in range(num_nodos):
        for v in range(num_nodos):
            if u != v:
                w = random.randint(peso_min, peso_max)
                aristas.append((u, v, w))
    return crear_grafo_desde_lista(num_nodos, aristas)


def imprimir_grafo(grafo, nombre="Grafo"):
    print(f"\n{nombre}")
    print(f"Nodos: {len(grafo)} | Aristas: {sum(len(v) for v in grafo.values())}")


def imprimir_resultado(distancias, origen):
    print(f"\n[Dijkstra] Distancias minimas desde nodo {origen}:")
    for nodo, dist in sorted(distancias.items()):
        d = f"{dist:>6}" if dist != math.inf else "   INF"
        print(f"  Nodo {nodo}: {d}")


def dijkstra(grafo, origen):
    distancias = {nodo: math.inf for nodo in grafo}
    distancias[origen] = 0
    predecesores = {nodo: None for nodo in grafo}
    heap = [(0, origen)]
    visitados = set()

    while heap:
        dist_actual, u = heapq.heappop(heap)
        if u in visitados:
            continue
        visitados.add(u)
        for v, peso in grafo[u]:
            nueva_dist = dist_actual + peso
            if nueva_dist < distancias[v]:
                distancias[v] = nueva_dist
                predecesores[v] = u
                heapq.heappush(heap, (nueva_dist, v))

    return distancias, predecesores


def reconstruir_camino(predecesores, origen, destino):
    camino = []
    nodo = destino
    while nodo is not None:
        camino.append(nodo)
        nodo = predecesores[nodo]
    camino.reverse()
    if camino and camino[0] == origen:
        return camino
    return []


def escenario_A_grafo_pequeno():
    aristas = [
        (0, 1, 4), (0, 2, 2), (1, 3, 5), (1, 4, 10),
        (2, 1, 1), (2, 3, 8), (2, 4, 10), (3, 4, 2),
        (3, 5, 6), (4, 6, 3), (5, 7, 9), (5, 8, 2),
        (6, 7, 4), (6, 9, 7), (7, 9, 1), (8, 9, 5),
        (0, 5, 15), (1, 8, 12), (3, 9, 20), (2, 7, 11),
    ]
    return crear_grafo_desde_lista(10, aristas)


def escenario_B_grafo_denso():
    return generar_grafo_completo(num_nodos=7, peso_min=1, peso_max=30, semilla=7)


if __name__ == "__main__":
    grafo_a = escenario_A_grafo_pequeno()
    imprimir_grafo(grafo_a, "Escenario A — Grafo pequeño (10 nodos)")

    inicio = time.perf_counter()
    dist_a, pred_a = dijkstra(grafo_a, origen=0)
    tiempo_a = (time.perf_counter() - inicio) * 1000

    imprimir_resultado(dist_a, origen=0)
    print(f"\n  Tiempo de ejecucion: {tiempo_a:.4f} ms")

    camino = reconstruir_camino(pred_a, origen=0, destino=9)
    print(f"\n  Camino mas corto 0 -> 9: {' -> '.join(map(str, camino))}")
    print(f"  Costo total: {dist_a[9]}")

    grafo_b = escenario_B_grafo_denso()
    imprimir_grafo(grafo_b, "Escenario B — Grafo denso completo (7 nodos, 42 aristas)")

    inicio = time.perf_counter()
    dist_b, pred_b = dijkstra(grafo_b, origen=0)
    tiempo_b = (time.perf_counter() - inicio) * 1000

    imprimir_resultado(dist_b, origen=0)
    print(f"\n  Tiempo de ejecucion: {tiempo_b:.4f} ms")

    print(f"\nresumen Dijkstra")
    print(f"  Escenario A (10 nodos, 20 aristas): {tiempo_a:.4f} ms")
    print(f"  Escenario B (7 nodos, 42 aristas):  {tiempo_b:.4f} ms")
