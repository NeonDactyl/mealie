import sqlalchemy as sa

from mealie.db.models._model_base import SqlAlchemyBase
from mealie.db.models._model_utils.guid import GUID


class ApiExtras(SqlAlchemyBase):
    __tablename__ = "api_extras"
    id = sa.Column(sa.Integer, primary_key=True)
    recipee_id = sa.Column(GUID, sa.ForeignKey("recipes.id"))
    key_name = sa.Column(sa.String)
    value = sa.Column(sa.String)

    def __init__(self, key, value) -> None:
        self.key_name = key
        self.value = value
