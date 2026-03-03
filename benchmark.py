"""
Script d'automatisation du benchmark pour comparer les algorithmes
"""

import os
import csv
import time
from typing import List, Dict
import greedy
import genetic
from data_generator import load_instance_from_csv


def run_experiment(algorithm_name: str, pieces: List[int], **params) -> Dict:
    """
    Exécute un algorithme sur une instance
    
    Args:
        algorithm_name: Nom de l'algorithme ('greedy' ou 'genetic')
        pieces: Liste des tailles de pièces
        **params: Paramètres supplémentaires pour l'algorithme
        
    Returns:
        Dictionnaire avec les résultats
    """
    if algorithm_name == 'greedy':
        metrics = greedy.solve(pieces)
    elif algorithm_name == 'genetic':
        metrics = genetic.solve(pieces, **params)
    else:
        raise ValueError(f"Algorithme inconnu: {algorithm_name}")
    
    return metrics


def run_benchmark(
    datasets_dir: str = 'datasets',
    results_dir: str = 'results',
    num_runs: int = 5,
    genetic_params: Dict = None
):
    """
    Exécute le benchmark complet
    
    Args:
        datasets_dir: Répertoire contenant les datasets
        results_dir: Répertoire pour sauvegarder les résultats
        num_runs: Nombre de répétitions par expérience
        genetic_params: Paramètres pour l'algorithme génétique
    """
    # Paramètres par défaut pour l'algorithme génétique
    if genetic_params is None:
        genetic_params = {
            'population_size': 100,
            'num_generations': 100,
            'mutation_rate': 0.1,
            'crossover_rate': 0.8,
            'elitism_size': 2,
            'verbose': False
        }
    
    # Créer le répertoire de résultats
    os.makedirs(results_dir, exist_ok=True)
    
    # Charger le catalogue des datasets
    catalog_path = os.path.join(datasets_dir, 'catalog.csv')
    datasets = []
    
    with open(catalog_path, 'r') as f:
        reader = csv.DictReader(f)
        datasets = list(reader)
    
    print("=== BENCHMARK DES ALGORITHMES ===")
    print(f"Nombre de datasets: {len(datasets)}")
    print(f"Répétitions par expérience: {num_runs}")
    print(f"Algorithmes: Greedy FFD, Genetic")
    print(f"Paramètres génétique: {genetic_params}")
    print()
    
    # Préparer le fichier de résultats détaillés
    detailed_results_path = os.path.join(results_dir, 'detailed_results.csv')
    detailed_file = open(detailed_results_path, 'w', newline='')
    detailed_writer = csv.writer(detailed_file)
    detailed_writer.writerow([
        'dataset', 'size', 'instance', 'algorithm', 'run',
        'num_bars', 'total_waste', 'fitness',
        'execution_time_ms', 'memory_kb'
    ])
    
    # Compteur de progression
    total_experiments = len(datasets) * 2 * num_runs  # 2 algorithmes
    current = 0
    
    # Pour chaque dataset
    for dataset_info in datasets:
        filename = dataset_info['filename']
        size = int(dataset_info['size'])
        instance = int(dataset_info['instance'])
        
        print(f"📊 Dataset: {filename} (n={size}, instance {instance})")
        
        # Charger les pièces
        pieces = load_instance_from_csv(filename)
        
        # Tester l'algorithme glouton
        print(f"  🔹 Greedy FFD...", end=' ', flush=True)
        for run in range(1, num_runs + 1):
            metrics = run_experiment('greedy', pieces)
            
            detailed_writer.writerow([
                filename, size, instance, 'Greedy_FFD', run,
                metrics['num_bars'],
                metrics['total_waste'],
                metrics['fitness'],
                metrics['execution_time'] * 1000,  # convertir en ms
                metrics['memory_kb']
            ])
            
            current += 1
        print(f"✅ ({current}/{total_experiments})")
        
        # Tester l'algorithme génétique
        print(f"  🔹 Genetic...", end=' ', flush=True)
        for run in range(1, num_runs + 1):
            metrics = run_experiment('genetic', pieces, **genetic_params)
            
            detailed_writer.writerow([
                filename, size, instance, 'Genetic', run,
                metrics['num_bars'],
                metrics['total_waste'],
                metrics['fitness'],
                metrics['execution_time'] * 1000,  # convertir en ms
                metrics['memory_kb']
            ])
            
            current += 1
        print(f"✅ ({current}/{total_experiments})")
    
    detailed_file.close()
    
    print(f"\n✅ Benchmark terminé!")
    print(f"Résultats détaillés: {detailed_results_path}")
    
    # Calculer les statistiques agrégées
    compute_aggregated_statistics(detailed_results_path, results_dir)


def compute_aggregated_statistics(detailed_results_path: str, results_dir: str):
    """
    Calcule les statistiques agrégées à partir des résultats détaillés
    
    Args:
        detailed_results_path: Chemin vers le fichier de résultats détaillés
        results_dir: Répertoire pour sauvegarder les statistiques
    """
    import numpy as np
    
    print("\n=== CALCUL DES STATISTIQUES ===")
    
    # Charger les résultats
    results = []
    with open(detailed_results_path, 'r') as f:
        reader = csv.DictReader(f)
        results = list(reader)
    
    # Grouper par (size, algorithm)
    groups = {}
    for row in results:
        size = int(row['size'])
        algo = row['algorithm']
        key = (size, algo)
        
        if key not in groups:
            groups[key] = {
                'num_bars': [],
                'total_waste': [],
                'execution_time_ms': [],
                'memory_kb': []
            }
        
        groups[key]['num_bars'].append(int(row['num_bars']))
        groups[key]['total_waste'].append(int(row['total_waste']))
        groups[key]['execution_time_ms'].append(float(row['execution_time_ms']))
        groups[key]['memory_kb'].append(float(row['memory_kb']))
    
    # Calculer les statistiques
    stats_path = os.path.join(results_dir, 'aggregated_statistics.csv')
    with open(stats_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'size', 'algorithm',
            'avg_num_bars', 'std_num_bars',
            'avg_total_waste', 'std_total_waste',
            'avg_execution_time_ms', 'std_execution_time_ms',
            'avg_memory_kb', 'std_memory_kb'
        ])
        
        for (size, algo), data in sorted(groups.items()):
            writer.writerow([
                size, algo,
                np.mean(data['num_bars']), np.std(data['num_bars']),
                np.mean(data['total_waste']), np.std(data['total_waste']),
                np.mean(data['execution_time_ms']), np.std(data['execution_time_ms']),
                np.mean(data['memory_kb']), np.std(data['memory_kb'])
            ])
    
    print(f"✅ Statistiques agrégées: {stats_path}")
    
    # Calculer les comparaisons entre algorithmes
    comparison_path = os.path.join(results_dir, 'algorithm_comparison.csv')
    with open(comparison_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'size',
            'greedy_avg_bars', 'genetic_avg_bars', 'improvement_bars_%',
            'greedy_avg_waste', 'genetic_avg_waste', 'improvement_waste_%',
            'greedy_avg_time_ms', 'genetic_avg_time_ms', 'time_ratio'
        ])
        
        sizes = sorted(set(size for size, _ in groups.keys()))
        
        for size in sizes:
            greedy_data = groups.get((size, 'Greedy_FFD'))
            genetic_data = groups.get((size, 'Genetic'))
            
            if greedy_data and genetic_data:
                greedy_bars = np.mean(greedy_data['num_bars'])
                genetic_bars = np.mean(genetic_data['num_bars'])
                improvement_bars = ((greedy_bars - genetic_bars) / greedy_bars * 100) if greedy_bars > 0 else 0
                
                greedy_waste = np.mean(greedy_data['total_waste'])
                genetic_waste = np.mean(genetic_data['total_waste'])
                improvement_waste = ((greedy_waste - genetic_waste) / greedy_waste * 100) if greedy_waste > 0 else 0
                
                greedy_time = np.mean(greedy_data['execution_time_ms'])
                genetic_time = np.mean(genetic_data['execution_time_ms'])
                time_ratio = genetic_time / greedy_time if greedy_time > 0 else 0
                
                writer.writerow([
                    size,
                    greedy_bars, genetic_bars, improvement_bars,
                    greedy_waste, genetic_waste, improvement_waste,
                    greedy_time, genetic_time, time_ratio
                ])
    
    print(f"✅ Comparaison des algorithmes: {comparison_path}")


if __name__ == "__main__":
    # Exécuter le benchmark complet
    run_benchmark(
        num_runs=5,
        genetic_params={
            'population_size': 100,
            'num_generations': 100,
            'mutation_rate': 0.1,
            'crossover_rate': 0.8,
            'elitism_size': 2,
            'verbose': False
        }
    )
    
    print("\n🎉 Benchmark terminé avec succès!")
