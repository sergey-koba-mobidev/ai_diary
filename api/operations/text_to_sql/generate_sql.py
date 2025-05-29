from llms.diary_llm import DiaryLLM

PROMPT = """
Based on the following database schema:
###SCHEMA_INFO###

Convert this question into a SQL query for PostgreSQL:
###USER_INPUT###

Remember that strings could have different registry.
Return ONLY the SQL query with no additional text.
"""


class GenerateSQL:
    def __init__(self, user_input) -> None:
        self.user_input = user_input
        self.model = DiaryLLM().get()

    def run(self):
        print(f"Generating SQL for {self.user_input}")
        schema_info = ""
        with open("/app/models.py", "r") as file:
            schema_info = file.read()
        response = self.model.invoke(
            PROMPT.replace("###USER_INPUT###", self.user_input).replace(
                "###SCHEMA_INFO###", schema_info
            )
        )
        generated_sql = response.content.replace("```sql", "").replace("```", "")
        print(f"Result: {generated_sql}")
        return generated_sql
