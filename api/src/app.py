from flask import Flask, request, jsonify, render_template
from .config import Config
from .model_loader import ModelLoader
from .recommender import RecommendationService

def create_app():
    """Flask application factory."""
    config = Config()
    model_loader = ModelLoader(config)
    recommender = RecommendationService(config, model_loader)

    app = Flask(__name__)

    @app.route("/")
    def home():
        return render_template('recommendation-page.html')
    
    @app.route("/api/healthCheck")
    def healthCheck():
        return jsonify({"status": "healthy", "version": config.version}), 200

    @app.route("/api/recommend", methods=["POST"])
    def recommend():
        payload = request.get_json(force=True, silent=False)
        user_songs = payload.get("songs", [])
        response, status = recommender.recommend(user_songs)
        return jsonify(response), status

    return app
