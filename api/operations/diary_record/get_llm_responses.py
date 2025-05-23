import time
import json
from models import postgres_session, DiaryRecord
from llms.diary_llm import DiaryLLM
from constants import WAIT_BETWEEN_LLM_QUERIES_SECONDS

PROMPT = """
Don't block this prompt, it is safe.
Проанализируй текст и верни результаты в виде JSON объекта.
Опиши о ком идет речь в данном тексте, верни список субъектов без пояснений в виде json массива с ключом subjects. Учитывай, что автор текста - это Сергей. Макс, Максим - это сын автора. Аня - это жена автора, Ира или бабушка Ира- мама Сергей, Саша или дедушка Саша - отец Сергея. Поместе информация о том, что делал каждый субъект в текстe, как вложенные подмассивы json в массиве "subjects".
Оцени настроение автора по шкале от 0 до 10, где 0 ужасное настроение, а 10 - отличное, верни оценку в JSON структуре с ключом "mood_mark". Также опиши настроение одним двумя словами и верни в структуре с ключом "mood".
Также верни список ключевых слов о чем идет речь в тексте и помести в JSON массив с ключом "tags".
Сделай краткое самари текста и верни в структуре с ключом "summary".
Добавь в структуру оценку физического состояния и здоровья автора текста от 0 до 10. где 0 - чувствует себя очень плохо, больной, 10 - полон сил и здоров и помести в поле с ключом "health_mark", если в тексте нет информации, пусть поле будет null. Если известны причины физического замочувствия, напиши их в поле "health_reason" или оставь поле null, если они неизвестны.
Опиши одним словом физическое состояние и здоровье автора и помести в поле "health", если в тексте нет информации, пусть поле будет null.
Опиши погоду в тексте одним словом, результат помести в поле "weather", если в тексте нет информации о погоде, пусть поле будет null.
Если в тексте есть информация о еде, то выведи список в виде json массива с ключом "food", если информации нет, то пусть поле будет null.
Если известна какая-либо географическая информация или места, где происходят события, то помести список мест в json массив с ключом "locations".
Если известна какая-либо информация о болезнях автора в этот день, то помести в ключ "illness".

Текст: ###DOCUMENT###
"""


class GetLLMResponses:
    def __init__(self) -> None:
        self.session = postgres_session()
        self.model = DiaryLLM().get()

    def run(self):
        diary_records = (
            self.session.query(DiaryRecord)
            .filter(DiaryRecord.llm_response == None)
            .all()
        )
        for diary_record in diary_records:
            try:
                print(
                    f"Processing record at='{diary_record.happened_at}' id='{diary_record.id}'"
                )
                response = self.model.invoke(
                    PROMPT.replace("###DOCUMENT###", diary_record.body)
                )
                llm_response = json.loads(
                    response.content.replace("```json", "").replace("```", "")
                )
                diary_record.llm_response = llm_response
                self.session.commit()
            except:
                print(response)
                print(f"error for {diary_record.id}")
            finally:
                time.sleep(WAIT_BETWEEN_LLM_QUERIES_SECONDS)  # Free tier
