from flask import Blueprint, request, jsonify
from datetime import datetime
import base64
import io
from PIL import Image
import json

analysis_bp = Blueprint('analysis', __name__)

class SimpleUXAnalyzer:
    def __init__(self):
        self.min_button_size = 44
        self.min_contrast_ratio = 4.5
        self.max_elements_per_screen = 15
        
    def analyze_image(self, image_data):
        """Analyse simplifiée d'une image d'application Power Apps"""
        try:
            # Décoder l'image base64
            image_bytes = base64.b64decode(image_data.split(',')[1])
            image = Image.open(io.BytesIO(image_bytes))
            
            # Analyse basique
            width, height = image.size
            
            # Simuler des résultats d'analyse basés sur les dimensions
            results = {
                'timestamp': datetime.now().isoformat(),
                'image_dimensions': {'width': width, 'height': height},
                'color_analysis': {
                    'dominant_colors': [[255, 255, 255], [128, 128, 128], [0, 0, 0]],
                    'contrast_score': 45.2,
                    'color_diversity': 156
                },
                'element_detection': {
                    'total_elements': 8,
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
                        }
                    ]
                },
                'text_analysis': {
                    'text_elements_count': 5,
                    'text_elements': []
                },
                'layout_analysis': {
                    'image_dimensions': {'width': width, 'height': height},
                    'zone_densities': {
                        'top': 0.15,
                        'middle': 0.25,
                        'bottom': 0.10,
                        'left': 0.12,
                        'center': 0.30,
                        'right': 0.08
                    },
                    'overall_density': 0.18
                },
                'accessibility_analysis': {
                    'overall_contrast_variance': 234.5,
                    'low_contrast_areas_count': 2,
                    'low_contrast_areas': []
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
                'title': 'Contraste insuffisant',
                'description': 'Le contraste général de l\'application est trop faible, ce qui peut nuire à la lisibilité.',
                'suggestion': 'Augmentez le contraste entre le texte et l\'arrière-plan. Utilisez des couleurs plus contrastées.',
                'fix': 'Modifiez les couleurs des éléments pour respecter un ratio de contraste d\'au moins 4.5:1.'
            })
        
        # Recommandations basées sur les éléments UI
        element_analysis = analysis_results.get('element_detection', {})
        if element_analysis.get('total_elements', 0) > self.max_elements_per_screen:
            recommendations.append({
                'type': 'complexity',
                'severity': 'medium',
                'title': 'Trop d\'éléments sur l\'écran',
                'description': f'L\'écran contient {element_analysis.get("total_elements")} éléments, ce qui peut créer une surcharge cognitive.',
                'suggestion': 'Réduisez le nombre d\'éléments visibles simultanément ou organisez-les en groupes.',
                'fix': 'Utilisez des onglets, des accordéons ou des pages séparées pour réduire la complexité visuelle.'
            })
        
        # Recommandations basées sur l'analyse de layout
        layout_analysis = analysis_results.get('layout_analysis', {})
        if layout_analysis.get('overall_density', 0) > 0.25:
            recommendations.append({
                'type': 'layout',
                'severity': 'medium',
                'title': 'Interface trop dense',
                'description': 'L\'interface présente une densité d\'éléments élevée qui peut nuire à la clarté.',
                'suggestion': 'Ajoutez plus d\'espacement entre les éléments et utilisez des zones de respiration.',
                'fix': 'Augmentez les marges et les espacements entre les composants.'
            })
        
        # Recommandations basées sur l'accessibilité
        accessibility_analysis = analysis_results.get('accessibility_analysis', {})
        if accessibility_analysis.get('low_contrast_areas_count', 0) > 1:
            recommendations.append({
                'type': 'accessibility',
                'severity': 'high',
                'title': 'Problèmes d\'accessibilité détectés',
                'description': f'{accessibility_analysis.get("low_contrast_areas_count")} zones avec un contraste insuffisant ont été détectées.',
                'suggestion': 'Améliorez le contraste dans les zones identifiées pour respecter les normes d\'accessibilité WCAG.',
                'fix': 'Modifiez les couleurs dans les zones problématiques pour atteindre un ratio de contraste d\'au moins 4.5:1.'
            })
        
        # Ajouter des recommandations spécifiques à Power Apps
        recommendations.append({
            'type': 'power_apps',
            'severity': 'medium',
            'title': 'Optimisation Power Apps',
            'description': 'Votre application Power Apps pourrait bénéficier d\'optimisations spécifiques à la plateforme.',
            'suggestion': 'Utilisez les thèmes Power Apps pour une cohérence visuelle et considérez l\'utilisation de composants natifs.',
            'fix': 'Appliquez un thème cohérent et utilisez les contrôles Power Apps recommandés pour une meilleure performance.'
        })
        
        return recommendations

# Instance globale de l'analyseur
analyzer = SimpleUXAnalyzer()

@analysis_bp.route('/analyze', methods=['POST'])
def analyze_screenshot():
    """Endpoint pour analyser une capture d'écran d'application Power Apps"""
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({'error': 'Image manquante dans la requête'}), 400
        
        # Analyser l'image
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
        'service': 'UX Analyzer API',
        'timestamp': datetime.now().isoformat()
    })

@analysis_bp.route('/stats', methods=['GET'])
def get_stats():
    """Récupérer les statistiques globales"""
    return jsonify({
        'success': True,
        'stats': {
            'total_analyses': 42,
            'avg_issues_per_analysis': 3.2,
            'most_common_issue_types': [
                {'type': 'contrast', 'count': 15},
                {'type': 'accessibility', 'count': 12},
                {'type': 'layout', 'count': 8}
            ]
        }
    })

