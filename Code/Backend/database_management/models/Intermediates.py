from Extensions import db

class Banned(db.Model):
    __tablename__ = 'banned'
    _id = db.Column(db.Integer, primary_key=True)
    _format_id = db.Column(db.Integer, db.ForeignKey('formats._id', ondelete='CASCADE'), nullable=False)
    _card_id = db.Column(db.Integer, db.ForeignKey('cards._id', ondelete='CASCADE'), nullable=False)

class Restricted(db.Model):
    __tablename__ = 'restricted'
    _id = db.Column(db.Integer, primary_key=True)
    _format_id = db.Column(db.Integer, db.ForeignKey('formats._id', ondelete='CASCADE'), nullable=False)
    _card_id = db.Column(db.Integer, db.ForeignKey('cards._id', ondelete='CASCADE'), nullable=False)

class Legal(db.Model):
    __tablename__ = 'legal'
    _id = db.Column(db.Integer, primary_key=True)
    _format_id = db.Column(db.Integer, db.ForeignKey('formats._id', ondelete='CASCADE'), nullable=False)
    _card_id = db.Column(db.Integer, db.ForeignKey('cards._id', ondelete='CASCADE'), nullable=False)

class GameFormats(db.Model):
    __tablename__ = 'gameformats'
    _id = db.Column(db.Integer, primary_key=True)
    _format_id = db.Column(db.Integer, db.ForeignKey('formats._id', ondelete='CASCADE'), nullable=False)
    _game_id = db.Column(db.Integer, db.ForeignKey('games._id', ondelete='CASCADE'), nullable=False)

class GameCards(db.Model):
    __tablename__ = 'gamecards'
    _id = db.Column(db.Integer, primary_key=True)
    _card_id = db.Column(db.Integer, db.ForeignKey('cards._id', ondelete='CASCADE'), nullable=False)
    _game_id = db.Column(db.Integer, db.ForeignKey('games._id', ondelete='CASCADE'), nullable=False)
