import re
import dateparser
from models import postgres_session, DiaryRecord
from langchain_text_splitters import MarkdownHeaderTextSplitter


class Load:
    def __init__(self, file_name) -> None:
        self.file_name = f"/diary_files/{file_name}"
        self.session = postgres_session()

    def run(self):
        headers_to_split_on = [
            ("###", "happened_at"),  # all diary files contain date as h3
        ]
        with open(self.file_name) as f:
            markdown_document = f.read()
        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on)
        md_header_splits = markdown_splitter.split_text(markdown_document)

        with self.session as session:
            for doc in md_header_splits:
                # remove images
                doc.page_content = re.sub("\!\[\]\[image.*\]", "", doc.page_content)
                doc.page_content = re.sub(
                    "\[image.*\]: <data:image.*>", "", doc.page_content
                ).strip()
                happened_at = dateparser.parse(doc.metadata["happened_at"])
                diary_record = self._get_record_by_date(happened_at)
                if not diary_record:
                    print(f"Creating record for {doc.metadata['happened_at']}")
                    diary_record = DiaryRecord(
                        body=doc.page_content, happened_at=happened_at
                    )
                    session.add(diary_record)
                    session.commit()
                else:
                    print(
                        f"Skip diary record {doc.metadata['happened_at']}. Already in database."
                    )

        return md_header_splits

    def _get_record_by_date(self, happened_at):
        return (
            self.session.query(DiaryRecord)
            .filter(DiaryRecord.happened_at == happened_at)
            .first()
        )
