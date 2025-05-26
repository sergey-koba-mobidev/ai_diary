import csv
import dateparser
from models import postgres_session, Sleep


class ImportCsv:
    """
    Expected structure:
    date,deepSleepTime,shallowSleepTime,wakeTime,start,stop,REMTime,naps
    2022-01-01,76,331,0,2021-12-31 23:02:00+0000,2022-01-01 06:50:00+0000,61,
    """

    def __init__(self, file_name) -> None:
        self.file_name = f"/health_files/{file_name}"
        self.session = postgres_session()

    def run(self):
        lines = []
        with self.session as session:
            with open(self.file_name, mode="r", encoding="utf-8-sig") as file:
                csv_file = csv.DictReader(file)
                for line in csv_file:
                    lines.append(line)
                    happened_at = dateparser.parse(line["date"])
                    sleep_record = self._get_sleep_by_date(happened_at)
                    if not sleep_record:
                        print(f"Creating sleep record for {line['date']}")
                        naps = line["naps"]
                        if naps == "":
                            naps = 0
                        sleep_record = Sleep(
                            deep_sleep_time=int(line["deepSleepTime"]),
                            shallow_sleep_time=int(line["shallowSleepTime"]),
                            rem_time=int(line["REMTime"]),
                            total_sleep_time=int(line["deepSleepTime"])
                            + int(line["shallowSleepTime"])
                            + int(line["REMTime"]),
                            wake_time=int(line["wakeTime"]),
                            start_at=dateparser.parse(line["start"]),
                            stop_at=dateparser.parse(line["stop"]),
                            naps=int(),
                            happened_at=happened_at,
                        )
                        session.add(sleep_record)
                        session.commit()
                    else:
                        print(f"Skip sleep record {line['date']}. Already in database.")

        return lines

    def _get_sleep_by_date(self, happened_at):
        return (
            self.session.query(Sleep).filter(Sleep.happened_at == happened_at).first()
        )
