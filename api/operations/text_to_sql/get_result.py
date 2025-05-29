import json
import decimal, datetime
from sqlalchemy import text
from .generate_sql import GenerateSQL
from models import postgres_session
from llms.diary_llm import DiaryLLM

PROMPT = """
Please generate chart using apex chart javascript library based on the following data in json format: 
###JSON_DATA###

And input from user:
###USER_INPUT###

Return html tag div for chart with unique random id and javascript code.
No body, head and other elements. Return as one section of html page.
Don't add any comments and minimize the code where possible.
Generate unique js variables names.
Set apex chart option width to "700px".
Remember, that value in labels formatter can be undefined.
"""


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
        self.model = DiaryLLM().get()

    def run(self):
        sql = GenerateSQL(user_input=self.user_input).run()
        res = (
            self.session.execute(text(sql)).mappings().all()
        )  # ideally validate for delete, update, etc and return error
        json_data = json.dumps([dict(r) for r in res], default=alchemyencoder)
        response = self.model.invoke(
            PROMPT.replace("###USER_INPUT###", self.user_input).replace(
                "###JSON_DATA###", json_data
            )
        )
        generated_html = response.content.replace("```html", "").replace("```", "")
        return {"answer": generated_html}
