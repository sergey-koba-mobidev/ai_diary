# AI Diary

## Idea
Parse diary in PDF files, add tags, keywords, build analytics using LLM.

## Architecture
- use Langchain as framework to connect LLM with python
- use Gemini as LLM
- use Postgres as Vector DB and DocStore

## Getting started
- Install Docker and Docker Compose
- clone project
- run `make setup`

## Everyday Usage
- `make start`
- `make stop`
- `make api-console` - open console of api container
- `make invoke-llm QUERY="<QUESTION>"` - ask LLM a question. Example: `make invoke-llm QUERY="how are you?"`
- `make alembic-revision M="<MESSAGE>"` - generate alembic revision
- `make import-diary-file FILE="<FILE_NAME>"` - import markdown file from `/diary_files`
- `make import-sleep-csv FILE="<FILE_NAME>"` - import csv file from `/health_files`
- `make get-llm-responses` - process all records without llm response
- `make process-llm-responses` - process all records with llm response and generate tags, subjects, locations, etc.

## Help
- run `make help` to see all commands

## Endpoints
- http://localhost:8080/ - Adminer database manager
- http://localhost:8000/api - Api
- http://localhost:8000/docs - Api docs
- http://localhost/ - Front

## License
TODO
