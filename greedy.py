"""
Algorithme Glouton (First Fit Decreasing) pour le problème de découpe
"""

import time
import tracemalloc
from typing import List, Dict, Tuple

BAR_LENGTH = 10


class Bar:
    """Représente une barre avec sa capacité restante"""
    
    def __init__(self, length: int = BAR_LENGTH):
        self.length = length
        self.remaining = length
        self.pieces = []
    
    def can_fit(self, piece_size: int) -> bool:
        """Vérifie si une pièce peut être placée dans cette barre"""
        return self.remaining >= piece_size
    
    def add_piece(self, piece_size: int):
        """Ajoute une pièce à la barre"""
        if self.can_fit(piece_size):
            self.pieces.append(piece_size)
            self.remaining -= piece_size
            return True
        return False
    
    def get_waste(self) -> int:
        """Retourne les pertes (espace non utilisé)"""
        return self.remaining


def first_fit_decreasing(pieces: List[int]) -> Tuple[List[Bar], Dict]:
    """
    Algorithme Glouton First Fit Decreasing (FFD)
    
    Stratégie:
    1. Trier les pièces par ordre décroissant
    2. Pour chaque pièce, la placer dans la première barre où elle entre
    3. Si aucune barre ne convient, créer une nouvelle barre
    
    Args:
        pieces: Liste des tailles de pièces à découper
        
    Returns:
        - Liste des barres utilisées
        - Dictionnaire avec les métriques
    """
    # Démarrer les mesures
    tracemalloc.start()
    start_time = time.time()
    
    # Trier les pièces par ordre décroissant
    sorted_pieces = sorted(pieces, reverse=True)
    
    bars = []
    
    # Placer chaque pièce
    for piece in sorted_pieces:
        # Chercher la première barre où la pièce entre
        placed = False
        for bar in bars:
            if bar.can_fit(piece):
                bar.add_piece(piece)
                placed = True
                break
        
        # Si aucune barre ne convient, créer une nouvelle barre
        if not placed:
            new_bar = Bar()
            new_bar.add_piece(piece)
            bars.append(new_bar)
    
    # Fin des mesures
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    # Calculer les métriques
    total_waste = sum(bar.get_waste() for bar in bars)
    num_bars = len(bars)
    execution_time = end_time - start_time
    memory_used = peak / 1024  # en KB
    
    # Fitness: minimiser le nombre de barres (on peut aussi pénaliser les pertes)
    fitness = num_bars + (total_waste / (BAR_LENGTH * num_bars) if num_bars > 0 else 0)
    
    metrics = {
        'num_bars': num_bars,
        'total_waste': total_waste,
        'fitness': fitness,
        'execution_time': execution_time,
        'memory_kb': memory_used,
        'algorithm': 'Greedy_FFD'
    }
    
    return bars, metrics


def solve(pieces: List[int]) -> Dict:
    """
    Interface pour résoudre le problème avec l'algorithme glouton
    
    Args:
        pieces: Liste des tailles de pièces
        
    Returns:
        Dictionnaire avec les métriques de performance
    """
    bars, metrics = first_fit_decreasing(pieces)
    return metrics


def print_solution(bars: List[Bar]):
    """
    Affiche la solution de manière lisible
    
    Args:
        bars: Liste des barres utilisées
    """
    print(f"\n=== Solution Greedy (First Fit Decreasing) ===")
    print(f"Nombre de barres utilisées: {len(bars)}")
    print()
    
    for i, bar in enumerate(bars, 1):
        pieces_str = ', '.join(map(str, bar.pieces))
        print(f"Barre {i}: [{pieces_str}] -> Utilisé: {bar.length - bar.remaining}/{bar.length}, Perte: {bar.remaining}")
    
    total_waste = sum(bar.get_waste() for bar in bars)
    print(f"\nPertes totales: {total_waste}")
    print(f"Efficacité: {((len(bars) * BAR_LENGTH - total_waste) / (len(bars) * BAR_LENGTH) * 100):.2f}%")


if __name__ == "__main__":
    # Test avec un exemple simple
    test_pieces = [7, 6, 5, 4, 3, 3, 2, 2, 2]
    
    print(f"Pièces à découper: {test_pieces}")
    print(f"Longueur de barre: {BAR_LENGTH}")
    
    bars, metrics = first_fit_decreasing(test_pieces)
    
    print_solution(bars)
    
    print(f"\n=== Métriques ===")
    print(f"Temps d'exécution: {metrics['execution_time']*1000:.4f} ms")
    print(f"Mémoire utilisée: {metrics['memory_kb']:.2f} KB")
    print(f"Fitness: {metrics['fitness']:.4f}")
