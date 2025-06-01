from Config import db

class Format(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    max = db.Column(db.Integer, unique=False, nullable=False)
    singleton = db.Column(db.Boolean, unique=False, nullable=False)
    hard_max = db.Column(db.Boolean, unique=False, nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "max": self.max,
            "singleton": self.singleton,
            "hard_max": self.hard_max
        }


    """    standard = Format(name="Standard", max=60, singleton=False, hard_max=False)
    modern = Format(name="Modern", max=60, singleton=False, hard_max=False)
    legacy = Format(name="Legacy", max=60, singleton=False, hard_max=False)
    edh = Format(name="EDH", max=100, singleton=True, hard_max=True)

    try:
        db.session.add(standard)
        db.session.add(modern)
        db.session.add(legacy)
        db.session.add(edh)

        db.session.commit()
    except Exception as e:
        print("OOPS: " + str(e))
"""








    #Format("standard", 60, False, False).toJSON(),
    #Format("modern", 60, False, False).toJSON(),
    #Format("legacy", 60, False, False).toJSON(),
    #Format("EDH", 100, True, True).toJSON()
