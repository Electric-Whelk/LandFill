from Database.Detritus.SpellFace import SpellFace


class Card:
    def __init__(self, **kwargs):
        try:
            sco = kwargs.get('scrython_object')
        except Exception as e:
            raise Exception("scrython_object is not defined")

        self.dict = self.parse_scrython_object(sco)
        #id, color_identity, face_one, face_two, usd, eur, land

    #static methods used in setup
    @staticmethod
    def check_if_land(sco):
        tl = sco['type_line'].split(' // ')
        for face in tl:
            sp = face.split(' ')
            if 'Land' not in sp and sco['cmc'] != 0:
                return False
        return True

    @staticmethod
    def parse_scrython_object(sco):
        id = sco['oracle_id']
        color_identity = sco['color_identity']
        usd = sco['prices']['usd']
        eur = sco['prices']['eur']
        land = Card.check_if_land(sco)

        try:
            faces = Card.validate_faces(sco)
        except KeyError:
            faces = [sco, None]

        for face in faces:
            if face is not None:
                if "Land" in face['type_line'].split(" "):
                    face = LandFace(face)
                else:
                    face = SpellFace(face)

        face_one = faces[0]
        face_two = faces[1]






    @staticmethod
    def validate_faces(sco):
        faces = sco['faces']
        l = len(faces)
        name = sco['name']
        if l != 2:
            raise Exception("Card " + name + " has " + str(l) + " faces")
        return faces











