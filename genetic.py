"""
Algorithme Génétique pour le problème de découpe (Cutting Stock Problem)
"""

import random
import time
import tracemalloc
from typing import List, Dict, Tuple
import copy

BAR_LENGTH = 10


class Individual:
    """Représente un individu (solution) dans la population"""
    
    def __init__(self, permutation: List[int], pieces: List[int]):
        """
        Args:
            permutation: Ordre de placement des pièces (indices)
            pieces: Liste des tailles de pièces originales
        """
        self.permutation = permutation
        self.pieces = pieces
        self.fitness = 0
        self.num_bars = 0
        self.total_waste = 0
        self.bars = []
        self._evaluate()
    
    def _evaluate(self):
        """Évalue la fitness de cet individu"""
        # Appliquer First Fit selon l'ordre de la permutation
        bars = []
        
        for idx in self.permutation:
            piece_size = self.pieces[idx]
            
            # Chercher la première barre où la pièce entre
            placed = False
            for bar in bars:
                if bar['remaining'] >= piece_size:
                    bar['pieces'].append(piece_size)
                    bar['remaining'] -= piece_size
                    placed = True
                    break
            
            # Si aucune barre ne convient, créer une nouvelle
            if not placed:
                bars.append({
                    'pieces': [piece_size],
                    'remaining': BAR_LENGTH - piece_size
                })
        
        self.bars = bars
        self.num_bars = len(bars)
        self.total_waste = sum(bar['remaining'] for bar in bars)
        
        # Fitness: minimiser le nombre de barres (priorité) et les pertes
        # Plus la fitness est petite, meilleure est la solution
        self.fitness = self.num_bars + (self.total_waste / (BAR_LENGTH * self.num_bars) if self.num_bars > 0 else 0)
    
    def __lt__(self, other):
        """Comparaison pour le tri (plus petite fitness = meilleure)"""
        return self.fitness < other.fitness


def create_initial_population(pieces: List[int], population_size: int) -> List[Individual]:
    """
    Crée la population initiale
    
    Args:
        pieces: Liste des tailles de pièces
        population_size: Taille de la population
        
    Returns:
        Liste d'individus
    """
    population = []
    n = len(pieces)
    
    # Premier individu: ordre décroissant (solution gloutonne)
    sorted_indices = sorted(range(n), key=lambda i: pieces[i], reverse=True)
    population.append(Individual(sorted_indices, pieces))
    
    # Reste de la population: permutations aléatoires
    for _ in range(population_size - 1):
        permutation = list(range(n))
        random.shuffle(permutation)
        population.append(Individual(permutation, pieces))
    
    return population


def selection_tournament(population: List[Individual], tournament_size: int = 3) -> Individual:
    """
    Sélection par tournoi
    
    Args:
        population: Population actuelle
        tournament_size: Nombre d'individus dans le tournoi
        
    Returns:
        Individu sélectionné
    """
    tournament = random.sample(population, tournament_size)
    return min(tournament, key=lambda ind: ind.fitness)


def crossover_order(parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
    """
    Croisement par ordre (Order Crossover - OX)
    
    Args:
        parent1: Premier parent
        parent2: Deuxième parent
        
    Returns:
        Deux enfants
    """
    n = len(parent1.permutation)
    
    # Choisir deux points de croisement
    point1 = random.randint(0, n - 2)
    point2 = random.randint(point1 + 1, n)
    
    # Créer les enfants
    child1_perm = [-1] * n
    child2_perm = [-1] * n
    
    # Copier la section entre les points
    child1_perm[point1:point2] = parent1.permutation[point1:point2]
    child2_perm[point1:point2] = parent2.permutation[point1:point2]
    
    # Remplir le reste dans l'ordre de l'autre parent
    def fill_child(child_perm, parent_perm):
        child_set = set(child_perm[point1:point2])
        idx = point2
        for gene in parent_perm[point2:] + parent_perm[:point2]:
            if gene not in child_set:
                if idx >= n:
                    idx = 0
                child_perm[idx] = gene
                idx += 1
    
    fill_child(child1_perm, parent2.permutation)
    fill_child(child2_perm, parent1.permutation)
    
    child1 = Individual(child1_perm, parent1.pieces)
    child2 = Individual(child2_perm, parent2.pieces)
    
    return child1, child2


def mutation_swap(individual: Individual, mutation_rate: float) -> Individual:
    """
    Mutation par échange de deux gènes
    
    Args:
        individual: Individu à muter
        mutation_rate: Probabilité de mutation
        
    Returns:
        Individu muté
    """
    if random.random() < mutation_rate:
        permutation = individual.permutation[:]
        n = len(permutation)
        
        # Échanger deux positions aléatoires
        i, j = random.sample(range(n), 2)
        permutation[i], permutation[j] = permutation[j], permutation[i]
        
        return Individual(permutation, individual.pieces)
    
    return individual


def genetic_algorithm(
    pieces: List[int],
    population_size: int = 100,
    num_generations: int = 100,
    mutation_rate: float = 0.1,
    crossover_rate: float = 0.8,
    elitism_size: int = 2,
    verbose: bool = False
) -> Tuple[Individual, Dict, List[float]]:
    """
    Algorithme Génétique pour le problème de découpe
    
    Args:
        pieces: Liste des tailles de pièces
        population_size: Taille de la population
        num_generations: Nombre de générations
        mutation_rate: Taux de mutation
        crossover_rate: Taux de croisement
        elitism_size: Nombre d'élites à préserver
        verbose: Afficher les informations de progression
        
    Returns:
        - Meilleur individu trouvé
        - Dictionnaire avec les métriques
        - Historique de convergence (meilleure fitness par génération)
    """
    # Démarrer les mesures
    tracemalloc.start()
    start_time = time.time()
    
    # Créer la population initiale
    population = create_initial_population(pieces, population_size)
    
    # Historique de convergence
    convergence_history = []
    
    # Évolution
    for generation in range(num_generations):
        # Trier la population par fitness
        population.sort()
        
        # Enregistrer la meilleure fitness
        best_fitness = population[0].fitness
        convergence_history.append(best_fitness)
        
        if verbose and generation % 10 == 0:
            print(f"Génération {generation}: Meilleure fitness = {best_fitness:.4f} (barres: {population[0].num_bars})")
        
        # Nouvelle génération
        new_population = []
        
        # Élitisme: garder les meilleurs individus
        new_population.extend(population[:elitism_size])
        
        # Créer le reste de la nouvelle population
        while len(new_population) < population_size:
            # Sélection
            parent1 = selection_tournament(population)
            parent2 = selection_tournament(population)
            
            # Croisement
            if random.random() < crossover_rate:
                child1, child2 = crossover_order(parent1, parent2)
            else:
                child1 = Individual(parent1.permutation[:], parent1.pieces)
                child2 = Individual(parent2.permutation[:], parent2.pieces)
            
            # Mutation
            child1 = mutation_swap(child1, mutation_rate)
            child2 = mutation_swap(child2, mutation_rate)
            
            new_population.append(child1)
            if len(new_population) < population_size:
                new_population.append(child2)
        
        population = new_population
    
    # Trouver la meilleure solution finale
    population.sort()
    best_individual = population[0]
    
    # Fin des mesures
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    # Métriques
    execution_time = end_time - start_time
    memory_used = peak / 1024  # en KB
    
    metrics = {
        'num_bars': best_individual.num_bars,
        'total_waste': best_individual.total_waste,
        'fitness': best_individual.fitness,
        'execution_time': execution_time,
        'memory_kb': memory_used,
        'algorithm': 'Genetic',
        'population_size': population_size,
        'num_generations': num_generations,
        'mutation_rate': mutation_rate,
        'crossover_rate': crossover_rate
    }
    
    return best_individual, metrics, convergence_history


def solve(pieces: List[int], **kwargs) -> Dict:
    """
    Interface pour résoudre le problème avec l'algorithme génétique
    
    Args:
        pieces: Liste des tailles de pièces
        **kwargs: Paramètres de l'algorithme génétique
        
    Returns:
        Dictionnaire avec les métriques de performance
    """
    _, metrics, _ = genetic_algorithm(pieces, **kwargs)
    return metrics


def print_solution(individual: Individual):
    """
    Affiche la solution de manière lisible
    
    Args:
        individual: Meilleur individu trouvé
    """
    print(f"\n=== Solution Algorithme Génétique ===")
    print(f"Nombre de barres utilisées: {individual.num_bars}")
    print()
    
    for i, bar in enumerate(individual.bars, 1):
        pieces_str = ', '.join(map(str, bar['pieces']))
        used = BAR_LENGTH - bar['remaining']
        print(f"Barre {i}: [{pieces_str}] -> Utilisé: {used}/{BAR_LENGTH}, Perte: {bar['remaining']}")
    
    print(f"\nPertes totales: {individual.total_waste}")
    print(f"Efficacité: {((individual.num_bars * BAR_LENGTH - individual.total_waste) / (individual.num_bars * BAR_LENGTH) * 100):.2f}%")


if __name__ == "__main__":
    # Test avec un exemple simple
    test_pieces = [7, 6, 5, 4, 3, 3, 2, 2, 2]
    
    print(f"Pièces à découper: {test_pieces}")
    print(f"Longueur de barre: {BAR_LENGTH}")
    
    best_individual, metrics, convergence = genetic_algorithm(
        test_pieces,
        population_size=50,
        num_generations=50,
        mutation_rate=0.1,
        crossover_rate=0.8,
        verbose=True
    )
    
    print_solution(best_individual)
    
    print(f"\n=== Métriques ===")
    print(f"Temps d'exécution: {metrics['execution_time']*1000:.4f} ms")
    print(f"Mémoire utilisée: {metrics['memory_kb']:.2f} KB")
    print(f"Fitness: {metrics['fitness']:.4f}")
    print(f"\nConvergence: {len(convergence)} générations")
