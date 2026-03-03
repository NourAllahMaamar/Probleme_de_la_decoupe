"""
Module de visualisation des résultats du benchmark
"""

import csv
import os
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List


def load_aggregated_statistics(results_dir: str = 'results') -> Dict:
    """
    Charge les statistiques agrégées depuis le fichier CSV
    
    Args:
        results_dir: Répertoire contenant les résultats
        
    Returns:
        Dictionnaire avec les données par algorithme et taille
    """
    stats_path = os.path.join(results_dir, 'aggregated_statistics.csv')
    
    data = {
        'Greedy_FFD': {'sizes': [], 'num_bars': [], 'std_bars': [], 'waste': [], 'std_waste': [], 
                       'time': [], 'std_time': [], 'memory': [], 'std_memory': []},
        'Genetic': {'sizes': [], 'num_bars': [], 'std_bars': [], 'waste': [], 'std_waste': [], 
                    'time': [], 'std_time': [], 'memory': [], 'std_memory': []}
    }
    
    with open(stats_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            algo = row['algorithm']
            size = int(row['size'])
            
            data[algo]['sizes'].append(size)
            data[algo]['num_bars'].append(float(row['avg_num_bars']))
            data[algo]['std_bars'].append(float(row['std_num_bars']))
            data[algo]['waste'].append(float(row['avg_total_waste']))
            data[algo]['std_waste'].append(float(row['std_total_waste']))
            data[algo]['time'].append(float(row['avg_execution_time_ms']))
            data[algo]['std_time'].append(float(row['std_execution_time_ms']))
            data[algo]['memory'].append(float(row['avg_memory_kb']))
            data[algo]['std_memory'].append(float(row['std_memory_kb']))
    
    return data


def plot_execution_time_comparison(data: Dict, output_dir: str = 'results/figures'):
    """
    Graphique comparant les temps d'exécution
    
    Args:
        data: Données chargées
        output_dir: Répertoire de sortie pour les figures
    """
    os.makedirs(output_dir, exist_ok=True)
    
    plt.figure(figsize=(10, 6))
    
    # Greedy
    plt.errorbar(data['Greedy_FFD']['sizes'], data['Greedy_FFD']['time'],
                 yerr=data['Greedy_FFD']['std_time'],
                 marker='o', linestyle='-', linewidth=2, capsize=5,
                 label='Greedy FFD', color='#2E86AB')
    
    # Genetic
    plt.errorbar(data['Genetic']['sizes'], data['Genetic']['time'],
                 yerr=data['Genetic']['std_time'],
                 marker='s', linestyle='-', linewidth=2, capsize=5,
                 label='Algorithme Génétique', color='#A23B72')
    
    plt.xlabel('Taille du problème (nombre de pièces)', fontsize=12)
    plt.ylabel('Temps d\'exécution (ms)', fontsize=12)
    plt.title('Comparaison des temps d\'exécution', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    output_path = os.path.join(output_dir, 'execution_time_comparison.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Graphique sauvegardé: {output_path}")
    plt.close()


def plot_num_bars_comparison(data: Dict, output_dir: str = 'results/figures'):
    """
    Graphique comparant le nombre de barres utilisées
    
    Args:
        data: Données chargées
        output_dir: Répertoire de sortie pour les figures
    """
    os.makedirs(output_dir, exist_ok=True)
    
    plt.figure(figsize=(10, 6))
    
    # Greedy
    plt.errorbar(data['Greedy_FFD']['sizes'], data['Greedy_FFD']['num_bars'],
                 yerr=data['Greedy_FFD']['std_bars'],
                 marker='o', linestyle='-', linewidth=2, capsize=5,
                 label='Greedy FFD', color='#2E86AB')
    
    # Genetic
    plt.errorbar(data['Genetic']['sizes'], data['Genetic']['num_bars'],
                 yerr=data['Genetic']['std_bars'],
                 marker='s', linestyle='-', linewidth=2, capsize=5,
                 label='Algorithme Génétique', color='#A23B72')
    
    plt.xlabel('Taille du problème (nombre de pièces)', fontsize=12)
    plt.ylabel('Nombre de barres utilisées', fontsize=12)
    plt.title('Comparaison du nombre de barres utilisées', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    output_path = os.path.join(output_dir, 'num_bars_comparison.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Graphique sauvegardé: {output_path}")
    plt.close()


def plot_waste_comparison(data: Dict, output_dir: str = 'results/figures'):
    """
    Graphique comparant les pertes totales
    
    Args:
        data: Données chargées
        output_dir: Répertoire de sortie pour les figures
    """
    os.makedirs(output_dir, exist_ok=True)
    
    plt.figure(figsize=(10, 6))
    
    # Greedy
    plt.errorbar(data['Greedy_FFD']['sizes'], data['Greedy_FFD']['waste'],
                 yerr=data['Greedy_FFD']['std_waste'],
                 marker='o', linestyle='-', linewidth=2, capsize=5,
                 label='Greedy FFD', color='#2E86AB')
    
    # Genetic
    plt.errorbar(data['Genetic']['sizes'], data['Genetic']['waste'],
                 yerr=data['Genetic']['std_waste'],
                 marker='s', linestyle='-', linewidth=2, capsize=5,
                 label='Algorithme Génétique', color='#A23B72')
    
    plt.xlabel('Taille du problème (nombre de pièces)', fontsize=12)
    plt.ylabel('Pertes totales', fontsize=12)
    plt.title('Comparaison des pertes totales', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    output_path = os.path.join(output_dir, 'waste_comparison.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Graphique sauvegardé: {output_path}")
    plt.close()


def plot_improvement_percentage(results_dir: str = 'results', output_dir: str = 'results/figures'):
    """
    Graphique montrant le pourcentage d'amélioration du génétique
    
    Args:
        results_dir: Répertoire contenant les résultats
        output_dir: Répertoire de sortie pour les figures
    """
    os.makedirs(output_dir, exist_ok=True)
    
    comparison_path = os.path.join(results_dir, 'algorithm_comparison.csv')
    
    sizes = []
    improvement_bars = []
    improvement_waste = []
    
    with open(comparison_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sizes.append(int(row['size']))
            improvement_bars.append(float(row['improvement_bars_%']))
            improvement_waste.append(float(row['improvement_waste_%']))
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Amélioration en nombre de barres
    ax1.bar(range(len(sizes)), improvement_bars, color='#F18F01', alpha=0.8)
    ax1.set_xticks(range(len(sizes)))
    ax1.set_xticklabels(sizes)
    ax1.set_xlabel('Taille du problème (nombre de pièces)', fontsize=11)
    ax1.set_ylabel('Amélioration (%)', fontsize=11)
    ax1.set_title('Amélioration - Nombre de barres', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')
    ax1.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
    
    # Amélioration en pertes
    ax2.bar(range(len(sizes)), improvement_waste, color='#C73E1D', alpha=0.8)
    ax2.set_xticks(range(len(sizes)))
    ax2.set_xticklabels(sizes)
    ax2.set_xlabel('Taille du problème (nombre de pièces)', fontsize=11)
    ax2.set_ylabel('Amélioration (%)', fontsize=11)
    ax2.set_title('Amélioration - Pertes totales', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
    
    plt.tight_layout()
    
    output_path = os.path.join(output_dir, 'improvement_percentage.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Graphique sauvegardé: {output_path}")
    plt.close()


def plot_time_vs_quality_tradeoff(results_dir: str = 'results', output_dir: str = 'results/figures'):
    """
    Graphique montrant le compromis temps vs qualité
    
    Args:
        results_dir: Répertoire contenant les résultats
        output_dir: Répertoire de sortie pour les figures
    """
    os.makedirs(output_dir, exist_ok=True)
    
    comparison_path = os.path.join(results_dir, 'algorithm_comparison.csv')
    
    sizes = []
    time_ratios = []
    quality_improvements = []
    
    with open(comparison_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sizes.append(int(row['size']))
            time_ratios.append(float(row['time_ratio']))
            quality_improvements.append(float(row['improvement_bars_%']))
    
    plt.figure(figsize=(10, 6))
    
    x_pos = np.arange(len(sizes))
    width = 0.35
    
    ax1 = plt.gca()
    bars1 = ax1.bar(x_pos - width/2, time_ratios, width, label='Ratio temps (Genetic/Greedy)', 
                     color='#6A4C93', alpha=0.8)
    ax1.set_xlabel('Taille du problème (nombre de pièces)', fontsize=12)
    ax1.set_ylabel('Ratio de temps', fontsize=12, color='#6A4C93')
    ax1.tick_params(axis='y', labelcolor='#6A4C93')
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(sizes)
    
    ax2 = ax1.twinx()
    bars2 = ax2.bar(x_pos + width/2, quality_improvements, width, 
                     label='Amélioration qualité (%)', color='#2A9D8F', alpha=0.8)
    ax2.set_ylabel('Amélioration qualité (%)', fontsize=12, color='#2A9D8F')
    ax2.tick_params(axis='y', labelcolor='#2A9D8F')
    ax2.axhline(y=0, color='black', linestyle='--', linewidth=0.8, alpha=0.5)
    
    plt.title('Compromis Temps vs Qualité', fontsize=14, fontweight='bold')
    
    # Légende combinée
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)
    
    plt.tight_layout()
    
    output_path = os.path.join(output_dir, 'time_vs_quality_tradeoff.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Graphique sauvegardé: {output_path}")
    plt.close()


def plot_memory_comparison(data: Dict, output_dir: str = 'results/figures'):
    """
    Graphique comparant l'utilisation mémoire
    
    Args:
        data: Données chargées
        output_dir: Répertoire de sortie pour les figures
    """
    os.makedirs(output_dir, exist_ok=True)
    
    plt.figure(figsize=(10, 6))
    
    # Greedy
    plt.errorbar(data['Greedy_FFD']['sizes'], data['Greedy_FFD']['memory'],
                 yerr=data['Greedy_FFD']['std_memory'],
                 marker='o', linestyle='-', linewidth=2, capsize=5,
                 label='Greedy FFD', color='#2E86AB')
    
    # Genetic
    plt.errorbar(data['Genetic']['sizes'], data['Genetic']['memory'],
                 yerr=data['Genetic']['std_memory'],
                 marker='s', linestyle='-', linewidth=2, capsize=5,
                 label='Algorithme Génétique', color='#A23B72')
    
    plt.xlabel('Taille du problème (nombre de pièces)', fontsize=12)
    plt.ylabel('Utilisation mémoire (KB)', fontsize=12)
    plt.title('Comparaison de l\'utilisation mémoire', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    output_path = os.path.join(output_dir, 'memory_comparison.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Graphique sauvegardé: {output_path}")
    plt.close()


def create_all_visualizations(results_dir: str = 'results'):
    """
    Crée toutes les visualisations
    
    Args:
        results_dir: Répertoire contenant les résultats
    """
    print("\n=== GÉNÉRATION DES VISUALISATIONS ===")
    
    # Charger les données
    data = load_aggregated_statistics(results_dir)
    
    # Créer les graphiques
    plot_execution_time_comparison(data)
    plot_num_bars_comparison(data)
    plot_waste_comparison(data)
    plot_memory_comparison(data)
    plot_improvement_percentage(results_dir)
    plot_time_vs_quality_tradeoff(results_dir)
    
    print("\n✅ Toutes les visualisations ont été générées!")


if __name__ == "__main__":
    create_all_visualizations()
