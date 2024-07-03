import json
import os
from typing import Dict, List

from split_lang import split
from split_lang.split.splitter import SubStringSection, TextSplitter
from split_lang.split.utils import DEFAULT_THRESHOLD
from tests.data.test_data import TestData, texts_de_fr_en, texts_zh_jp_ko_en
from tests.test_config import TEST_DATA_FOLDER


def generate_test_data(data: TestData):
    # Create the tests/data directory if it doesn't exist
    os.makedirs(TEST_DATA_FOLDER, exist_ok=True)

    result: List[Dict[str, List[SubStringSection]]] = []
    for text in data.texts:
        section = split(
            text=text,
            threshold=data.threshold,
            splitter=data.splitter,
            lang_map=data.lang_map,
            default_lang=data.default_lang,
            verbose=True,
        )
        result.append({text: section})

    # Convert result to JSON serializable format using pydantic
    json_result = result

    # Write the result to a JSON file using pydantic's .json() method
    with open(
        os.path.join(TEST_DATA_FOLDER, f"{data.filename}.json"), "w", encoding="utf-8"
    ) as f:
        f.write(
            json.dumps(
                {
                    list(sections.keys())[0]: [
                        section.model_dump()
                        for section in sections[list(sections.keys())[0]]
                    ]
                    for sections in json_result
                },
                ensure_ascii=False,
                indent=4,
            )
        )


def main():
    splitter = TextSplitter()
    zh_jp_ko_en_lang_map = {
        "zh": "zh",
        "zh-cn": "zh",
        "zh-tw": "x",
        "ko": "ko",
        "ja": "ja",
    }

    data = TestData(
        filename="zh_jp_ko_en",
        texts=texts_zh_jp_ko_en,
        threshold=DEFAULT_THRESHOLD,
        splitter=splitter,
        lang_map=zh_jp_ko_en_lang_map,
        default_lang="en",
    )
    generate_test_data(data=data)

    # data = TestData(
    #     filename="de_fr_en",
    #     texts=texts_de_fr_en,
    #     threshold=4.9e-4,
    #     splitter=splitter,
    #     lang_map=None,
    #     default_lang="x",
    # )
    # generate_test_data(data=data)
    return


if __name__ == "__main__":
    main()
