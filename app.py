from flask import Flask, render_template
from config import Config
from database.models import db
from routes.prediction_routes import prediction_bp
from routes.report_routes import report_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(prediction_bp)
    app.register_blueprint(report_bp)

    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/diabetes")
    def diabetes_page():
        return render_template("diabetes.html")

    @app.route("/heart")
    def heart_page():
        return render_template("heart.html")

    @app.route("/breast-cancer")
    def breast_cancer_page():
        return render_template("breast_cancer.html")

    @app.route("/history")
    def history_page():
        return render_template("history.html")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)