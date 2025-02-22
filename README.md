# AI Diary

## Idea
Parse diary in PDF files, add tags, keywords, build analytics using LLM.

## Architecture
- use Langchain as framework to connect LLM with python
- use Ollama as LLM
- use Postgres as Vector DB and DocStore

## Getting started
- Install Docker and Docker Compose
- clone project
- run `make setup`

## Everyday Usage
- `make start`
- `make stop`
- `make invoke-llm QUERY="<QUESTION>"` - ask LLM a question. Example: `make invoke-llm QUERY="how are you?"`

## Help
- run `make help` to see all commands

## Endpoints
- http://localhost:8080/ - Adminer database manager
- http://localhost:8000/api - Api
- http://localhost:8000/docs - Api docs
- http://localhost/ - Front
- http://localhost:11434/ - Ollama API

## License
TODO
