from llms.diary_llm import DiaryLLM

model = DiaryLLM().get()
response = model.invoke("Hello")
print(response)
