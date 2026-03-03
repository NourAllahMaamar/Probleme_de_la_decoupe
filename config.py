"""
Fichier de configuration pour le benchmark
Modifiez les paramètres ici pour personnaliser l'exécution
"""

# ============================================================================
# PARAMÈTRES DU PROBLÈME
# ============================================================================

# Longueur des barres
BAR_LENGTH = 10

# Plage de tailles des pièces
MIN_PIECE_SIZE = 1
MAX_PIECE_SIZE = 9


# ============================================================================
# GÉNÉRATION DES DATASETS
# ============================================================================

# Tailles des instances à générer (nombre de pièces)
DATASET_SIZES = [20, 50, 100, 200]

# Nombre d'instances par taille
NUM_INSTANCES_PER_SIZE = 5


# ============================================================================
# PARAMÈTRES DU BENCHMARK
# ============================================================================

# Nombre de répétitions par expérience (pour calculer les moyennes)
NUM_RUNS = 5


# ============================================================================
# PARAMÈTRES DE L'ALGORITHME GÉNÉTIQUE
# ============================================================================

# Taille de la population
GENETIC_POPULATION_SIZE = 100

# Nombre de générations
GENETIC_NUM_GENERATIONS = 100

# Taux de mutation (probabilité de mutation d'un individu)
# Valeur recommandée: 0.05 - 0.2
GENETIC_MUTATION_RATE = 0.1

# Taux de croisement (probabilité de croisement entre deux parents)
# Valeur recommandée: 0.6 - 0.9
GENETIC_CROSSOVER_RATE = 0.8

# Nombre d'individus élites préservés à chaque génération
# Valeur recommandée: 1 - 5
GENETIC_ELITISM_SIZE = 2

# Afficher les détails de progression du génétique
GENETIC_VERBOSE = False


# ============================================================================
# PARAMÈTRES DE VISUALISATION
# ============================================================================

# Résolution des graphiques (DPI)
# 300 = haute qualité, 150 = qualité moyenne, 72 = basse qualité
FIGURE_DPI = 300

# Palette de couleurs pour les graphiques
COLOR_GREEDY = '#2E86AB'    # Bleu
COLOR_GENETIC = '#A23B72'   # Violet


# ============================================================================
# CHEMINS DES FICHIERS
# ============================================================================

# Répertoire pour les datasets
DATASETS_DIR = 'datasets'

# Répertoire pour les résultats
RESULTS_DIR = 'results'

# Répertoire pour les figures
FIGURES_DIR = 'results/figures'


# ============================================================================
# NOTES D'UTILISATION
# ============================================================================

"""
CONSEILS POUR AJUSTER LES PARAMÈTRES:

1. Pour des tests rapides:
   - DATASET_SIZES = [20, 50]
   - NUM_RUNS = 3
   - GENETIC_NUM_GENERATIONS = 50

2. Pour un benchmark exhaustif:
   - DATASET_SIZES = [20, 50, 100, 200, 500]
   - NUM_RUNS = 10
   - GENETIC_NUM_GENERATIONS = 200

3. Pour améliorer la qualité du génétique:
   - Augmenter GENETIC_POPULATION_SIZE (150-200)
   - Augmenter GENETIC_NUM_GENERATIONS (150-300)
   - Réduire GENETIC_MUTATION_RATE (0.05)

4. Pour accélérer le génétique:
   - Réduire GENETIC_POPULATION_SIZE (50)
   - Réduire GENETIC_NUM_GENERATIONS (50)
   
5. Impact de la taille de population:
   - Petite (50): Plus rapide, peut converger prématurément
   - Moyenne (100): Bon équilibre
   - Grande (200): Plus lent, exploration plus complète

6. Impact du taux de mutation:
   - Faible (0.05): Convergence rapide, risque de minimum local
   - Moyen (0.1): Équilibre exploration/exploitation
   - Élevé (0.3): Plus d'exploration, convergence lente
"""
