from extension import db

class Professor(db.Model):
    __tablename__ = "professor"
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(50), nullable=False)
    
class Question(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    state = db.Column(db.Text, nullable=False)
    idP = db.Column(db.Integer, db.ForeignKey("professor.username"))
    
class Answer(db.Model) :
    __tablename__ = "answer"
    id = db.Column(db.Integer, primary_key=True)
    solution= db.Column(db.Boolean, nullable=False)
    text = db.Column(db.Text, nullable=False)
    idQ = db.Column(db.Integer, db.ForeignKey("question.id"))    

class Tag(db.Model):
    __tablename__ = "tag"
    name = db.Column(db.String(50), primary_key=True)
    
class HasTag(db.Model):
    __tablename__ = "hasTag"
    idQ = db.Column(db.Integer, db.ForeignKey("answer.id"), primary_key=True)
    idT = db.Column(db.String(50), db.ForeignKey("tag.name"), primary_key=True)

class Serie(db.Model):
    __tablename__ = "serie"
    id = db.Column(db.Integer, primary_key=True)

class inSerie(db.Model):
    idS = db.Column(db.Integer, db.ForeignKey("serie.id"), primary_key=True)
    idQ = db.Column(db.Integer, db.ForeignKey("question.id"), primary_key=True)
    num = db.Column(db.Integer, nullable=False)