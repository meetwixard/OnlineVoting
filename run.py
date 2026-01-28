from flask import Flask
from app.models import db, Voter
from app.routes import vote_bp
import os

def create_app():
    app = Flask(__name__)
    
    # Configuration
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'secure_vote.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        # Create storage folder if it doesn't exist
        if not os.path.exists('instance'):
            os.makedirs('instance')
            
        db.create_all()
        # Seed test data
        if not Voter.query.get(1):
            db.session.add(Voter(id=1, username="alpha_user_01"))
            db.session.commit()

    app.register_blueprint(vote_bp)
    return app

if __name__ == '__main__':
    secure_app = create_app()
    secure_app.run(port=5000, debug=True)
