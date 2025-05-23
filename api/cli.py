import typer
from llms.diary_llm import DiaryLLM
from operations.diary_file.load import Load
from operations.diary_record.get_llm_responses import GetLLMResponses
from operations.tag.generate_all import GenerateAll as GenerateAllTags
from operations.person.generate_all import GenerateAll as GenerateAllPersons

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
def import_diary_file(file_name: str):
    """
    Import a markdown file from /diary_files folder, split it by headers ### and load to database
    """
    documents = Load(file_name=file_name).run()
    print(f"Processed {len(documents)} records.")


@app.command()
def get_llm_responses():
    """
    Process all diary records without response and get response
    """
    GetLLMResponses().run()


@app.command()
def process_llm_responses():
    """
    Process all diary records with LLM responses and generate entities like tags,
    subjects, locations, etc.
    """
    GenerateAllTags().run()  # Generate tags
    print("Generated tags")
    GenerateAllPersons().run()  # Generate tags
    print("Generated persons")


if __name__ == "__main__":
    app()
