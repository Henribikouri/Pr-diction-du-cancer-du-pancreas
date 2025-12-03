# 🩺 Projet d'Analyse et de Prédiction des Maladies du Pancréas

## Introduction

Ce projet est une application web basée sur **Django** et **Django REST Framework (DRF)**, conçue pour intégrer et servir un modèle de **Machine Learning** spécialisé dans la prédiction de maladies du pancréas. L'objectif est de fournir une interface et une API pour faciliter l'analyse précoce et le support à la décision clinique.

## Technologies Utilisées

| Catégorie | Outil / Bibliothèque | Rôle dans le Projet |
| :--- | :--- | :--- |
| **Backend Web** | Python, **Django** | Fournit la structure MVC (MTV dans Django) et le serveur de développement. |
| **API** | **Django REST Framework** | Crée les points de terminaison RESTful pour communiquer avec le modèle ML. |
| **HTTP Requests** | **Requests** | Utilisé dans le module `image_processing/signals.py` pour effectuer des requêtes web. |
| **ML/Data** | Scikit-learn, TensorFlow/Keras, Pandas... | Cadre pour la construction et l'inférence des modèles de prédiction. |

---

## 🚀 Démarrage et Installation (Guide Complet)

Suivez ces étapes pour configurer et exécuter l'application sur votre machine locale.

### 1. Cloner le Dépôt

Récupérez le code source depuis GitHub :

```bash
git clone https://github.com/Henribikouri/Pr-diction-du-cancer-du-pancreas.git
cd health_system
