# Ubuntu Linux 실습 보고서

## 문제 1. Ubuntu 환경 구성

### 1) 수행 내용
Ubuntu 22.04 환경에서 VMware Workstation을 사용하여 리눅스 환경을 구성하였다.
Chrome 웹 브라우저와 Visual Studio Code를 설치하여 개발 환경을 구축하였다.

### 2) 설치 결과
- Google Chrome 설치 완료
```
student@robotics:~/study/linux/project01$ google-chrome --version
Google Chrome 150.0.7871.46 
```
- Visual Studio Code 설치 완료
```
student@robotics:~/study/linux/project01$ code --version
1.127.0
```
- 네트워크 연결 상태 확인 완료 (ping 명령어 사용)
```
student@robotics:~/Desktop$ ping -c 4 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=128 time=78.6 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=128 time=471 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=128 time=56.3 ms
64 bytes from 8.8.8.8: icmp_seq=4 ttl=128 time=53.1 ms
```

## 문제 2. Python 프로그램 작성 및 실행
### 1) 수행 내용
VS Code를 이용하여 Python 프로그램을 작성하였다. <br>
해당 프로그램은 test 디렉토리를 생성하고 그 안에 "Hello Linux" 문자열을 포함한 hello.txt 파일을 생성한다.

### 2) 폴더 구조

```
home/
└── student/
    └── study/
        └── linux/
            └── project01/
                ├── test/
                │   └── hello.txt
                ├── 1_hello.py
                └── 1_linux.md
```

### 3) 프로그램 코드

```python
import os

def main():
    target_directory = "test"
    file_path = os.path.join(target_directory, "hello.txt")
    content = "Hello Linux"

    os.makedirs(target_directory, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    print(f"file creation complete: {file_path}")

if __name__ == "__main__":
    main()
```
