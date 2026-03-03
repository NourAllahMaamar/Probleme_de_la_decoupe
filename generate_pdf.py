"""
Script pour générer un PDF à partir du rapport HTML
"""

import os
import subprocess
import webbrowser
from pathlib import Path


def generate_pdf_from_html():
    """
    Génère un PDF à partir du rapport HTML
    
    Méthodes disponibles (dans l'ordre de préférence):
    1. Utiliser le navigateur (méthode manuelle recommandée)
    2. Utiliser wkhtmltopdf (si installé)
    3. Utiliser weasyprint (si installé)
    """
    
    html_file = Path('results/Rapport_Complet_Benchmark.html').absolute()
    pdf_file = Path('results/Rapport_Complet_Benchmark.pdf').absolute()
    
    if not html_file.exists():
        print(f"❌ Fichier HTML introuvable: {html_file}")
        return False
    
    print("=" * 70)
    print(" " * 15 + "GÉNÉRATION DU RAPPORT PDF")
    print("=" * 70)
    print()
    
    # Méthode 1: Ouvrir dans le navigateur pour impression manuelle (RECOMMANDÉ)
    print("📄 Méthode 1: Impression via navigateur (RECOMMANDÉE)")
    print("-" * 70)
    print("Le rapport HTML va s'ouvrir dans votre navigateur.")
    print()
    print("Pour générer le PDF:")
    print("  1. Attendez que la page soit complètement chargée")
    print("  2. Utilisez Fichier → Imprimer (ou Ctrl+P / Cmd+P)")
    print("  3. Sélectionnez 'Enregistrer au format PDF' comme destination")
    print("  4. Sauvegardez le fichier sous: Rapport_Complet_Benchmark.pdf")
    print()
    
    response = input("Voulez-vous ouvrir le rapport dans votre navigateur? (o/n): ")
    if response.lower() in ['o', 'oui', 'y', 'yes']:
        webbrowser.open(f'file://{html_file}')
        print(f"✅ Rapport ouvert dans le navigateur: {html_file}")
        print()
        print("💡 Une fois le PDF généré, placez-le dans le dossier 'results/'")
        return True
    
    print()
    
    # Méthode 2: wkhtmltopdf
    print("📄 Méthode 2: Utilisation de wkhtmltopdf")
    print("-" * 70)
    
    if check_tool_installed('wkhtmltopdf'):
        print("✅ wkhtmltopdf est installé")
        try:
            cmd = [
                'wkhtmltopdf',
                '--enable-local-file-access',
                '--print-media-type',
                '--no-stop-slow-scripts',
                '--javascript-delay', '1000',
                str(html_file),
                str(pdf_file)
            ]
            subprocess.run(cmd, check=True)
            print(f"✅ PDF généré avec succès: {pdf_file}")
            return True
        except Exception as e:
            print(f"❌ Erreur lors de la génération: {e}")
    else:
        print("❌ wkhtmltopdf n'est pas installé")
        print("   Installation: https://wkhtmltopdf.org/downloads.html")
        print("   macOS: brew install wkhtmltopdf")
        print("   Linux: sudo apt-get install wkhtmltopdf")
    
    print()
    
    # Méthode 3: WeasyPrint
    print("📄 Méthode 3: Utilisation de WeasyPrint")
    print("-" * 70)
    
    try:
        from weasyprint import HTML
        print("✅ WeasyPrint est installé")
        try:
            HTML(filename=str(html_file)).write_pdf(str(pdf_file))
            print(f"✅ PDF généré avec succès: {pdf_file}")
            return True
        except Exception as e:
            print(f"❌ Erreur lors de la génération: {e}")
    except ImportError:
        print("❌ WeasyPrint n'est pas installé")
        print("   Installation: pip install weasyprint")
    
    print()
    print("=" * 70)
    print("⚠️  Résumé:")
    print("   - Le fichier HTML est disponible: " + str(html_file))
    print("   - Utilisez la Méthode 1 (navigateur) pour générer le PDF")
    print("   - Ou installez wkhtmltopdf/weasyprint pour automatiser")
    print("=" * 70)
    
    return False


def check_tool_installed(tool_name):
    """Vérifie si un outil en ligne de commande est installé"""
    try:
        subprocess.run([tool_name, '--version'], 
                      stdout=subprocess.DEVNULL, 
                      stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False


def open_html_in_browser():
    """Ouvre simplement le rapport HTML dans le navigateur"""
    html_file = Path('results/Rapport_Complet_Benchmark.html').absolute()
    
    if html_file.exists():
        print(f"📖 Ouverture du rapport: {html_file}")
        webbrowser.open(f'file://{html_file}')
        print("✅ Rapport ouvert dans votre navigateur")
        print()
        print("💡 Pour générer un PDF:")
        print("   Fichier → Imprimer → Enregistrer au format PDF")
    else:
        print(f"❌ Fichier introuvable: {html_file}")
        print("   Exécutez d'abord: python main.py")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--open':
        # Juste ouvrir dans le navigateur
        open_html_in_browser()
    else:
        # Processus complet de génération PDF
        generate_pdf_from_html()
