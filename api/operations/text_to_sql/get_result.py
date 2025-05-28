import json
import decimal, datetime
from sqlalchemy import text
from .generate_sql import GenerateSQL
from models import postgres_session


def alchemyencoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)


class GetResult:
    def __init__(self, user_input) -> None:
        self.user_input = user_input
        self.session = postgres_session()

    def run(self):
        sql = GenerateSQL(user_input=self.user_input).run()
        res = self.session.execute(text(sql)).mappings().all()
        return json.dumps([dict(r) for r in res], default=alchemyencoder)
