from app import db


class User(db.Model):
    """User of the app."""
    __tablename__ = 'User'

    id       = db.Column(db.Integer, primary_key=True)
    email    = db.Column(db.String(128), index=True, unique=True)
    nickname = db.Column(db.String(32), index=True, unique=True)

    def is_authenticated(self):
        # not "is this user authenticated?"
        # actually means "should this user be ALLOWED to authenticate?"
        return True

    def is_active(self):
        # "is this account currently able to be used) (i.e. not banned)
        # not "is this account currently logged in?"
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return 'User(id={}, email={}, nickname={})'.format(self.id,
                self.email, self.nickname)


# TODO properly implement many-to-many
class ArtistEntry(db.Model):
    """
    An entry for an artist on a user's to-listen list.

    One record per user-artist pair.
    """
    __tablename__ = 'ArtistEntry' # could do __tablename__ = __name__ instead

    name  = db.Column(db.String(64), primary_key=True)
    album = db.Column(db.String(128))
    id    = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)

    def __repr__(self):
        return 'ArtistEntry(name={}, album={}, id={})'.format(self.name,
                self.album, self.id)
