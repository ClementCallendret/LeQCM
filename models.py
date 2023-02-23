from extension import db

class Professor(db.Model):
    __tablename__ = "professor"
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(50), nullable=False)
    sel = db.Column(db.String(64))

class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    sel = db.Column(db.String(64))

class Question(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    state = db.Column(db.Text, nullable=False)
    numeralAnswer = db.Column(db.Float, nullable=True)
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
    title = db.Column(db.String(50), nullable=False)
    idP = db.Column(db.Integer, db.ForeignKey("professor.username"))

class InSerie(db.Model):
    __tablename__ = "inSerie"
    idS = db.Column(db.Integer, db.ForeignKey("serie.id"), primary_key=True)
    idQ = db.Column(db.Integer, db.ForeignKey("question.id"), primary_key=True)
    posQ = db.Column(db.Integer, nullable=False)

class Session(db.Model):
    __tablename__ = "session"
    id = db.Column(db.Integer, primary_key=True)
    idP = db.Column(db.Integer, db.ForeignKey("professor.username"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    idSequence = db.Column(db.Integer, db.ForeignKey("serie.id"), nullable=True)

class StudentAnswer(db.Model):
    __tablename__ = "studentAnswer"
    idSession = db.Column(db.Integer, db.ForeignKey("session.id"), primary_key=True)
    idStudent = db.Column(db.Integer, db.ForeignKey("student.id"), primary_key=True)
    idQuestion = db.Column(db.Integer, db.ForeignKey("question.id"), primary_key=True)
    correct = db.Column(db.Boolean, nullable=False)
    