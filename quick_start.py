"""
Script de démarrage rapide - Test avec une petite instance
"""

import greedy
import genetic

# Instance de test simple
test_pieces = [7, 6, 5, 4, 3, 3, 2, 2, 2, 8, 7, 5, 4, 3]

print("=" * 70)
print(" " * 20 + "TEST RAPIDE")
print("=" * 70)
print(f"\nPièces à découper: {test_pieces}")
print(f"Nombre total de pièces: {len(test_pieces)}")
print(f"Longueur des barres: 10")
print()

# Test Greedy
print("=" * 70)
print("🔹 ALGORITHME GLOUTON (First Fit Decreasing)")
print("=" * 70)
bars_greedy, metrics_greedy = greedy.first_fit_decreasing(test_pieces)
greedy.print_solution(bars_greedy)
print(f"\n⏱️  Temps: {metrics_greedy['execution_time']*1000:.4f} ms")
print(f"💾 Mémoire: {metrics_greedy['memory_kb']:.2f} KB")

# Test Genetic
print("\n" + "=" * 70)
print("🔹 ALGORITHME GÉNÉTIQUE")
print("=" * 70)
print("Configuration: Population=50, Générations=50")
print()

best_individual, metrics_genetic, convergence = genetic.genetic_algorithm(
    test_pieces,
    population_size=50,
    num_generations=50,
    mutation_rate=0.1,
    crossover_rate=0.8,
    verbose=True
)

genetic.print_solution(best_individual)
print(f"\n⏱️  Temps: {metrics_genetic['execution_time']*1000:.4f} ms")
print(f"💾 Mémoire: {metrics_genetic['memory_kb']:.2f} KB")

# Comparaison
print("\n" + "=" * 70)
print("📊 COMPARAISON")
print("=" * 70)
print(f"\nNombre de barres:")
print(f"  Greedy:  {metrics_greedy['num_bars']}")
print(f"  Genetic: {metrics_genetic['num_bars']}")

if metrics_greedy['num_bars'] > metrics_genetic['num_bars']:
    improvement = ((metrics_greedy['num_bars'] - metrics_genetic['num_bars']) / metrics_greedy['num_bars'] * 100)
    print(f"  ➡️  Génétique est meilleur de {improvement:.1f}%")
elif metrics_greedy['num_bars'] < metrics_genetic['num_bars']:
    print(f"  ➡️  Glouton est meilleur")
else:
    print(f"  ➡️  Résultats identiques")

print(f"\nPertes totales:")
print(f"  Greedy:  {metrics_greedy['total_waste']}")
print(f"  Genetic: {metrics_genetic['total_waste']}")

print(f"\nTemps d'exécution:")
print(f"  Greedy:  {metrics_greedy['execution_time']*1000:.4f} ms")
print(f"  Genetic: {metrics_genetic['execution_time']*1000:.4f} ms")
ratio = metrics_genetic['execution_time'] / metrics_greedy['execution_time']
print(f"  ➡️  Génétique est {ratio:.1f}x plus lent")

print("\n" + "=" * 70)
print("✅ Test terminé!")
print("=" * 70)
print("\n💡 Pour le benchmark complet, exécutez: python main.py")
print()
