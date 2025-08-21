# UX Analyzer - SaaS d'analyse UX pour Power Apps

Un SaaS (Software as a Service) spécialement conçu pour analyser l'expérience utilisateur des applications Microsoft Power Apps et fournir des recommandations d'amélioration détaillées.

## 🌟 Fonctionnalités

### Analyse automatisée d'UX
- **Analyse de contraste** : Détection des problèmes de lisibilité
- **Détection d'éléments UI** : Identification des boutons, champs de texte, icônes
- **Évaluation de la densité** : Analyse de la surcharge visuelle
- **Vérification d'accessibilité** : Conformité aux normes WCAG

### Recommandations personnalisées
- **Problèmes de priorité haute** : Contraste insuffisant, accessibilité critique
- **Problèmes de priorité moyenne** : Taille des boutons, complexité de l'interface
- **Optimisations Power Apps** : Conseils spécifiques à la plateforme Microsoft

### Rapports détaillés
- **Analyse visuelle** : Répartition par zones de l'écran
- **Statistiques** : Nombre d'éléments, couleurs dominantes
- **Correctifs actionables** : Instructions précises pour résoudre chaque problème

## 🚀 Démo en ligne

L'application est déployée et accessible à l'adresse suivante :
**[https://xlhyimcl8jvv.manus.space](https://xlhyimcl8jvv.manus.space)**

## 🏗️ Architecture

### Backend (Flask)
- **API REST** : Endpoints pour l'analyse d'images
- **Analyse d'images** : Traitement des captures d'écran Power Apps
- **Base de données** : Stockage des analyses et statistiques
- **CORS** : Support des requêtes cross-origin

### Frontend (React)
- **Interface moderne** : UI construite avec React et Tailwind CSS
- **Upload d'images** : Glisser-déposer et sélection de fichiers
- **Visualisation des résultats** : Affichage interactif des analyses
- **Responsive design** : Compatible desktop et mobile

## 📁 Structure du projet

```
ux-analyzer-project/
├── ux-analyzer-backend/          # API Flask
│   ├── src/
│   │   ├── main.py              # Point d'entrée de l'application
│   │   ├── models/              # Modèles de base de données
│   │   ├── routes/              # Endpoints API
│   │   └── static/              # Fichiers statiques (frontend build)
│   └── requirements.txt         # Dépendances Python
├── ux-analyzer-frontend/         # Interface React
│   ├── src/
│   │   ├── App.jsx             # Composant principal
│   │   ├── components/         # Composants UI
│   │   └── lib/                # Utilitaires
│   ├── package.json            # Dépendances Node.js
│   └── vite.config.js          # Configuration Vite
└── README.md                   # Ce fichier
```

## 🛠️ Installation et développement local

### Prérequis
- Python 3.11+
- Node.js 18+
- pnpm (gestionnaire de paquets)

### Backend (Flask)

1. **Créer un environnement virtuel** :
   ```bash
   cd ux-analyzer-backend
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate     # Windows
   ```

2. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

3. **Lancer le serveur de développement** :
   ```bash
   python src/main.py
   ```
   L'API sera accessible sur `http://localhost:5000`

### Frontend (React)

1. **Installer les dépendances** :
   ```bash
   cd ux-analyzer-frontend
   pnpm install
   ```

2. **Lancer le serveur de développement** :
   ```bash
   pnpm run dev
   ```
   L'interface sera accessible sur `http://localhost:5173`

## 🌐 Déploiement

### Déploiement sur Google Cloud Platform

Le projet inclut un guide détaillé pour le déploiement sur GCP :
- **Cloud Run** pour le backend Flask
- **Cloud Storage** ou **Firebase Hosting** pour le frontend
- **Cloud SQL** pour la base de données

Consultez le fichier `gcp_deployment_guide.md` pour les instructions complètes.

### Déploiement rapide (Manus)

L'application est actuellement déployée sur la plateforme Manus :
- **Backend** : Service Flask avec analyse d'images
- **Frontend** : Application React intégrée
- **URL publique** : [https://xlhyimcl8jvv.manus.space](https://xlhyimcl8jvv.manus.space)

## 📊 API Endpoints

### POST `/api/analyze`
Analyse une capture d'écran d'application Power Apps.

**Paramètres** :
```json
{
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
  "image_name": "power_app_screenshot.png"
}
```

**Réponse** :
```json
{
  "success": true,
  "analysis": {
    "timestamp": "2025-08-21T04:03:17.032955",
    "color_analysis": { ... },
    "element_detection": { ... },
    "recommendations": [ ... ]
  }
}
```

### GET `/api/health`
Vérification de l'état du service.

### GET `/api/stats`
Statistiques globales d'utilisation.

### GET `/api/demo`
Données d'exemple pour tests et démonstration.

## 🎯 Types d'analyses

### Analyse de contraste
- Détection des problèmes de lisibilité
- Calcul des ratios de contraste
- Recommandations WCAG 2.1

### Détection d'éléments UI
- Identification automatique des boutons
- Reconnaissance des champs de texte
- Détection des icônes et conteneurs

### Évaluation de la densité
- Analyse de la surcharge visuelle
- Répartition spatiale des éléments
- Recommandations d'espacement

### Vérifications d'accessibilité
- Conformité aux normes WCAG
- Taille minimale des éléments interactifs
- Contraste des couleurs

## 🔧 Technologies utilisées

### Backend
- **Flask** : Framework web Python
- **Pillow** : Traitement d'images
- **SQLAlchemy** : ORM pour base de données
- **Flask-CORS** : Support CORS

### Frontend
- **React** : Bibliothèque UI
- **Vite** : Build tool moderne
- **Tailwind CSS** : Framework CSS utilitaire
- **Shadcn/ui** : Composants UI modernes
- **Lucide React** : Icônes

## 📝 Utilisation

1. **Accédez à l'application** : [https://xlhyimcl8jvv.manus.space](https://xlhyimcl8jvv.manus.space)

2. **Téléchargez une capture d'écran** de votre application Power Apps

3. **Glissez-déposez l'image** ou utilisez le bouton de sélection

4. **Cliquez sur "Analyser l'image"** et patientez quelques secondes

5. **Consultez les résultats** :
   - Recommandations prioritaires
   - Analyse détaillée des éléments
   - Palette de couleurs
   - Répartition spatiale

6. **Appliquez les correctifs** suggérés dans votre application Power Apps

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Poussez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👨‍💻 Auteur

**Pierre Bournet** - [@pierrebournet](https://github.com/pierrebournet)

## 🙏 Remerciements

- Microsoft Power Apps pour l'inspiration
- La communauté open source pour les outils utilisés
- Les contributeurs et testeurs du projet

---

**🚀 Commencez dès maintenant** : [https://xlhyimcl8jvv.manus.space](https://xlhyimcl8jvv.manus.space)

