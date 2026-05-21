import os
import json
import requests
import asyncio

TEST_CASES_PATH = "./test_cases.json"

def load_test_cases(file_path: os.PathLike):
    with open(file_path, 'r', encoding='utf-8') as f:
        test_cases = json.load(f)
    print(f"{len(test_cases)}개의 테스트 케이스가 로드되었습니다.")
    return test_cases

def main():
    test_cases = load_test_cases(TEST_CASES_PATH)
    for i, tc in enumerate(test_cases):
        print(f"Case [{i+1}/{len(test_cases)}]")
        match tc['Method']:
            case "post":
                rq = requests.post(url=tc['url'], json=tc['data'])
            case "patch":
                rq = requests.patch(url=tc['url'], json=tc['data'])
            case "delete":
                rq = requests.delete(url=tc['url'], json=tc['data'])
            case "get":
                rq = requests.get(url=tc['url'], json=tc['data'])
                
            case _:
                continue

       
        print(rq, rq.content.decode('utf-8'))
        print()
    return

if __name__ == "__main__":
    main()