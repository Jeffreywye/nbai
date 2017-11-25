from database.tables._base import DatabaseRecord
from database.connection import connection
from database.tables.fields import Fields as f
from database.tables.fields import Structure as s



TABLE_NAME = 'player_predictions'

@connection.register
class PlayerPredictionRecord(DatabaseRecord):

    __collection__ = TABLE_NAME

    structure = {
        f.player_id   : s.player_id,
        f.game_id     : s.game_id,
        f.team_abbr   : s.team_abbr,
        f.prediction  : s.prediction,

    }

    indexes = [
        {
            'fields' : [f.player_id],
            'unique' : False
        }
    ]

    required_fields = [
        f.player_id,
        f.game_id,
        f.team_abbr,
        f.prediction
    ]

    default_values = {

    }
