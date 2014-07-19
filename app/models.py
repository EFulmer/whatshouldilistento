from app import db


class User(db.Model):
    """User of the app."""
    __tablename__ = 'User'
    id       = db.Column(db.Integer, primary_key=True)
    email    = db.Column(db.String(128), index=True, unique=True)
    nickname = db.Column(db.String(32), index=True, unique=True)

    def __repr__(self):
        return 'User(id={}, email={}, nickname={})'.format(self.id,
                self.email, self.nickname)


# TODO properly implement many-to-many
class ArtistEntry(db.Model):
    __tablename__ = 'ArtistEntry' # could do __tablename__ = __name__ instead
    name  = db.Column(db.String(64), primary_key=True)
    album = db.Column(db.String(128))
    id    = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    def __repr__(self):
        return 'ArtistEntry(name={}, album={}, id={})'.format(self.name,
                self.album, self.id)
