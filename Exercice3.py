#Exercice 3 : Voyageur de commerce (TSP)

import math
import random

# Matrice des distances (symétrique, "-" = infini)
distances = {
    (1,2):14,(1,3):15,(1,8):17,
    (2,3):13,(2,4):14,(2,5):20,(2,8):21,
    (3,4):11,(3,5):21,(3,6):17,(3,7):9,(3,8):9,
    (4,5):11,(4,6):10,(4,7):8,(4,8):20,
    (5,6):15,(5,7):18,
    (6,7):9,
    (7,8):13
}

def dist(i,j):
    if (i,j) in distances: return distances[(i,j)]
    if (j,i) in distances: return distances[(j,i)]
    return math.inf

# Coût d'une tournée
def cout_tournee(tour):
    return sum(dist(tour[i], tour[i+1]) for i in range(len(tour)-1))

# Recuit simulé
def recuit(tour, T=100, alpha=0.9, iters=5):
    best = tour[:]
    best_cost = cout_tournee(best)
    for _ in range(iters):
        i,j = random.sample(range(1,len(tour)-1),2)
        new_tour = tour[:]
        new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
        new_cost = cout_tournee(new_tour)
        if new_cost < best_cost or random.random() < math.exp((best_cost-new_cost)/T):
            best, best_cost = new_tour, new_cost
        T *= alpha
    return best, best_cost

# Tabou simple pour TSP
def tabou_tsp(tour, max_iter=50, tenure=7):
    best = tour[:]
    best_cost = cout_tournee(best)
    tabu = []
    for _ in range(max_iter):
        voisins = []
        for i in range(1,len(tour)-1):
            for j in range(i+1,len(tour)-1):
                new_tour = tour[:]
                new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
                if new_tour not in tabu:
                    voisins.append(new_tour)
        if not voisins: break
        tour = min(voisins, key=cout_tournee)
        cost = cout_tournee(tour)
        if cost < best_cost:
            best, best_cost = tour, cost
        tabu.append(tour)
        if len(tabu) > tenure: tabu.pop(0)
    return best, best_cost

# Test
tour_init = [1,2,3,4,5,6,7,8,1]
print("Recuit simulé :", recuit(tour_init))
print("Tabou TSP :", tabou_tsp(tour_init))
