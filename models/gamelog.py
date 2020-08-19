import datetime
from models.shared import db, ma


# GameLog Model
class GameLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grid = db.Column(db.String(10000))
    paths = db.Column(db.String(1000))
    error_flag = db.Column(db.Boolean)
    req_time = db.Column(db.DateTime, default=datetime.datetime.now())
    res_duration = db.Column(db.Float)

    def __repr__(self):
        return '<Log %r>' % self.req_time.strftime("%d-%m-%Y (%H:%M:%S)")


# GameLog Schema
class GameLogSchema(ma.Schema):
    class Meta:
        fields = ("id", "grid", "paths", "error_flag", "req_time", "res_duration")


# Initialize Schemas
gamelog_schema = GameLogSchema()
gamelogs_schema = GameLogSchema(many=True)