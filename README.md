# Application Graphique de Descente de Gradient pour la Régression et la Classification

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-learn">
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas">
  <img src="https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge&logo=matplotlib&logoColor=white" alt="Matplotlib">
  <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
</p>

---

## 🌟 Vue d'ensemble du Projet

Bienvenue dans notre projet innovant ! Cette application graphique est conçue pour démystifier l'algorithme de **Descente de Gradient (Gradient Descent)**, le rendant accessible et intuitif pour tous, des débutants aux experts en apprentissage automatique. Que ce soit pour la **régression** ou la **classification**, notre outil offre une interface conviviale pour explorer, préparer, entraîner et visualiser les performances des modèles de machine learning.

**L'objectif principal** est de fournir une plateforme interactive où les utilisateurs peuvent télécharger leurs propres datasets, effectuer un prétraitement des données, appliquer l'algorithme de Descente de Gradient, et ajuster ses paramètres pour observer instantanément l'impact sur la performance du modèle.

---

## ✨ Fonctionnalités Clés

Notre application est dotée des capacités suivantes, conçues pour une expérience utilisateur optimale :

* **📤 Téléchargement de Dataset (Upload) :** Importez facilement vos fichiers de données (CSV, Excel, etc.) pour commencer votre analyse.
* **📊 Tableau de Bord Statistique :** Obtenez une vue d'ensemble rapide de votre dataset avec des statistiques descriptives et des visualisations clés.
* **🧹 Prétraitement des Données :** Des outils intégrés pour nettoyer et préparer vos données (gestion des valeurs manquantes, mise à l'échelle, encodage des variables catégorielles).
* **🧠 Application de la Descente de Gradient :** Entraînez des modèles de régression et de classification basés sur l'algorithme de Descente de Gradient.
* **📈 Visualisation de la Performance :** Mesurez et visualisez l'exactitude (accuracy) et d'autres métriques de performance de votre modèle en temps réel.
* **⚙️ Ajustement des Paramètres (Hyperparamètres) :** Modifiez le taux d'apprentissage ($\alpha$), le nombre d'itérations, et observez l'impact sur la courbe d'apprentissage et la performance.
* **🎨 Design Intuitif & Conception Robuste :** Une interface utilisateur pensée pour la facilité d'utilisation et une architecture backend solide pour des traitements efficaces.

---

## 🏛️ Architecture du Projet

Notre application est construite sur le puissant framework web **Django**, suivant une architecture client-serveur classique pour garantir scalabilité et performance.

**Schéma Conceptuel (À remplacer par une image réelle ou un diagramme Mermaid.js):**
```mermaid
graph TD
    A[Navigateur Utilisateur] -->|Requêtes HTTP / AJAX| B(Application Django)
    B -->|Frontend (HTML, CSS, JS)| A
    B -->|Backend (Python)| C(Logiciel de Traitement des Données)
    B -->|Backend (Python)| D(Logiciel d'Apprentissage Automatique)
    C -->|Utilise Pandas| E(Dataset Téléchargé)
    D -->|Utilise Scikit-learn| E
    D -->|Utilise Matplotlib/Chart.js| F(Visualisations)
    B -->|Interagit avec| G(Base de Données - SQLite par défaut)