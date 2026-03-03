# Benchmark - Problème de la Découpe (Cutting Stock Problem)

## 📋 Description

Ce projet implémente et compare deux algorithmes pour résoudre le problème de découpe (Cutting Stock Problem):

1. **Algorithme Glouton (First Fit Decreasing)** - Approche déterministe rapide
2. **Algorithme Génétique** - Métaheuristique évolutionnaire

Le projet suit rigoureusement le guide de benchmarking des algorithmes avec génération automatique de données, mesures de performance, visualisations et analyse détaillée.

## 🎯 Problème

**Objectif:** Minimiser le nombre de barres utilisées pour découper un ensemble de pièces.

**Contraintes:**
- Longueur fixe des barres: 10 unités
- Pièces de taille variable: 1 à 9 unités
- Chaque pièce doit être découpée dans une seule barre

## 📁 Structure du Projet

```
.
├── data_generator.py       # Génération des instances de test
├── greedy.py              # Algorithme Glouton (FFD)
├── genetic.py             # Algorithme Génétique
├── benchmark.py           # Automatisation des expériences
├── visualization.py       # Génération des graphiques
├── main.py               # Script principal d'exécution
├── requirements.txt      # Dépendances Python
└── README.md            # Ce fichier
```

## 🚀 Installation

### Prérequis

- Python 3.7 ou supérieur
- pip

### Installation des dépendances

```bash
pip install -r requirements.txt
```

## ▶️ Utilisation

### Exécution complète du benchmark

Pour exécuter tout le pipeline (génération de données, benchmark, visualisation, analyse):

```bash
python main.py
```

Cette commande va:
1. ✅ Générer 20 instances de test (4 tailles × 5 instances)
2. ✅ Exécuter les deux algorithmes sur toutes les instances (5 répétitions)
3. ✅ Calculer les statistiques agrégées
4. ✅ Générer 6 graphiques de comparaison
5. ✅ Produire un rapport d'analyse complet

**Temps d'exécution estimé:** 2-5 minutes (selon votre machine)

### Exécution par module

#### 1. Générer uniquement les datasets

```bash
python data_generator.py
```

#### 2. Tester l'algorithme Glouton

```bash
python greedy.py
```

#### 3. Tester l'algorithme Génétique

```bash
python genetic.py
```

#### 4. Exécuter le benchmark

```bash
python benchmark.py
```

#### 5. Générer les visualisations

```bash
python visualization.py
```

## 📊 Résultats Générés

Après l'exécution, les fichiers suivants sont créés:

### Données

- `datasets/instance_n{size}_i{num}.csv` - Instances de test
- `datasets/catalog.csv` - Catalogue des datasets

### Résultats

- `results/detailed_results.csv` - Résultats détaillés de chaque exécution
- `results/aggregated_statistics.csv` - Statistiques agrégées par algorithme/taille
- `results/algorithm_comparison.csv` - Comparaison directe des algorithmes

### Visualisations

- `results/figures/execution_time_comparison.png` - Comparaison temps d'exécution
- `results/figures/num_bars_comparison.png` - Comparaison nombre de barres
- `results/figures/waste_comparison.png` - Comparaison pertes totales
- `results/figures/memory_comparison.png` - Comparaison utilisation mémoire
- `results/figures/improvement_percentage.png` - Pourcentages d'amélioration
- `results/figures/time_vs_quality_tradeoff.png` - Compromis temps/qualité

### Analyse

- `results/analysis_report.md` - Rapport d'analyse complet avec conclusions

## ⚙️ Configuration

### Paramètres du Benchmark

Dans `main.py`, vous pouvez modifier:

```python
# Tailles des instances à tester
generate_all_datasets(sizes=[20, 50, 100, 200], num_instances=5)

# Nombre de répétitions
run_benchmark(num_runs=5, ...)

# Paramètres de l'algorithme génétique
genetic_params={
    'population_size': 100,      # Taille de la population
    'num_generations': 100,      # Nombre de générations
    'mutation_rate': 0.1,        # Taux de mutation (0-1)
    'crossover_rate': 0.8,       # Taux de croisement (0-1)
    'elitism_size': 2,          # Nombre d'élites préservés
    'verbose': False            # Afficher les détails
}
```

## 📈 Métriques Calculées

Pour chaque algorithme et instance:

- **Nombre de barres utilisées** - Objectif principal à minimiser
- **Pertes totales** - Somme des espaces non utilisés
- **Fitness** - Fonction de coût combinée
- **Temps d'exécution** - En millisecondes
- **Utilisation mémoire** - En kilooctets

## 🧮 Algorithmes

### Greedy First Fit Decreasing (FFD)

**Stratégie:**
1. Trier les pièces par ordre décroissant
2. Pour chaque pièce, la placer dans la première barre où elle entre
3. Si aucune barre ne convient, créer une nouvelle barre

**Complexité:** O(n log n + n·m)

**Garantie:** Au plus 11/9 · OPT + 1 barres

### Algorithme Génétique

**Représentation:** Permutation des pièces (ordre de placement)

**Opérateurs:**
- **Sélection:** Tournoi (taille 3)
- **Croisement:** Order Crossover (OX)
- **Mutation:** Swap de deux positions
- **Élitisme:** Conservation des 2 meilleurs

**Fitness:** Minimiser nombre de barres + pénalité pour les pertes

## 📊 Exemple de Résultats

```
Taille | Greedy (barres) | Genetic (barres) | Amélioration
-------|----------------|------------------|-------------
20     | 12.4           | 12.0            | +3.2%
50     | 30.8           | 29.6            | +3.9%
100    | 61.2           | 59.1            | +3.4%
200    | 122.5          | 118.8           | +3.0%
```

## 🎓 Analyse Théorique vs Pratique

Le projet permet de vérifier expérimentalement:

- ✅ La complexité temporelle des algorithmes
- ✅ Le compromis temps/qualité
- ✅ La scalabilité selon la taille du problème
- ✅ L'impact des paramètres (pour le génétique)

## 🔧 Extensions Possibles

### BONUS implémentés

- ✅ Configuration flexible des paramètres
- ✅ Export automatique des graphiques (PNG haute résolution)
- ✅ Rapport automatique détaillé (Markdown)

### Améliorations futures

- 📄 Export du rapport en PDF (nécessite `reportlab` ou `weasyprint`)
- 🔄 Algorithme hybride (initialisation génétique avec FFD)
- ⚡ Parallélisation de l'algorithme génétique
- 📊 Interface graphique interactive
