from flask import Blueprint, request, jsonify
from datetime import datetime
import base64
import json

analysis_bp = Blueprint('analysis', __name__)

class MinimalUXAnalyzer:
    def __init__(self):
        self.min_button_size = 44
        self.min_contrast_ratio = 4.5
        self.max_elements_per_screen = 15
        
    def analyze_image(self, image_data):
        """Analyse minimale d'une image d'application Power Apps"""
        try:
            # Simuler l'analyse d'image sans traitement réel
            # En production, ceci serait remplacé par une vraie analyse d'image
            
            results = {
                'timestamp': datetime.now().isoformat(),
                'image_dimensions': {'width': 1024, 'height': 768},
                'color_analysis': {
                    'dominant_colors': [
                        [255, 255, 255],  # Blanc
                        [128, 128, 128],  # Gris
                        [0, 0, 0],        # Noir
                        [74, 144, 226],   # Bleu Power Apps
                        [242, 242, 242]   # Gris clair
                    ],
                    'contrast_score': 42.8,
                    'color_diversity': 156
                },
                'element_detection': {
                    'total_elements': 12,
                    'elements': [
                        {
                            'type': 'button',
                            'position': {'x': 100, 'y': 200},
                            'dimensions': {'width': 120, 'height': 40},
                            'area': 4800
                        },
                        {
                            'type': 'text_field',
                            'position': {'x': 50, 'y': 100},
                            'dimensions': {'width': 200, 'height': 30},
                            'area': 6000
                        },
                        {
                            'type': 'icon',
                            'position': {'x': 300, 'y': 150},
                            'dimensions': {'width': 24, 'height': 24},
                            'area': 576
                        },
                        {
                            'type': 'container',
                            'position': {'x': 20, 'y': 50},
                            'dimensions': {'width': 400, 'height': 300},
                            'area': 120000
                        }
                    ]
                },
                'text_analysis': {
                    'text_elements_count': 8,
                    'text_elements': [
                        {
                            'text': 'Import components',
                            'confidence': 95,
                            'position': {'x': 425, 'y': 27},
                            'dimensions': {'width': 150, 'height': 20}
                        },
                        {
                            'text': 'Canvas',
                            'confidence': 98,
                            'position': {'x': 443, 'y': 66},
                            'dimensions': {'width': 60, 'height': 16}
                        }
                    ]
                },
                'layout_analysis': {
                    'image_dimensions': {'width': 1024, 'height': 768},
                    'zone_densities': {
                        'top': 0.22,
                        'middle': 0.35,
                        'bottom': 0.18,
                        'left': 0.25,
                        'center': 0.40,
                        'right': 0.15
                    },
                    'overall_density': 0.26
                },
                'accessibility_analysis': {
                    'overall_contrast_variance': 189.3,
                    'low_contrast_areas_count': 3,
                    'low_contrast_areas': [
                        {
                            'position': {'x': 100, 'y': 200},
                            'contrast_score': 18.5
                        },
                        {
                            'position': {'x': 300, 'y': 400},
                            'contrast_score': 15.2
                        }
                    ]
                },
                'recommendations': []
            }
            
            # Générer des recommandations basées sur l'analyse
            results['recommendations'] = self._generate_recommendations(results)
            
            return results
            
        except Exception as e:
            return {'error': f'Erreur lors de l\'analyse: {str(e)}'}
    
    def _generate_recommendations(self, analysis_results):
        """Génération des recommandations basées sur l'analyse"""
        recommendations = []
        
        # Recommandations basées sur l'analyse des couleurs
        color_analysis = analysis_results.get('color_analysis', {})
        if color_analysis.get('contrast_score', 0) < 50:
            recommendations.append({
                'type': 'contrast',
                'severity': 'high',
                'title': 'Contraste insuffisant détecté',
                'description': 'Le contraste général de l\'application est de {:.1f}, ce qui est en dessous du seuil recommandé de 50 pour une bonne lisibilité.'.format(color_analysis.get('contrast_score', 0)),
                'suggestion': 'Augmentez le contraste entre le texte et l\'arrière-plan. Utilisez des couleurs plus contrastées pour améliorer la lisibilité.',
                'fix': 'Modifiez les couleurs des éléments pour respecter un ratio de contraste d\'au moins 4.5:1 selon les normes WCAG.'
            })
        
        # Recommandations basées sur les éléments UI
        element_analysis = analysis_results.get('element_detection', {})
        if element_analysis.get('total_elements', 0) > self.max_elements_per_screen:
            recommendations.append({
                'type': 'complexity',
                'severity': 'medium',
                'title': 'Interface surchargée',
                'description': f'L\'écran contient {element_analysis.get("total_elements")} éléments interactifs, ce qui dépasse la limite recommandée de {self.max_elements_per_screen} éléments.',
                'suggestion': 'Réduisez le nombre d\'éléments visibles simultanément ou organisez-les en groupes logiques.',
                'fix': 'Utilisez des onglets, des accordéons ou divisez le contenu en plusieurs écrans pour réduire la complexité visuelle.'
            })
        
        # Vérifier la taille des boutons
        small_buttons = []
        for element in element_analysis.get('elements', []):
            if element['type'] == 'button':
                width = element['dimensions']['width']
                height = element['dimensions']['height']
                if width < self.min_button_size or height < self.min_button_size:
                    small_buttons.append(element)
        
        if small_buttons:
            recommendations.append({
                'type': 'button_size',
                'severity': 'medium',
                'title': 'Boutons trop petits détectés',
                'description': f'{len(small_buttons)} bouton(s) sont plus petits que la taille recommandée de {self.min_button_size}x{self.min_button_size}px.',
                'suggestion': f'Augmentez la taille des boutons pour faciliter l\'interaction tactile, surtout sur mobile.',
                'fix': f'Redimensionnez les boutons pour qu\'ils mesurent au moins {self.min_button_size}x{self.min_button_size}px.'
            })
        
        # Recommandations basées sur l'analyse de layout
        layout_analysis = analysis_results.get('layout_analysis', {})
        if layout_analysis.get('overall_density', 0) > 0.25:
            recommendations.append({
                'type': 'layout',
                'severity': 'medium',
                'title': 'Densité d\'interface élevée',
                'description': f'L\'interface présente une densité de {layout_analysis.get("overall_density", 0):.1%}, ce qui peut nuire à la clarté.',
                'suggestion': 'Ajoutez plus d\'espacement entre les éléments et utilisez des zones de respiration (whitespace).',
                'fix': 'Augmentez les marges et les espacements entre les composants pour améliorer la lisibilité.'
            })
        
        # Recommandations basées sur l'accessibilité
        accessibility_analysis = analysis_results.get('accessibility_analysis', {})
        if accessibility_analysis.get('low_contrast_areas_count', 0) > 2:
            recommendations.append({
                'type': 'accessibility',
                'severity': 'high',
                'title': 'Problèmes d\'accessibilité critiques',
                'description': f'{accessibility_analysis.get("low_contrast_areas_count")} zones avec un contraste insuffisant ont été détectées.',
                'suggestion': 'Améliorez le contraste dans les zones identifiées pour respecter les normes d\'accessibilité WCAG 2.1.',
                'fix': 'Modifiez les couleurs dans les zones problématiques pour atteindre un ratio de contraste d\'au moins 4.5:1.'
            })
        
        # Recommandations spécifiques à Power Apps
        recommendations.append({
            'type': 'power_apps_optimization',
            'severity': 'low',
            'title': 'Optimisations Power Apps recommandées',
            'description': 'Votre application Power Apps pourrait bénéficier d\'optimisations spécifiques à la plateforme Microsoft.',
            'suggestion': 'Utilisez les thèmes Power Apps natifs et les composants recommandés pour une meilleure cohérence.',
            'fix': 'Appliquez un thème Power Apps cohérent et privilégiez les contrôles natifs pour optimiser les performances.'
        })
        
        # Recommandation sur la navigation
        if element_analysis.get('total_elements', 0) > 8:
            recommendations.append({
                'type': 'navigation',
                'severity': 'low',
                'title': 'Navigation à optimiser',
                'description': 'Avec plusieurs éléments sur l\'écran, la navigation pourrait être simplifiée.',
                'suggestion': 'Organisez les éléments en groupes logiques et ajoutez des indicateurs visuels pour guider l\'utilisateur.',
                'fix': 'Utilisez des séparateurs visuels, des groupes de contrôles et une hiérarchie claire pour améliorer la navigation.'
            })
        
        return recommendations

# Instance globale de l'analyseur
analyzer = MinimalUXAnalyzer()

@analysis_bp.route('/analyze', methods=['POST'])
def analyze_screenshot():
    """Endpoint pour analyser une capture d'écran d'application Power Apps"""
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({'error': 'Image manquante dans la requête'}), 400
        
        # Analyser l'image (simulation)
        results = analyzer.analyze_image(data['image'])
        
        if 'error' in results:
            return jsonify(results), 500
        
        return jsonify({
            'success': True,
            'analysis': results
        })
        
    except Exception as e:
        return jsonify({'error': f'Erreur serveur: {str(e)}'}), 500

@analysis_bp.route('/health', methods=['GET'])
def health_check():
    """Endpoint de vérification de l'état du service"""
    return jsonify({
        'status': 'healthy',
        'service': 'UX Analyzer API - Power Apps Edition',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat(),
        'features': [
            'Analyse de contraste',
            'Détection d\'éléments UI',
            'Recommandations d\'accessibilité',
            'Optimisations Power Apps'
        ]
    })

@analysis_bp.route('/stats', methods=['GET'])
def get_stats():
    """Récupérer les statistiques globales (simulées)"""
    return jsonify({
        'success': True,
        'stats': {
            'total_analyses': 127,
            'avg_issues_per_analysis': 4.2,
            'most_common_issue_types': [
                {'type': 'contrast', 'count': 45, 'percentage': 35.4},
                {'type': 'accessibility', 'count': 38, 'percentage': 29.9},
                {'type': 'button_size', 'count': 22, 'percentage': 17.3},
                {'type': 'layout', 'count': 15, 'percentage': 11.8},
                {'type': 'complexity', 'count': 7, 'percentage': 5.5}
            ],
            'avg_resolution': {'width': 1024, 'height': 768},
            'platform_insights': {
                'power_apps_specific_issues': 23,
                'mobile_compatibility_score': 78.5,
                'accessibility_compliance': 82.3
            }
        }
    })

@analysis_bp.route('/demo', methods=['GET'])
def demo_analysis():
    """Endpoint de démonstration avec des données d'exemple"""
    demo_result = {
        'success': True,
        'analysis': {
            'timestamp': datetime.now().isoformat(),
            'image_dimensions': {'width': 1047, 'height': 464},
            'color_analysis': {
                'dominant_colors': [[255, 255, 255], [74, 144, 226], [128, 128, 128]],
                'contrast_score': 38.5,
                'color_diversity': 89
            },
            'element_detection': {
                'total_elements': 16,
                'elements': [
                    {'type': 'button', 'position': {'x': 450, 'y': 320}, 'dimensions': {'width': 80, 'height': 32}},
                    {'type': 'text_field', 'position': {'x': 170, 'y': 180}, 'dimensions': {'width': 180, 'height': 28}}
                ]
            },
            'recommendations': [
                {
                    'type': 'contrast',
                    'severity': 'high',
                    'title': 'Contraste insuffisant détecté',
                    'description': 'Le contraste général de l\'application est de 38.5, ce qui est en dessous du seuil recommandé.',
                    'suggestion': 'Augmentez le contraste entre le texte et l\'arrière-plan.',
                    'fix': 'Modifiez les couleurs pour respecter un ratio de contraste d\'au moins 4.5:1.'
                },
                {
                    'type': 'complexity',
                    'severity': 'medium',
                    'title': 'Interface surchargée',
                    'description': 'L\'écran contient 16 éléments interactifs, ce qui dépasse la limite recommandée.',
                    'suggestion': 'Organisez les éléments en groupes logiques.',
                    'fix': 'Utilisez des onglets ou divisez le contenu en plusieurs écrans.'
                }
            ]
        }
    }
    
    return jsonify(demo_result)

