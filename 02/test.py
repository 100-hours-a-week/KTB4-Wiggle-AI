import os
import json
import requests

TEST_CASES_PATH = "./test_cases.json"

def load_test_cases(file_path: os.PathLike):
    with open(file_path, 'r', encoding='utf-8') as f:
        test_cases = json.load(f)
    print(f"{len(test_cases)}개의 테스트 케이스가 로드되었습니다.")
    return test_cases

def main():
    test_cases = load_test_cases(TEST_CASES_PATH)
    for tc in test_cases:
        match tc['Method']:
            case "create":
                rq = requests.post(url=tc['url'], json=tc['data'])
            case "update":
                rq = requests.patch(url=tc['url'], json=tc['data'])
            case "delete":
                rq = requests.delete(url=tc['url'], json=tc['data'])
            case _:
                continue

       
        print(rq, rq.content)
    return

if __name__ == "__main__":
    main()