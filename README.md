# 🚀 Application Graphique d'Algorithme de Descente de Gradient 🚀

## Un Outil Intuitif pour la Régression et la Classification

Bienvenue sur le dépôt GitHub de notre projet de Master ! Cette application web innovante, développée avec Django, vise à démystifier l'algorithme de Descente de Gradient (Gradient Descent) en offrant une interface utilisateur graphique et intuitive. Que vous soyez un débutant, un amateur ou un expert en Machine Learning, notre outil rendra l'analyse et la modélisation prédictive accessibles à tous.

---

## ✨ Fonctionnalités Clés de l'Application ✨

Notre application est conçue pour être une solution complète et conviviale pour l'exploration de données et l'apprentissage automatique :

1.  **Téléchargement de Dataset Simplifié** 📥
    * Uploadez vos propres fichiers de données (CSV, Excel, etc.) en toute simplicité.
    * Interface utilisateur claire et directe pour une prise en main rapide.

2.  **Tableau de Bord Intuitif (Dashboard)** 📊
    * Affichez des statistiques descriptives complètes de votre dataset.
    * Obtenez un aperçu rapide de la structure de vos données, des valeurs manquantes, des types de colonnes, etc.

3.  **Prétraitement de Données (Preprocessing)** 🧹
    * Gérez les valeurs manquantes (imputation).
    * Mettez à l'échelle vos caractéristiques numériques (Standardization, Normalization).
    * Encodez vos données catégorielles (One-Hot Encoding, Label Encoding).
    * Contrôlez ces opérations via une interface interactive.

4.  **Application de l'Algorithme de Descente de Gradient** 🧠
    * Appliquez l'algorithme de Descente de Gradient pour des tâches de Régression (par ex., Régression Linéaire) et de Classification (par ex., Régression Logistique).
    * Utilisation de la puissance de `scikit-learn` pour une implémentation robuste.

5.  **Visualisation de la Performance du Modèle** 📈
    * Affichez des métriques de performance claires (Accuracy, Precision, Recall, F1-score, RMSE, R-squared).
    * Visualisez la Matrice de Confusion pour une compréhension approfondie de la performance du classifieur.

6.  **Ajustement des Paramètres Intuitif** 🛠️
    * Modifiez facilement le **taux d'apprentissage ($\alpha$)** et le **nombre d'itérations**.
    * Observez l'impact de ces changements en temps réel grâce à la **courbe d'apprentissage (Learning Curve)**.
    * Optimisez la performance de votre modèle de manière interactive.

---

## 🛠️ Technologies Utilisées 🛠️

Notre projet s'appuie sur un stack technologique moderne et robuste pour garantir performance et flexibilité.

* **Backend (Logique Serveur & ML) :**
    * **Python** (Langage de programmation principal)
        * `![Python Logo](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)` (Lien symbolique, remplacez par votre image si vous en avez une)
    * **Django** (Framework Web pour le Backend)
        * `![Django Logo](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)` (Lien symbolique)
    * **scikit-learn** (Bibliothèque Machine Learning)
        * `![Scikit-learn Logo](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)` (Lien symbolique)
    * **Pandas** (Manipulation et Analyse de Données)
        * `![Pandas Logo](https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)` (Lien symbolique)
    * **NumPy** (Calcul Numérique)
        * `![NumPy Logo](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)` (Lien symbolique)
    * **Matplotlib** (Visualisation de Données, pour la génération côté serveur si besoin)
        * `![Matplotlib Logo](https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge&logo=matplotlib&logoColor=white)` (Lien symbolique)

* **Frontend (Interface Utilisateur) :**
    * **HTML5** (Structure des Pages Web)
        * `![HTML5 Logo](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)` (Lien symbolique)
    * **CSS3** (Style et Mise en Page)
        * `![CSS3 Logo](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)` (Lien symbolique)
    * **JavaScript** (Interactivité Côté Client)
        * `![JavaScript Logo](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)` (Lien symbolique)
    * **Bootstrap / Tailwind CSS** (Frameworks CSS pour un Design Responsive et Moderne)
        * `![Bootstrap Logo](https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)` (Lien symbolique)
    * **Chart.js / Plotly.js** (Bibliothèques JS pour des Graphiques Interactifs)
        * `![Chart.js Logo](https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chart.js&logoColor=white)` (Lien symbolique)

---

## 👥 Équipe de Développement 👥

Ce projet a été développé par une équipe passionnée et complémentaire :

* **Mohammed** (Expert Frontend & Gestion de Données) 🎨
    * `![Mohammed Photo](https://via.placeholder.com/150/0000FF/FFFFFF?text=Mohammed)` (Lien symbolique - Remplacer par une photo ou un avatar réel)
    * Spécialisé dans la conception d'interfaces utilisateur intuitives et l'intégration de données avec Django.
* **Amad** (Expert Mathématiques & Logique ML) 🧠
    * `![Amad Photo](https://via.placeholder.com/150/FF0000/FFFFFF?text=Amad)` (Lien symbolique - Remplacer par une photo ou un avatar réel)
    * Force vive derrière l'implémentation de l'algorithme de Descente de Gradient et l'optimisation des modèles.

---

## 🚀 Comment Démarrer le Projet (pour les Développeurs) 🚀

Suivez ces étapes simples pour configurer et exécuter le projet en local :

1.  **Cloner le dépôt :**
    ```bash
    git clone [https://github.com/votre_utilisateur/votre_projet.git](https://github.com/votre_utilisateur/votre_projet.git)
    cd votre_projet
    ```

2.  **Créer et activer l'environnement virtuel :**
    ```bash
    python -m venv venv
    # Sur Windows
    .\venv\Scripts\activate
    # Sur macOS/Linux
    source venv/bin/activate
    ```

3.  **Installer les dépendances :**
    ```bash
    pip install -r requirements.txt
    ```
    *(Assurez-vous de générer un fichier `requirements.txt` avec `pip freeze > requirements.txt`)*

4.  **Appliquer les migrations Django :**
    ```bash
    python manage.py migrate
    ```

5.  **Lancer le serveur de développement :**
    ```bash
    python manage.py runserver
    ```

L'application sera accessible dans votre navigateur à l'adresse : `http://127.0.0.1:8000/`

---

## 🗺️ Aperçu de la Feuille de Route du Projet 🗺️

Pour une compréhension claire de notre approche structurée, voici un aperçu de nos phases de développement :

* **Phase 0: ⚙️ Configuration Initiale**
    * Installation des outils, configuration de l'environnement, mise en place de Git.
    * *Mohammed & Amad (Collaboration Totale)*
* **Phase 1: ⬆️ Téléchargement des Données**
    * Développement de l'interface d'upload et de la logique de lecture des fichiers.
    * *Mohammed (Frontend), Amad (Backend Support & ML Research)*
* **Phase 2: 🔍 Exploration & Prétraitement**
    * Affichage du Dashboard des statistiques et implémentation des options de preprocessing.
    * *Mohammed (Frontend Dashboard), Amad (Backend Preprocessing Logic)*
* **Phase 3: 🧠 Entraînement du Modèle ML**
    * Intégration de l'algorithme de Descente de Gradient et calcul des métriques de performance initiales.
    * *Mohammed (Frontend ML Config), Amad (Core ML Logic & Training)*
* **Phase 4: 📊 Ajustement & Visualisation**
    * Mise en place des contrôles de paramètres et de la courbe d'apprentissage interactive.
    * *Mohammed (Frontend Interactivité), Amad (Backend Data for Visuals)*
* **Phase 5: ✅ Finalisation & Présentation**
    * Tests complets, optimisation, préparation de la présentation finale.
    * *Mohammed & Amad (Collaboration Totale)*

---

## 🤝 Contribution 🤝

Nous apprécions toutes les contributions à ce projet ! Si vous souhaitez contribuer, veuillez suivre les étapes suivantes :

1.  Faire un "fork" de ce dépôt.
2.  Créer une nouvelle branche pour votre fonctionnalité (`git checkout -b feature/nouvelle-fonctionnalite`).
3.  Effectuer vos modifications et les commiter (`git commit -m 'Ajout d'une nouvelle fonctionnalité'`).
4.  Pousser (push) votre branche (`git git push origin feature/nouvelle-fonctionnalite`).
5.  Ouvrir une "Pull Request" (PR) pour que nous puissions examiner vos modifications.

---

## 📜 Licence 📜

Ce projet est sous licence MIT. Pour plus de détails, consultez le fichier `LICENSE`.

---

**N'hésitez pas à explorer et à expérimenter avec notre application ! Votre feedback est précieux.**