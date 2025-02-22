import typer
from llms.diary_llm import DiaryLLM

app = typer.Typer(no_args_is_help=True)


@app.command()
def invoke_llm(query: str):
    """
    Just directly ask LLM something.
    """
    model = DiaryLLM().get()
    response = model.invoke(query)
    print(response)


@app.command()
def test(query: str):
    """
    Test
    """
    print("test")


if __name__ == "__main__":
    app()
