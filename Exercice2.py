#Exercice 2 : Affectation des containers (Recherche Taboue)

import random

# Données
couts = [[5, 3, 4],  # D1 -> M1, M2, M3
         [6, 7, 2]]  # D2 -> M1, M2, M3
capacites = [8, 9]
demandes = [4, 5, 8]

# Générer une solution initiale (remplissage greedy)
def solution_initiale():
    sol = [[0]*len(demandes) for _ in range(len(capacites))]
    reste = demandes[:]
    for j in range(len(demandes)):
        for i in range(len(capacites)):
            q = min(capacites[i]-sum(sol[i]), reste[j])
            sol[i][j] += q
            reste[j] -= q
    return sol

# Calcul du coût
def cout_total(sol):
    return sum(sol[i][j]*couts[i][j] for i in range(len(capacites)) for j in range(len(demandes)))

# Générer voisins
def voisins(sol):
    voisins = []
    for i in range(len(capacites)):
        for j in range(len(demandes)):
            if sol[i][j] > 0:
                for k in range(len(capacites)):
                    if k != i and sum(sol[k]) < capacites[k]:
                        new_sol = [row[:] for row in sol]
                        new_sol[i][j] -= 1
                        new_sol[k][j] += 1
                        voisins.append(new_sol)
    return voisins

# Recherche taboue
def tabou(max_iter=100, tenure=5):
    sol = solution_initiale()
    best = sol
    tabu = []
    for _ in range(max_iter):
        cand = voisins(sol)
        cand = [c for c in cand if c not in tabu]
        if not cand: break
        sol = min(cand, key=cout_total)
        if cout_total(sol) < cout_total(best):
            best = sol
        tabu.append(sol)
        if len(tabu) > tenure:
            tabu.pop(0)
    return best, cout_total(best)

best_sol, best_cost = tabou()
print("Solution optimale taboue :", best_sol)
print("Coût minimal :", best_cost)
