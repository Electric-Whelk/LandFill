from Config import flask_db

class FlaskFormat(flask_db.Model):
    id = flask_db.Column(flask_db.Integer, primary_key=True)
    name = flask_db.Column(flask_db.String(80), unique=True, nullable=False)
    max = flask_db.Column(flask_db.Integer, unique=False, nullable=False)
    singleton = flask_db.Column(flask_db.Boolean, unique=False, nullable=False)
    hard_max = flask_db.Column(flask_db.Boolean, unique=False, nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "max": self.max,
            "singleton": self.singleton,
            "hard_max": self.hard_max
        }


    """    standard = FlaskFormat(name="Standard", max=60, singleton=False, hard_max=False)
    modern = FlaskFormat(name="Modern", max=60, singleton=False, hard_max=False)
    legacy = FlaskFormat(name="Legacy", max=60, singleton=False, hard_max=False)
    edh = FlaskFormat(name="EDH", max=100, singleton=True, hard_max=True)

    try:
        flask_db.session.add(standard)
        flask_db.session.add(modern)
        flask_db.session.add(legacy)
        flask_db.session.add(edh)

        flask_db.session.commit()
    except Exception as e:
        print("OOPS: " + str(e))
"""








    #FlaskFormat("standard", 60, False, False).toJSON(),
    #FlaskFormat("modern", 60, False, False).toJSON(),
    #FlaskFormat("legacy", 60, False, False).toJSON(),
    #FlaskFormat("EDH", 100, True, True).toJSON()
