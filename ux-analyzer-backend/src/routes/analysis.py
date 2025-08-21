from flask import Blueprint, request, jsonify
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import json
from datetime import datetime
import os
import colorsys
from skimage import measure
from scipy.spatial.distance import euclidean
import pytesseract
from src.models.analysis import Analysis
from src.models.user import db

analysis_bp = Blueprint('analysis', __name__)

class UXAnalyzer:
    def __init__(self):
        self.min_button_size = 44  # Taille minimale recommandée pour les boutons (en pixels)
        self.min_contrast_ratio = 4.5  # Ratio de contraste minimum pour l'accessibilité
        self.max_elements_per_screen = 15  # Nombre maximum d'éléments interactifs recommandé
        
    def analyze_image(self, image_data):
        """Analyse principale d'une image d'application Power Apps"""
        try:
            # Décoder l'image base64
            image_bytes = base64.b64decode(image_data.split(',')[1])
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convertir en format OpenCV
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Effectuer les différentes analyses
            results = {
                'timestamp': datetime.now().isoformat(),
                'image_dimensions': {'width': image.width, 'height': image.height},
                'color_analysis': self._analyze_colors(cv_image),
                'element_detection': self._detect_ui_elements(cv_image),
                'text_analysis': self._analyze_text(cv_image),
                'layout_analysis': self._analyze_layout(cv_image),
                'accessibility_analysis': self._analyze_accessibility(cv_image),
                'recommendations': []
            }
            
            # Générer les recommandations basées sur l'analyse
            results['recommendations'] = self._generate_recommendations(results)
            
            return results
            
        except Exception as e:
            return {'error': f'Erreur lors de l\'analyse: {str(e)}'}
    
    def _analyze_colors(self, image):
        """Analyse des couleurs et des contrastes"""
        # Convertir en RGB pour l'analyse des couleurs
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Extraire les couleurs dominantes
        pixels = rgb_image.reshape(-1, 3)
        unique_colors, counts = np.unique(pixels, axis=0, return_counts=True)
        
        # Trier par fréquence
        sorted_indices = np.argsort(counts)[::-1]
        dominant_colors = unique_colors[sorted_indices[:10]]  # Top 10 couleurs
        
        # Analyser les contrastes
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        contrast_score = np.std(gray)
        
        return {
            'dominant_colors': [color.tolist() for color in dominant_colors],
            'contrast_score': float(contrast_score),
            'color_diversity': len(unique_colors)
        }
    
    def _detect_ui_elements(self, image):
        """Détection des éléments d'interface utilisateur"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Détection des contours pour identifier les éléments
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        elements = []
        for contour in contours:
            # Calculer les propriétés de chaque élément
            area = cv2.contourArea(contour)
            if area > 100:  # Filtrer les petits éléments
                x, y, w, h = cv2.boundingRect(contour)
                
                # Classifier l'élément basé sur ses dimensions
                element_type = self._classify_element(w, h, area)
                
                elements.append({
                    'type': element_type,
                    'position': {'x': int(x), 'y': int(y)},
                    'dimensions': {'width': int(w), 'height': int(h)},
                    'area': float(area)
                })
        
        return {
            'total_elements': len(elements),
            'elements': elements[:20]  # Limiter à 20 éléments pour éviter la surcharge
        }
    
    def _classify_element(self, width, height, area):
        """Classification des éléments UI basée sur leurs dimensions"""
        aspect_ratio = width / height if height > 0 else 0
        
        if width < 50 and height < 50:
            return 'icon'
        elif aspect_ratio > 3:
            return 'text_field'
        elif aspect_ratio < 0.5:
            return 'vertical_element'
        elif 0.8 <= aspect_ratio <= 1.2 and area < 5000:
            return 'button'
        elif area > 10000:
            return 'container'
        else:
            return 'generic_element'
    
    def _analyze_text(self, image):
        """Analyse du texte dans l'image"""
        try:
            # Utiliser OCR pour extraire le texte
            text_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
            
            text_elements = []
            for i in range(len(text_data['text'])):
                if int(text_data['conf'][i]) > 30:  # Confiance minimale
                    text_elements.append({
                        'text': text_data['text'][i],
                        'confidence': int(text_data['conf'][i]),
                        'position': {
                            'x': int(text_data['left'][i]),
                            'y': int(text_data['top'][i])
                        },
                        'dimensions': {
                            'width': int(text_data['width'][i]),
                            'height': int(text_data['height'][i])
                        }
                    })
            
            return {
                'text_elements_count': len(text_elements),
                'text_elements': text_elements[:10]  # Limiter pour la performance
            }
            
        except Exception as e:
            return {
                'text_elements_count': 0,
                'text_elements': [],
                'error': f'Erreur OCR: {str(e)}'
            }
    
    def _analyze_layout(self, image):
        """Analyse de la disposition et de l'alignement"""
        height, width = image.shape[:2]
        
        # Analyser la densité des éléments
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        
        # Calculer la densité par zones
        zones = {
            'top': edges[:height//3, :],
            'middle': edges[height//3:2*height//3, :],
            'bottom': edges[2*height//3:, :],
            'left': edges[:, :width//3],
            'center': edges[:, width//3:2*width//3],
            'right': edges[:, 2*width//3:]
        }
        
        zone_densities = {}
        for zone_name, zone in zones.items():
            density = np.sum(zone > 0) / zone.size
            zone_densities[zone_name] = float(density)
        
        return {
            'image_dimensions': {'width': width, 'height': height},
            'zone_densities': zone_densities,
            'overall_density': float(np.sum(edges > 0) / edges.size)
        }
    
    def _analyze_accessibility(self, image):
        """Analyse de l'accessibilité"""
        # Analyser les contrastes de couleurs
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Calculer le contraste moyen
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        contrast_variance = np.var(gray)
        
        # Détecter les zones de faible contraste
        low_contrast_areas = []
        
        # Diviser l'image en blocs pour analyser le contraste local
        h, w = gray.shape
        block_size = 50
        
        for y in range(0, h - block_size, block_size):
            for x in range(0, w - block_size, block_size):
                block = gray[y:y+block_size, x:x+block_size]
                local_contrast = np.std(block)
                
                if local_contrast < 20:  # Seuil de faible contraste
                    low_contrast_areas.append({
                        'position': {'x': x, 'y': y},
                        'contrast_score': float(local_contrast)
                    })
        
        return {
            'overall_contrast_variance': float(contrast_variance),
            'low_contrast_areas_count': len(low_contrast_areas),
            'low_contrast_areas': low_contrast_areas[:10]  # Limiter pour la performance
        }
    
    def _generate_recommendations(self, analysis_results):
        """Génération des recommandations basées sur l'analyse"""
        recommendations = []
        
        # Recommandations basées sur l'analyse des couleurs
        color_analysis = analysis_results.get('color_analysis', {})
        if color_analysis.get('contrast_score', 0) < 30:
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
        
        # Vérifier la taille des boutons
        for element in element_analysis.get('elements', []):
            if element['type'] == 'button':
                width = element['dimensions']['width']
                height = element['dimensions']['height']
                if width < self.min_button_size or height < self.min_button_size:
                    recommendations.append({
                        'type': 'button_size',
                        'severity': 'medium',
                        'title': 'Bouton trop petit',
                        'description': f'Un bouton de taille {width}x{height}px est trop petit pour une interaction tactile confortable.',
                        'suggestion': f'Augmentez la taille du bouton à au moins {self.min_button_size}x{self.min_button_size}px.',
                        'fix': f'Redimensionnez le bouton situé en position ({element["position"]["x"]}, {element["position"]["y"]}).',
                        'position': element['position']
                    })
        
        # Recommandations basées sur l'analyse de layout
        layout_analysis = analysis_results.get('layout_analysis', {})
        if layout_analysis.get('overall_density', 0) > 0.3:
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
        if accessibility_analysis.get('low_contrast_areas_count', 0) > 5:
            recommendations.append({
                'type': 'accessibility',
                'severity': 'high',
                'title': 'Problèmes d\'accessibilité détectés',
                'description': f'{accessibility_analysis.get("low_contrast_areas_count")} zones avec un contraste insuffisant ont été détectées.',
                'suggestion': 'Améliorez le contraste dans les zones identifiées pour respecter les normes d\'accessibilité WCAG.',
                'fix': 'Modifiez les couleurs dans les zones problématiques pour atteindre un ratio de contraste d\'au moins 4.5:1.'
            })
        
        return recommendations

# Instance globale de l'analyseur
analyzer = UXAnalyzer()

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
        
        # Sauvegarder l'analyse en base de données
        try:
            analysis = Analysis(results, data.get('image_name', 'screenshot'))
            db.session.add(analysis)
            db.session.commit()
            
            # Ajouter l'ID de l'analyse aux résultats
            results['analysis_id'] = analysis.id
            
        except Exception as db_error:
            print(f"Erreur de sauvegarde en base: {str(db_error)}")
            # Continuer même si la sauvegarde échoue
        
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



@analysis_bp.route('/analyses', methods=['GET'])
def get_analyses():
    """Récupérer la liste des analyses récentes"""
    try:
        limit = request.args.get('limit', 10, type=int)
        analyses = Analysis.get_recent_analyses(limit)
        
        return jsonify({
            'success': True,
            'analyses': [analysis.to_dict() for analysis in analyses]
        })
        
    except Exception as e:
        return jsonify({'error': f'Erreur serveur: {str(e)}'}), 500

@analysis_bp.route('/analyses/<int:analysis_id>', methods=['GET'])
def get_analysis(analysis_id):
    """Récupérer une analyse spécifique par son ID"""
    try:
        analysis = Analysis.get_analysis_by_id(analysis_id)
        
        if not analysis:
            return jsonify({'error': 'Analyse non trouvée'}), 404
        
        return jsonify({
            'success': True,
            'analysis': analysis.to_dict()
        })
        
    except Exception as e:
        return jsonify({'error': f'Erreur serveur: {str(e)}'}), 500

@analysis_bp.route('/stats', methods=['GET'])
def get_stats():
    """Récupérer les statistiques globales"""
    try:
        total_analyses = Analysis.query.count()
        
        if total_analyses == 0:
            return jsonify({
                'success': True,
                'stats': {
                    'total_analyses': 0,
                    'avg_issues_per_analysis': 0,
                    'most_common_issue_types': []
                }
            })
        
        # Calculer la moyenne des problèmes par analyse
        analyses = Analysis.query.all()
        total_issues = sum(analysis.total_issues for analysis in analyses)
        avg_issues = total_issues / total_analyses if total_analyses > 0 else 0
        
        # Compter les types de problèmes les plus fréquents
        issue_types = {}
        for analysis in analyses:
            recommendations = json.loads(analysis.recommendations) if analysis.recommendations else []
            for rec in recommendations:
                issue_type = rec.get('type', 'unknown')
                issue_types[issue_type] = issue_types.get(issue_type, 0) + 1
        
        # Trier par fréquence
        most_common = sorted(issue_types.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return jsonify({
            'success': True,
            'stats': {
                'total_analyses': total_analyses,
                'avg_issues_per_analysis': round(avg_issues, 2),
                'most_common_issue_types': [{'type': t, 'count': c} for t, c in most_common]
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Erreur serveur: {str(e)}'}), 500

