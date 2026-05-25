import math
import random
import time


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


def pagerank(grafo, damping=0.85, max_iter=100, tol=1e-6):
    nodos = list(grafo.keys())
    n = len(nodos)
    rank = {nodo: 1.0 / n for nodo in nodos}
    dangling = [nodo for nodo in nodos if len(grafo[nodo]) == 0]

    for _ in range(max_iter):
        rank_anterior = rank.copy()
        dangling_sum = sum(rank_anterior[nodo] for nodo in dangling)

        nuevo_rank = {}
        for nodo in nodos:
            contribucion = 0.0
            for origen in nodos:
                vecinos = [v for v, _ in grafo[origen]]
                if nodo in vecinos:
                    contribucion += rank_anterior[origen] / len(grafo[origen])
            contribucion += dangling_sum / n
            nuevo_rank[nodo] = (1 - damping) / n + damping * contribucion

        total = sum(nuevo_rank.values())
        nuevo_rank = {nodo: v / total for nodo, v in nuevo_rank.items()}

        diff = sum(abs(nuevo_rank[nd] - rank_anterior[nd]) for nd in nodos)
        rank = nuevo_rank

        if diff < tol:
            break

    return rank


def imprimir_resultado_pagerank(ranks, nombre="PageRank"):
    print(f"\n[{nombre}] Ranking de importancia de nodos:")
    ordenados = sorted(ranks.items(), key=lambda x: x[1], reverse=True)
    for pos, (nodo, r) in enumerate(ordenados, 1):
        barra = "█" * int(r * 200)
        print(f"  #{pos:>2} Nodo {nodo}: {r:.6f}  {barra}")


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
    ranks_a = pagerank(grafo_a)
    tiempo_a = (time.perf_counter() - inicio) * 1000

    imprimir_resultado_pagerank(ranks_a, "PageRank Escenario A")
    print(f"\n  Tiempo de ejecucion: {tiempo_a:.4f} ms")

    nodo_mas_importante = max(ranks_a, key=ranks_a.get)
    print(f"\n  Nodo mas importante del grafo: {nodo_mas_importante}")
    print(f"  Rank: {ranks_a[nodo_mas_importante]:.6f}")

    grafo_b = escenario_B_grafo_denso()
    imprimir_grafo(grafo_b, "Escenario B — Grafo denso completo (7 nodos, 42 aristas)")

    inicio = time.perf_counter()
    ranks_b = pagerank(grafo_b)
    tiempo_b = (time.perf_counter() - inicio) * 1000

    imprimir_resultado_pagerank(ranks_b, "PageRank Escenario B")
    print(f"\n  Tiempo de ejecucion: {tiempo_b:.4f} ms")

    print(f"\nresumen PageRank")
    print(f"  Escenario A (10 nodos, 20 aristas): {tiempo_a:.4f} ms")
    print(f"  Escenario B (7 nodos, 42 aristas):  {tiempo_b:.4f} ms")
