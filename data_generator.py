"""
Module pour générer les instances de test pour le problème de découpe (Cutting Stock Problem)
"""

import random
import csv
import os
from typing import List

# Paramètres du problème
BAR_LENGTH = 10
MIN_PIECE_SIZE = 1
MAX_PIECE_SIZE = 9

def generate_instance(n: int, seed: int = None) -> List[int]:
    """
    Génère une instance du problème de découpe
    
    Args:
        n: Nombre de pièces à générer
        seed: Graine aléatoire pour la reproductibilité
        
    Returns:
        Liste des tailles de pièces
    """
    if seed is not None:
        random.seed(seed)
    
    pieces = [random.randint(MIN_PIECE_SIZE, MAX_PIECE_SIZE) for _ in range(n)]
    return pieces


def save_instance_to_csv(pieces: List[int], filename: str):
    """
    Sauvegarde une instance dans un fichier CSV
    
    Args:
        pieces: Liste des tailles de pièces
        filename: Nom du fichier de sortie
    """
    os.makedirs('datasets', exist_ok=True)
    filepath = os.path.join('datasets', filename)
    
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['piece_id', 'size'])
        for i, size in enumerate(pieces, 1):
            writer.writerow([i, size])
    
    print(f"Instance sauvegardée: {filepath}")


def load_instance_from_csv(filename: str) -> List[int]:
    """
    Charge une instance depuis un fichier CSV
    
    Args:
        filename: Nom du fichier à charger
        
    Returns:
        Liste des tailles de pièces
    """
    filepath = os.path.join('datasets', filename)
    pieces = []
    
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pieces.append(int(row['size']))
    
    return pieces


def generate_all_datasets(sizes: List[int] = [20, 50, 100, 200], num_instances: int = 5):
    """
    Génère tous les datasets pour le benchmark
    
    Args:
        sizes: Liste des tailles d'instances à générer
        num_instances: Nombre d'instances par taille
    """
    print("=== Génération des datasets ===")
    print(f"Tailles: {sizes}")
    print(f"Instances par taille: {num_instances}")
    print(f"Paramètres: BAR_LENGTH={BAR_LENGTH}, pièces entre {MIN_PIECE_SIZE} et {MAX_PIECE_SIZE}")
    print()
    
    datasets_info = []
    
    for size in sizes:
        for instance_num in range(1, num_instances + 1):
            # Utiliser une graine fixe pour la reproductibilité
            seed = size * 1000 + instance_num
            pieces = generate_instance(size, seed=seed)
            
            filename = f"instance_n{size}_i{instance_num}.csv"
            save_instance_to_csv(pieces, filename)
            
            datasets_info.append({
                'filename': filename,
                'size': size,
                'instance': instance_num,
                'num_pieces': len(pieces),
                'total_demand': sum(pieces)
            })
    
    # Sauvegarder le catalogue des datasets
    catalog_path = os.path.join('datasets', 'catalog.csv')
    with open(catalog_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['filename', 'size', 'instance', 'num_pieces', 'total_demand'])
        writer.writeheader()
        writer.writerows(datasets_info)
    
    print(f"\n✅ {len(datasets_info)} datasets générés avec succès!")
    print(f"Catalogue sauvegardé: {catalog_path}")
    
    return datasets_info


if __name__ == "__main__":
    # Générer tous les datasets
    generate_all_datasets()
