from app import app, db
from app.models import User, Concept, SearchWord, Image

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Concept': Concept, 'SearchWord': SearchWord, 'Image': Image}