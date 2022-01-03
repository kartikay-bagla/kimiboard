from server_dashboard.extensions import db


class Tile(db.Model):
    """User model."""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    icon = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(200), nullable=False)

    @property
    def as_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "icon": self.icon,
            "url": self.url,
        }
