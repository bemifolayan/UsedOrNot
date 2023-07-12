from flask_sqlalchemy import SQLAlchemy

class Liked(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), unique=True, nullable=False)
    url = db.Column(db.String(), unique=True, nullable=False)
    
    def __repr__(self):
        return f"User('{self.id}', '{self.description}', '{self.url}')"

def saved_liked(id, description, url):
    liked = Liked(id=id, description=description, url=url) 
    db.session.add()
    db.session.commit()
    