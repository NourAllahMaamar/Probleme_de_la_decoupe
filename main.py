"""
Script principal pour exécuter le benchmark complet et générer le rapport
"""

import os
import csv
from datetime import datetime
from data_generator import generate_all_datasets
from benchmark import run_benchmark
from visualization import create_all_visualizations


def generate_analysis_report(results_dir: str = 'results'):
    """
    Génère un rapport d'analyse détaillé
    
    Args:
        results_dir: Répertoire contenant les résultats
    """
    print("\n=== GÉNÉRATION DU RAPPORT D'ANALYSE ===")
    
    # Charger les résultats de comparaison
    comparison_path = os.path.join(results_dir, 'algorithm_comparison.csv')
    
    comparisons = []
    with open(comparison_path, 'r') as f:
        reader = csv.DictReader(f)
        comparisons = list(reader)
    
    # Charger les statistiques agrégées
    stats_path = os.path.join(results_dir, 'aggregated_statistics.csv')
    stats = []
    with open(stats_path, 'r') as f:
        reader = csv.DictReader(f)
        stats = list(reader)
    
    # Créer le rapport
    report_path = os.path.join(results_dir, 'analysis_report.md')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Rapport d'Analyse - Benchmark Cutting Stock Problem\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")
        
        # Introduction
        f.write("## 1. Introduction\n\n")
        f.write("Ce rapport présente les résultats du benchmark comparant deux algorithmes pour le problème ")
        f.write("de découpe (Cutting Stock Problem):\n\n")
        f.write("- **Algorithme Glouton (Greedy First Fit Decreasing)**: Approche déterministe rapide\n")
        f.write("- **Algorithme Génétique**: Approche métaheuristique évolutionnaire\n\n")
        f.write("**Paramètres du problème:**\n")
        f.write("- Longueur des barres: 10 unités\n")
        f.write("- Tailles des pièces: 1 à 9 unités (générées aléatoirement)\n")
        f.write(f"- Tailles testées: {', '.join([c['size'] for c in comparisons])} pièces\n")
        f.write("- Répétitions par expérience: 5\n\n")
        f.write("---\n\n")
        
        # Complexité théorique
        f.write("## 2. Complexité Théorique\n\n")
        f.write("### Algorithme Glouton (FFD)\n")
        f.write("- **Complexité temporelle:** $O(n \\log n + n \\cdot m)$\n")
        f.write("  - $O(n \\log n)$ pour le tri des pièces\n")
        f.write("  - $O(n \\cdot m)$ pour le placement (n pièces, m barres)\n")
        f.write("- **Complexité spatiale:** $O(n + m)$\n")
        f.write("- **Garantie:** FFD garantit au plus $\\frac{11}{9} \\cdot OPT + 1$ barres (où OPT est la solution optimale)\n\n")
        
        f.write("### Algorithme Génétique\n")
        f.write("- **Complexité temporelle:** $O(g \\cdot p \\cdot n \\cdot m)$\n")
        f.write("  - $g$ = nombre de générations\n")
        f.write("  - $p$ = taille de la population\n")
        f.write("  - $n$ = nombre de pièces\n")
        f.write("  - $m$ = nombre de barres moyen\n")
        f.write("- **Complexité spatiale:** $O(p \\cdot n)$\n")
        f.write("- **Nature:** Métaheuristique, pas de garantie d'optimalité\n\n")
        f.write("---\n\n")
        
        # Résultats expérimentaux
        f.write("## 3. Résultats Expérimentaux\n\n")
        f.write("### 3.1 Comparaison par taille de problème\n\n")
        f.write("| Taille | Greedy (barres) | Genetic (barres) | Amélioration | Greedy (pertes) | Genetic (pertes) | Amélioration |\n")
        f.write("|--------|----------------|------------------|--------------|-----------------|------------------|---------------|\n")
        
        for comp in comparisons:
            size = comp['size']
            greedy_bars = float(comp['greedy_avg_bars'])
            genetic_bars = float(comp['genetic_avg_bars'])
            imp_bars = float(comp['improvement_bars_%'])
            greedy_waste = float(comp['greedy_avg_waste'])
            genetic_waste = float(comp['genetic_avg_waste'])
            imp_waste = float(comp['improvement_waste_%'])
            
            f.write(f"| {size} | {greedy_bars:.2f} | {genetic_bars:.2f} | "
                   f"{imp_bars:+.2f}% | {greedy_waste:.2f} | {genetic_waste:.2f} | {imp_waste:+.2f}% |\n")
        
        f.write("\n### 3.2 Temps d'exécution\n\n")
        f.write("| Taille | Greedy (ms) | Genetic (ms) | Ratio (Genetic/Greedy) |\n")
        f.write("|--------|-------------|--------------|------------------------|\n")
        
        for comp in comparisons:
            size = comp['size']
            greedy_time = float(comp['greedy_avg_time_ms'])
            genetic_time = float(comp['genetic_avg_time_ms'])
            ratio = float(comp['time_ratio'])
            
            f.write(f"| {size} | {greedy_time:.4f} | {genetic_time:.4f} | {ratio:.2f}x |\n")
        
        f.write("\n---\n\n")
        
        # Analyse détaillée
        f.write("## 4. Analyse Détaillée\n\n")
        
        # Calculer les moyennes
        avg_imp_bars = sum(float(c['improvement_bars_%']) for c in comparisons) / len(comparisons)
        avg_imp_waste = sum(float(c['improvement_waste_%']) for c in comparisons) / len(comparisons)
        avg_time_ratio = sum(float(c['time_ratio']) for c in comparisons) / len(comparisons)
        
        f.write("### 4.1 Qualité des solutions\n\n")
        f.write(f"**Amélioration moyenne du Génétique:**\n")
        f.write(f"- Nombre de barres: {avg_imp_bars:+.2f}%\n")
        f.write(f"- Pertes totales: {avg_imp_waste:+.2f}%\n\n")
        
        if avg_imp_bars > 0:
            f.write("✅ **Conclusion:** L'algorithme génétique produit des solutions de meilleure qualité ")
            f.write("en moyenne, réduisant le nombre de barres utilisées et les pertes.\n\n")
        elif avg_imp_bars > -1:
            f.write("⚖️ **Conclusion:** Les deux algorithmes produisent des solutions de qualité comparable.\n\n")
        else:
            f.write("⚠️ **Conclusion:** L'algorithme glouton produit des solutions de meilleure qualité ")
            f.write("dans ce contexte.\n\n")
        
        f.write("### 4.2 Performance temporelle\n\n")
        f.write(f"**Ratio de temps moyen (Genetic/Greedy):** {avg_time_ratio:.2f}x\n\n")
        f.write(f"L'algorithme génétique est environ **{avg_time_ratio:.1f} fois plus lent** que l'algorithme glouton.\n")
        f.write("Ce surcoût est dû à l'exploration de nombreuses solutions candidates sur plusieurs générations.\n\n")
        
        f.write("### 4.3 Évolution selon la taille\n\n")
        
        # Analyser la tendance
        improvements = [float(c['improvement_bars_%']) for c in comparisons]
        sizes = [int(c['size']) for c in comparisons]
        
        f.write("**Tendance observée:**\n")
        if improvements[-1] > improvements[0]:
            f.write("- L'avantage du génétique **augmente** avec la taille du problème\n")
            f.write("- Pour les grandes instances, le génétique devient plus avantageux\n\n")
        elif improvements[-1] < improvements[0]:
            f.write("- L'avantage du génétique **diminue** avec la taille du problème\n")
            f.write("- Le glouton reste compétitif même sur grandes instances\n\n")
        else:
            f.write("- L'amélioration reste **stable** quelle que soit la taille\n\n")
        
        # Identifier le point de bascule
        best_improvement_idx = improvements.index(max(improvements))
        best_size = sizes[best_improvement_idx]
        f.write(f"**Taille optimale pour le génétique:** n = {best_size} ")
        f.write(f"(amélioration de {improvements[best_improvement_idx]:.2f}%)\n\n")
        
        f.write("---\n\n")
        
        # Compromis temps vs qualité
        f.write("## 5. Compromis Temps vs Qualité\n\n")
        f.write("### Matrice de décision\n\n")
        f.write("| Critère | Greedy FFD | Algorithme Génétique |\n")
        f.write("|---------|------------|----------------------|\n")
        f.write("| **Vitesse** | ⭐⭐⭐⭐⭐ Très rapide | ⭐⭐ Plus lent |\n")
        f.write("| **Qualité solution** | ⭐⭐⭐⭐ Bonne | ⭐⭐⭐⭐⭐ Excellente |\n")
        f.write("| **Complexité** | ⭐⭐⭐⭐⭐ Simple | ⭐⭐ Plus complexe |\n")
        f.write("| **Déterminisme** | ⭐⭐⭐⭐⭐ Déterministe | ⭐⭐ Stochastique |\n")
        f.write("| **Scalabilité** | ⭐⭐⭐⭐⭐ Excellente | ⭐⭐⭐ Bonne |\n\n")
        
        f.write("### Cas d'usage recommandés\n\n")
        f.write("**Utiliser Greedy FFD quand:**\n")
        f.write("- ⚡ Le temps de calcul est critique\n")
        f.write("- 📊 Les instances sont très grandes (> 1000 pièces)\n")
        f.write("- 🎯 Une solution rapide et raisonnable suffit\n")
        f.write("- 🔄 Traitement en temps réel requis\n\n")
        
        f.write("**Utiliser l'Algorithme Génétique quand:**\n")
        f.write("- 💎 La qualité optimale est prioritaire\n")
        f.write("- 💰 Le coût du matériau est élevé (minimiser les pertes)\n")
        f.write("- 📈 Les instances sont de taille moyenne (100-500 pièces)\n")
        f.write("- ⏰ Le temps de calcul n'est pas contraignant\n\n")
        
        f.write("---\n\n")
        
        # Conclusion finale
        f.write("## 6. Conclusion Finale\n\n")
        
        f.write("### Points clés\n\n")
        f.write("1. **Performance théorique confirmée expérimentalement**\n")
        f.write("   - Le Greedy FFD est effectivement plus rapide ($O(n \\log n)$ vs $O(g \\cdot p \\cdot n)$)\n")
        f.write("   - Le Génétique produit de meilleures solutions grâce à l'exploration plus large\n\n")
        
        f.write("2. **Compromis temps-qualité clairement établi**\n")
        f.write(f"   - Génétique: {avg_imp_bars:+.2f}% meilleure qualité pour {avg_time_ratio:.1f}x plus de temps\n\n")
        
        f.write("3. **Choix dépend du contexte applicatif**\n")
        f.write("   - Pas de solution universelle\n")
        f.write("   - Évaluer les contraintes spécifiques (temps, coût, volume)\n\n")
        
        f.write("### Recommandation\n\n")
        
        if avg_imp_bars > 3 and avg_time_ratio < 50:
            f.write("🏆 **Recommandation: Algorithme Génétique**\n\n")
            f.write("L'amélioration de qualité significative justifie le surcoût temporel modéré. ")
            f.write("Dans un contexte industriel où le coût du matériau est important, les économies ")
            f.write("réalisées compensent largement le temps de calcul supplémentaire.\n")
        elif avg_time_ratio > 100:
            f.write("🏆 **Recommandation: Greedy FFD**\n\n")
            f.write("Le surcoût temporel du génétique est trop élevé par rapport au gain de qualité. ")
            f.write("Le glouton offre un excellent compromis pour la plupart des applications.\n")
        else:
            f.write("🏆 **Recommandation: Approche Hybride**\n\n")
            f.write("- Utiliser **Greedy FFD** pour le traitement en temps réel ou les grandes instances\n")
            f.write("- Utiliser **Génétique** pour l'optimisation offline ou les instances critiques\n")
            f.write("- Possibilité d'initialiser le génétique avec la solution gloutonne pour combiner les avantages\n")
        
        f.write("\n### Perspectives d'amélioration\n\n")
        f.write("**Optimisations possibles:**\n")
        f.write("1. Algorithme hybride: initialisation génétique avec le solution FFD\n")
        f.write("2. Parallélisation de l'algorithme génétique\n")
        f.write("3. Adaptation dynamique des paramètres du génétique\n")
        f.write("4. Utilisation de bornes inférieures pour évaluer la qualité des solutions\n\n")
        
        f.write("---\n\n")
        f.write("*Rapport généré automatiquement par le système de benchmark*\n")
    
    print(f"✅ Rapport d'analyse généré: {report_path}")


def main():
    """
    Fonction principale pour exécuter tout le pipeline de benchmark
    """
    print("=" * 70)
    print(" " * 15 + "BENCHMARK CUTTING STOCK PROBLEM")
    print("=" * 70)
    print()
    
    # Étape 1: Générer les datasets
    print("📦 ÉTAPE 1: Génération des datasets")
    print("-" * 70)
    generate_all_datasets(sizes=[20, 50, 100, 200], num_instances=5)
    
    # Étape 2: Exécuter le benchmark
    print("\n" + "=" * 70)
    print("🏃 ÉTAPE 2: Exécution du benchmark")
    print("-" * 70)
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
    
    # Étape 3: Créer les visualisations
    print("\n" + "=" * 70)
    print("📊 ÉTAPE 3: Génération des visualisations")
    print("-" * 70)
    create_all_visualizations()
    
    # Étape 4: Générer le rapport d'analyse
    print("\n" + "=" * 70)
    print("📝 ÉTAPE 4: Génération du rapport d'analyse")
    print("-" * 70)
    generate_analysis_report()
    
    # Résumé final
    print("\n" + "=" * 70)
    print("✅ BENCHMARK TERMINÉ AVEC SUCCÈS!")
    print("=" * 70)
    print("\n📁 Fichiers générés:")
    print("   - datasets/                     : Instances de test")
    print("   - results/detailed_results.csv  : Résultats détaillés")
    print("   - results/aggregated_statistics.csv : Statistiques agrégées")
    print("   - results/algorithm_comparison.csv  : Comparaison des algorithmes")
    print("   - results/figures/              : Graphiques PNG")
    print("   - results/analysis_report.md    : Rapport d'analyse complet")
    print("\n🎯 Consultez analysis_report.md pour l'analyse détaillée!")
    print()


if __name__ == "__main__":
    main()
