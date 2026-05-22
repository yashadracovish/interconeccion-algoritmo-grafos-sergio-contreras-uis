import time
import math
import random

def crear_grafo_desde_lista(num_nodos, aristas):
    grafo = {i: [] for i in range(num_nodos)}
    for u, v, w in aristas:
        grafo[u].append((v, w))
    return grafo

def grafo_a_lista_aristas(grafo):
    aristas = []
    for u in grafo:
        for v, w in grafo[u]:
            aristas.append((u, v, w))
    return aristas

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
    print(f"\n{'='*50}")
    print(f"  {nombre}")
    print(f"  Nodos: {len(grafo)}  |  Aristas: {sum(len(v) for v in grafo.values())}")
    print(f"{'='*50}")

def imprimir_resultado(distancias, origen):
    print(f"\n  [Bellman-Ford] Distancias mínimas desde nodo {origen}:")
    for nodo, dist in sorted(distancias.items()):
        d = f"{dist:>6}" if dist != math.inf else "   INF"
        print(f"    Nodo {nodo}: {d}")

def bellman_ford(grafo, origen):
    V = len(grafo)
    distancias = {nodo: math.inf for nodo in grafo}
    distancias[origen] = 0
    predecesores = {nodo: None for nodo in grafo}

    aristas = grafo_a_lista_aristas(grafo)

    for _ in range(V - 1):
        actualizado = False
        for u, v, w in aristas:
            if distancias[u] != math.inf and distancias[u] + w < distancias[v]:
                distancias[v] = distancias[u] + w
                predecesores[v] = u
                actualizado = True
        if not actualizado:
            break

    ciclo_negativo = False
    for u, v, w in aristas:
        if distancias[u] != math.inf and distancias[u] + w < distancias[v]:
            ciclo_negativo = True
            break

    return distancias, predecesores, ciclo_negativo

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

def escenario_pesos_negativos():
    aristas = [
        (0, 1, 4), (0, 2, 3), (1, 3, -2), (2, 1, -1),
        (2, 3, 7), (3, 4, 5), (1, 4, 6),
    ]
    return crear_grafo_desde_lista(5, aristas)

def escenario_ciclo_negativo():
    aristas = [
        (0, 1, 1), (1, 2, -3), (2, 0, 1),
        (0, 3, 5), (1, 3, 2),
    ]
    return crear_grafo_desde_lista(4, aristas)

if __name__ == "__main__":
    print("\n" + "="*55)
    print("  INTERCONEXIÓN S.A. — Algoritmo de Bellman-Ford")
    print("="*55)

    grafo_a = escenario_A_grafo_pequeno()
    imprimir_grafo(grafo_a, "Escenario A — Grafo pequeño (10 nodos)")
    inicio = time.perf_counter()
    dist_a, pred_a, ciclo_a = bellman_ford(grafo_a, origen=0)
    tiempo_a = (time.perf_counter() - inicio) * 1000
    imprimir_resultado(dist_a, origen=0)
    print(f"\n  ⏱  Tiempo de ejecución: {tiempo_a:.4f} ms")
    print(f"  Ciclo negativo detectado: {'⚠️  SÍ' if ciclo_a else 'NO'}")

    camino = reconstruir_camino(pred_a, origen=0, destino=9)
    print(f"\n  Camino más corto 0 → 9: {' → '.join(map(str, camino))}")
    print(f"  Costo total: {dist_a[9]}")

    grafo_b = escenario_B_grafo_denso()
    imprimir_grafo(grafo_b, "Escenario B — Grafo denso completo (7 nodos, 42 aristas)")
    inicio = time.perf_counter()
    dist_b, pred_b, ciclo_b = bellman_ford(grafo_b, origen=0)
    tiempo_b = (time.perf_counter() - inicio) * 1000
    imprimir_resultado(dist_b, origen=0)
    print(f"\n  ⏱  Tiempo de ejecución: {tiempo_b:.4f} ms")
    print(f"  Ciclo negativo detectado: {'⚠️  SÍ' if ciclo_b else 'NO'}")

    print(f"\n{'#'*55}")
    print("  CASO ESPECIAL: Pesos negativos (subsidios en canales)")
    print(f"{'#'*55}")
    grafo_neg = escenario_pesos_negativos()
    imprimir_grafo(grafo_neg, "Grafo con pesos negativos")
    dist_neg, _, ciclo_neg = bellman_ford(grafo_neg, origen=0)
    imprimir_resultado(dist_neg, origen=0)
    print(f"  Ciclo negativo detectado: {'⚠️  SÍ' if ciclo_neg else 'NO'}")

    print(f"\n{'#'*55}")
    print("  CASO ESPECIAL: Detección de ciclo negativo")
    print(f"{'#'*55}")
    grafo_cn = escenario_ciclo_negativo()
    imprimir_grafo(grafo_cn, "Grafo con ciclo negativo")
    _, _, ciclo = bellman_ford(grafo_cn, origen=0)
    print(f"\n  Bellman-Ford detectó ciclo negativo: {'⚠️  SÍ' if ciclo else 'NO'}")

    print(f"\n{'='*55}")
    print("  RESUMEN BELLMAN-FORD")
    print(f"{'='*55}")
    print(f"  Escenario A (10 nodos, 20 aristas): {tiempo_a:.4f} ms")
    print(f"  Escenario B  (7 nodos, 42 aristas): {tiempo_b:.4f} ms")
    print("="*55)
