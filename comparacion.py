import heapq
import time
import random
import math


def crearGrafo(num_nodos, edges):
    graph = {i: [] for i in range(num_nodos)}

    for u, v, peso in edges:
        graph[u].append((v, peso))

    return graph


def pasarALista(grafo):
    lista = []

    for nodo in grafo:
        for destino, costo in grafo[nodo]:
            lista.append((nodo, destino, costo))

    return lista


def generar_grafo_random(cantNodos, densidad=0.4, minimo=1, maximo=20, seed=42):
    random.seed(seed)

    conexiones = []

    for i in range(cantNodos):
        for j in range(cantNodos):

            if i != j and random.random() < densidad:
                conexiones.append((i, j, random.randint(minimo, maximo)))

    return crearGrafo(cantNodos, conexiones)


def generarCompleto(nodos, minPeso=1, maxPeso=20, semilla=99):
    random.seed(semilla)

    listaAristas = []

    for origen in range(nodos):
        for destino in range(nodos):

            if origen != destino:
                peso = random.randint(minPeso, maxPeso)
                listaAristas.append((origen, destino, peso))

    return crearGrafo(nodos, listaAristas)


def mostrarGrafo(grafo, titulo="Grafo"):
    totalAristas = sum(len(x) for x in grafo.values())

    print("\n" + "=" * 45)
    print(f" {titulo}")
    print(f" nodos -> {len(grafo)}")
    print(f" aristas -> {totalAristas}")
    print("=" * 45)


def printResultados(distancias, origen, nombre):
    print(f"\n[{nombre}] desde {origen}")

    for nodo, dist in sorted(distancias.items()):

        if dist == math.inf:
            texto = "INF"
        else:
            texto = f"{dist}"

        print(f" nodo {nodo}: {texto}")


def dijkstra(grafo, start):
    distancias = {}
    anteriores = {}

    for nodo in grafo:
        distancias[nodo] = math.inf
        anteriores[nodo] = None

    distancias[start] = 0

    cola = [(0, start)]
    vistos = set()

    while cola:

        distanciaActual, actual = heapq.heappop(cola)

        if actual in vistos:
            continue

        vistos.add(actual)

        for vecino, peso in grafo[actual]:

            nueva = distanciaActual + peso

            if nueva < distancias[vecino]:
                distancias[vecino] = nueva
                anteriores[vecino] = actual

                heapq.heappush(cola, (nueva, vecino))

    return distancias, anteriores


def reconstruirCamino(previos, inicio, final):
    camino = []

    actual = final

    while actual is not None:
        camino.append(actual)
        actual = previos[actual]

    camino.reverse()

    if camino and camino[0] == inicio:
        return camino

    return []


def bellmanFord(grafo, origen):
    cantidad = len(grafo)

    dist = {}
    padres = {}

    for nodo in grafo:
        dist[nodo] = math.inf
        padres[nodo] = None

    dist[origen] = 0

    edges = pasarALista(grafo)

    for _ in range(cantidad - 1):

        huboCambio = False

        for u, v, w in edges:

            if dist[u] != math.inf and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                padres[v] = u

                huboCambio = True

        if not huboCambio:
            break

    tieneCiclo = False

    for u, v, w in edges:

        if dist[u] != math.inf and dist[u] + w < dist[v]:
            tieneCiclo = True
            break

    return dist, padres, tieneCiclo


def medirTiempo(funcion, *args):
    inicio = time.perf_counter()

    resultado = funcion(*args)

    fin = time.perf_counter()

    return resultado, (fin - inicio) * 1000


def comparar(distA, distB):

    for nodo in distA:

        a = distA[nodo] if distA[nodo] != math.inf else 999999999
        b = distB[nodo] if distB[nodo] != math.inf else 999999999

        if abs(a - b) > 1e-9:
            return False

    return True


def ejecutarEscenario(nombre, grafo, inicio=0, negativos=False):

    print("\n" + "#" * 50)
    print(f" escenario -> {nombre}")
    print(f" origen -> {inicio}")

    mostrarGrafo(grafo, nombre)

    (distD, prevD), tiempoD = medirTiempo(dijkstra, grafo, inicio)

    (distBF, prevBF, cicloNeg), tiempoBF = medirTiempo(
        bellmanFord,
        grafo,
        inicio
    )

    printResultados(distD, inicio, "Dijkstra")
    printResultados(distBF, inicio, "BellmanFord")

    if cicloNeg:
        print("\nSe encontro ciclo negativo")

    iguales = comparar(distD, distBF)

    if iguales:
        print("\nResultados iguales")
    else:
        print("\nResultados diferentes")

        if not negativos:
            print("Algo raro paso con el grafo")

    print(f"\nTiempo Dijkstra -> {tiempoD:.4f} ms")
    print(f"Tiempo Bellman -> {tiempoBF:.4f} ms")

    if tiempoD > 0:
        veces = tiempoBF / tiempoD
        print(f"BellmanFord fue {veces:.2f}x mas lento")

    return {
        "dijkstra": tiempoD,
        "bellman": tiempoBF,
        "ok": iguales
    }


def escenarioA():
    aristas = [
        (0, 1, 4), (0, 2, 2), (1, 3, 5), (1, 4, 10),
        (2, 1, 1), (2, 3, 8), (2, 4, 10), (3, 4, 2),
        (3, 5, 6), (4, 6, 3), (5, 7, 9), (5, 8, 2),
        (6, 7, 4), (6, 9, 7), (7, 9, 1), (8, 9, 5),
        (0, 5, 15), (1, 8, 12), (3, 9, 20), (2, 7, 11)
    ]

    return crearGrafo(10, aristas)


def escenarioB():
    return generarCompleto(
        nodos=7,
        minPeso=1,
        maxPeso=30,
        semilla=7
    )


def escenarioNegativo():

    conexiones = [
        (0, 1, 4),
        (0, 2, 3),
        (1, 3, -2),
        (2, 1, -1),
        (2, 3, 7),
        (3, 4, 5),
        (1, 4, 6)
    ]

    return crearGrafo(5, conexiones)


def escenarioCiclo():
    edges = [
        (0, 1, 1),
        (1, 2, -3),
        (2, 0, 1),
        (0, 3, 5),
        (1, 3, 2)
    ]

    return crearGrafo(4, edges)


if __name__ == "__main__":

    print("\n" + "=" * 50)
    print(" InterConexion S.A")
    print(" Dijkstra vs Bellman Ford")
    print("=" * 50)

    g1 = escenarioA()

    resultadoA = ejecutarEscenario(
        "grafo pequeno",
        g1,
        inicio=0
    )

    g2 = escenarioB()

    resultadoB = ejecutarEscenario(
        "grafo denso",
        g2,
        inicio=0
    )

    print("\n" + "#" * 50)
    print(" caso pesos negativos ")
    print("#" * 50)

    gNeg = escenarioNegativo()

    mostrarGrafo(gNeg, "negativos")

    (distDij, _), td = medirTiempo(dijkstra, gNeg, 0)

    (distBell, _, ciclo), tb = medirTiempo(
        bellmanFord,
        gNeg,
        0
    )

    printResultados(distDij, 0, "Dijkstra")
    printResultados(distBell, 0, "BellmanFord")

    mismo = comparar(distDij, distBell)

    if mismo:
        print("\nCoincidieron esta vez")
    else:
        print("\nDijkstra fallo con pesos negativos")

    print("\n" + "#" * 50)
    print(" ciclo negativo ")
    print("#" * 50)

    gCiclo = escenarioCiclo()

    mostrarGrafo(gCiclo, "ciclo negativo")

    _, _, hay = bellmanFord(gCiclo, 0)

    if hay:
        print("\nBellmanFord detecto el ciclo")
    else:
        print("\nNo detecto nada")

    print("\n" + "=" * 50)
    print(" resumen ")
    print("=" * 50)

    print(
        f"A -> Dijkstra {resultadoA['dijkstra']:.4f} ms | "
        f"Bellman {resultadoA['bellman']:.4f} ms"
    )

    print(
        f"B -> Dijkstra {resultadoB['dijkstra']:.4f} ms | "
        f"Bellman {resultadoB['bellman']:.4f} ms"
    )

    print("\nConclusiones:")
    print("Dijkstra es mas rapido cuando no hay negativos")
    print("BellmanFord sirve cuando existen pesos negativos")
    print("Tambien detecta ciclos negativos")