"""
Problème d'ordonnancement de la maintenance de centrales électriques
Algorithme génétique : sélection par loterie + mutation par inversion
"""
import random

# ---------- Données du problème ----------
CAPACITE = [20, 15, 35, 40, 15, 15, 10]       # MW de chaque unité
NB_INTERVALLES = [2, 2, 1, 1, 1, 1, 1]        # intervalles de maintenance requis
DEMANDE = [80, 90, 65, 70]                    # MW demandés par intervalle
CAPACITE_TOTALE = sum(CAPACITE)               # 150 MW

N_UNITES = len(CAPACITE)
N_INTERV = len(DEMANDE)

# ---------- Paramètres de l'AG ----------
TAILLE_POP = 50
GENERATIONS = 100
P_CROISEMENT = 0.8
P_MUTATION = 0.1


# ---------- Encodage ----------
# Un gène = 4 bits (un bit par intervalle, 1 = en maintenance)
# Unités 1 et 2 : 1100, 0110, 0011
# Unités 3 à 7  : 1000, 0100, 0010, 0001
def genes_possibles(k):
    liste = []
    for debut in range(N_INTERV - k + 1):
        gene = [0] * N_INTERV
        for i in range(debut, debut + k):
            gene[i] = 1
        liste.append(gene)
    return liste


GENES = [genes_possibles(k) for k in NB_INTERVALLES]


def creer_chromosome():
    return [random.choice(GENES[u])[:] for u in range(N_UNITES)]


# ---------- Fonction objective ----------
# Réserve(t) = Capacité totale - Puissance perdue(t) - Demande(t)
# Performance = plus petite réserve (0 si une réserve est négative)
def fitness(chromosome):
    reserves = []
    for t in range(N_INTERV):
        perdue = sum(CAPACITE[u] * chromosome[u][t] for u in range(N_UNITES))
        reserves.append(CAPACITE_TOTALE - perdue - DEMANDE[t])
    return max(0, min(reserves))


# ---------- Sélection par loterie (roulette) ----------
def selection_loterie(population, performances):
    total = sum(performances)
    if total == 0:
        return random.choice(population)
    tirage = random.uniform(0, total)
    cumul = 0
    for individu, perf in zip(population, performances):
        cumul += perf
        if cumul >= tirage:
            return individu
    return population[-1]


# ---------- Croisement (à 1 point, entre deux gènes) ----------
def croisement(p1, p2):
    if random.random() < P_CROISEMENT:
        point = random.randint(1, N_UNITES - 1)
        return p1[:point] + p2[point:], p2[:point] + p1[point:]
    return p1[:], p2[:]


# ---------- Mutation par inversion ----------
# On inverse l'ordre des 4 bits d'un gène (ex: 1100 -> 0011, 1000 -> 0001)
def mutation_inversion(chromosome):
    nouveau = [g[:] for g in chromosome]
    for u in range(N_UNITES):
        if random.random() < P_MUTATION:
            nouveau[u].reverse()
    return nouveau


# ---------- Algorithme génétique ----------
def algorithme_genetique():
    population = [creer_chromosome() for _ in range(TAILLE_POP)]
    meilleur = max(population, key=fitness)

    for _ in range(GENERATIONS):
        performances = [fitness(c) for c in population]

        courant = population[performances.index(max(performances))]
        if fitness(courant) > fitness(meilleur):
            meilleur = courant

        nouvelle_pop = []
        while len(nouvelle_pop) < TAILLE_POP:
            p1 = selection_loterie(population, performances)
            p2 = selection_loterie(population, performances)
            e1, e2 = croisement(p1, p2)
            nouvelle_pop.append(mutation_inversion(e1))
            nouvelle_pop.append(mutation_inversion(e2))
        population = nouvelle_pop[:TAILLE_POP]

    return meilleur


if __name__ == "__main__":
    solution = algorithme_genetique()
    print("Meilleure cédule :", " ".join("".join(map(str, g)) for g in solution))
    print("Performance (réserve minimale) :", fitness(solution), "MW")
