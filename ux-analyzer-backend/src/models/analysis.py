from src.models.user import db
from datetime import datetime
import json

class Analysis(db.Model):
    """Modèle pour stocker les analyses UX"""
    __tablename__ = 'analyses'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    image_name = db.Column(db.String(255), nullable=True)
    image_dimensions = db.Column(db.Text, nullable=True)  # JSON string
    
    # Résultats d'analyse stockés en JSON
    color_analysis = db.Column(db.Text, nullable=True)
    element_detection = db.Column(db.Text, nullable=True)
    text_analysis = db.Column(db.Text, nullable=True)
    layout_analysis = db.Column(db.Text, nullable=True)
    accessibility_analysis = db.Column(db.Text, nullable=True)
    recommendations = db.Column(db.Text, nullable=True)
    
    # Métadonnées
    total_issues = db.Column(db.Integer, default=0)
    severity_high = db.Column(db.Integer, default=0)
    severity_medium = db.Column(db.Integer, default=0)
    severity_low = db.Column(db.Integer, default=0)
    
    def __init__(self, analysis_data, image_name=None):
        self.image_name = image_name
        self.image_dimensions = json.dumps(analysis_data.get('image_dimensions', {}))
        self.color_analysis = json.dumps(analysis_data.get('color_analysis', {}))
        self.element_detection = json.dumps(analysis_data.get('element_detection', {}))
        self.text_analysis = json.dumps(analysis_data.get('text_analysis', {}))
        self.layout_analysis = json.dumps(analysis_data.get('layout_analysis', {}))
        self.accessibility_analysis = json.dumps(analysis_data.get('accessibility_analysis', {}))
        self.recommendations = json.dumps(analysis_data.get('recommendations', []))
        
        # Calculer les statistiques
        recommendations = analysis_data.get('recommendations', [])
        self.total_issues = len(recommendations)
        self.severity_high = len([r for r in recommendations if r.get('severity') == 'high'])
        self.severity_medium = len([r for r in recommendations if r.get('severity') == 'medium'])
        self.severity_low = len([r for r in recommendations if r.get('severity') == 'low'])
    
    def to_dict(self):
        """Convertir l'analyse en dictionnaire"""
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'image_name': self.image_name,
            'image_dimensions': json.loads(self.image_dimensions) if self.image_dimensions else {},
            'color_analysis': json.loads(self.color_analysis) if self.color_analysis else {},
            'element_detection': json.loads(self.element_detection) if self.element_detection else {},
            'text_analysis': json.loads(self.text_analysis) if self.text_analysis else {},
            'layout_analysis': json.loads(self.layout_analysis) if self.layout_analysis else {},
            'accessibility_analysis': json.loads(self.accessibility_analysis) if self.accessibility_analysis else {},
            'recommendations': json.loads(self.recommendations) if self.recommendations else [],
            'statistics': {
                'total_issues': self.total_issues,
                'severity_high': self.severity_high,
                'severity_medium': self.severity_medium,
                'severity_low': self.severity_low
            }
        }
    
    @staticmethod
    def get_recent_analyses(limit=10):
        """Récupérer les analyses récentes"""
        return Analysis.query.order_by(Analysis.timestamp.desc()).limit(limit).all()
    
    @staticmethod
    def get_analysis_by_id(analysis_id):
        """Récupérer une analyse par son ID"""
        return Analysis.query.get(analysis_id)

class AnalysisStats(db.Model):
    """Modèle pour stocker les statistiques globales"""
    __tablename__ = 'analysis_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=datetime.utcnow().date, nullable=False)
    total_analyses = db.Column(db.Integer, default=0)
    avg_issues_per_analysis = db.Column(db.Float, default=0.0)
    most_common_issue_type = db.Column(db.String(100), nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'total_analyses': self.total_analyses,
            'avg_issues_per_analysis': self.avg_issues_per_analysis,
            'most_common_issue_type': self.most_common_issue_type
        }

