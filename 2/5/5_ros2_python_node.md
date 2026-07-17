# ROS2 Python 노드 생성 및 빌드

## 1. 수행 목표
### 1. ROS2 Humble 환경에서 Python으로 간단한 노드를 작성한다.

- 노드 이름은 logging_node로 설정.
- 실행 시  노드 이름을 INFO 수준의 로그로 출력.
- 로그를 출력한 뒤 실행 상태를 유지.
- setup.py에 실행 프로그램 등록.
- colcon build --symlink-install 명령어로 빌드.
- ros2 run 명령어로 노드 실행.

## 2. 개발 환경

- 운영체제: Ubuntu 22.04
- 셸: Bash
- ROS2 배포판: Humble
- 프로그래밍 언어: Python
- ROS2 Python 클라이언트 라이브러리: rclpy
- 빌드 도구: colcon
- 빌드 형식: ament_python

## 3. 파일 구조 및 경로
#### 트리구조
```text
ros2_ws/
├── src/
│   └── my_robot_controller/
│       ├── my_robot_controller/
│       │   ├── __init__.py
│       │   └── logging.py
│       ├── resource/
│       │   └── my_robot_controller
│       ├── package.xml
│       ├── setup.cfg
│       └── setup.py
├── build/
├── install/
└── log/
```

#### logging.py 경로

```text
~/ros2_ws/src/my_robot_controller/my_robot_controller/logging.py
```

## 4. Python 노드 소스 코드
#### logging.py

```python
import rclpy
from rclpy.node import Node


class LoggingNode(Node):
    """노드 이름 INFO 로그로 출력"""

    def __init__(self):
        super().__init__('logging_node')

        # 현재 노드 가져와 INFO 로그 출력
        node_name = self.get_name()
        self.get_logger().info(f'노드 이름: {node_name}')


def main(args=None):
    """노드를 초기화하고 실행 상태를 유지"""

    # ROS2 Python 통신 시스템 초기화
    rclpy.init(args=args)

    # LoggingNode 클래스 객체 생성
    logging_node = LoggingNode()

    try:
        # 노드 실행 상태를 유지
        # 콜백 들어오면 처리 위해 대기
        rclpy.spin(logging_node)

    except KeyboardInterrupt:
        # 종료했을 때 안내 로그
        logging_node.get_logger().info('logging_node를 종료합니다.')

    finally:
        # 노드가 사용한 자원을 정리
        logging_node.destroy_node()

        # 통신 시스템을 종료한다.
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## 5. rclpy.node.Node 클래스 상속
1. ROS2의 기능은 노드 단위로 작성.  
2. Python에서 ROS2 노드를 만들 때는 rclpy.node 모듈의 Node 클래스를 상속받은 새로운 클래스를 정의.

```python
from rclpy.node import Node

class LoggingNode(Node):
    def __init__(self):
        super().__init__('logging_node')
```

LoggingNode 클래스가 ROS2의 Node 클래스를 상속.

```python
super().__init__('logging_node')
```

#### Node 클래스를 상속 시 가능한 것

- Publisher 생성
- Subscriber 생성
- Service 생성
- Client 생성
- Timer 생성
- Parameter 관리
- ROS2 로그 기록
- 노드 이름 및 네임스페이스 관리


## 6. 노드 객체 생성

#### 클래스 객체 생성

```python
logging_node = LoggingNode()
```

#### 메서드 호출된 뒤 ROS2 노드 생성

```python
super().__init__('logging_node')
```

#### rclpy.spin()에 전달 후 실행

```python
rclpy.spin(logging_node)
```

## 7. rclpy.init()의 역할
#### 프로그램 사용을 위한 초기화 함수
```python
rclpy.init(args=args)
```
#### 역할
- ROS2 통신 기능 초기화
- ROS2 실행 컨텍스트 초기화
- 명령행 인자 처리
- 노드가 ROS2 네트워크에 참여할 수 있도록 준비

#### 실행 순서
```python
rclpy.init(args=args)
node = LoggingNode()
```
--> 주의: rclpy.init()`을 호출하지 않으면 노드 생성시 오류가 생길 수 있음

## 8. rclpy.spin()의 역할

#### 전달받은 노드가 계속 실행시키는 함수
```python
rclpy.spin(logging_node)
```

#### 노드실행 중일 때 해야할 것
- Subscriber 메시지 수신
- Service 요청 수신
- Timer 실행
- Action 요청 처리
- 등록된 콜백 함수 실행

#### rclpy.spin()을 사용하는 이유
Python 프로그램은 마지막 코드가 실행되면 종료하면 되지만  
로봇의 노드는 센서 메시지, 제어 명령, 서비스 요청 등등을 기다려야 하기에 바로 종료하면 안됨

## 9. rclpy.shutdown()의 역할

#### 실행 환경 종료 함수
```python
rclpy.shutdown()
```
#### 역할
- ROS2 실행 컨텍스트 종료
- 통신 기능 종료
- ROS2 관련 자원 정리
- 프로그램의 정상적인 종료 처리

#### 노드 반드시 사용하는 코드
```python
finally:
    logging_node.destroy_node()
    rclpy.shutdown()
```
| 코드 | 역할 |
|---|---|
| destroy_node() |  생성한 노드 객체의 자원을 정리 | 
| rclpy.shutdown() | 실행 환경 종료 |

## 10. 실행 순서
```python
rclpy.init()
node = LoggingNode()
rclpy.spin(node)
node.destroy_node()
rclpy.shutdown()
```

| 코드 | 역할 |
|---|---|
| rclpy.init() | ROS2 환경을 초기화 | 
| LoggingNode() | 노드 객체 생성 |
| rclpy.spin() | 노드 실행 유지 |
| destroy_node() | 노드 객체 자원을 정리 |
| rclpy.shutdown() | ROS2 환경 종료 |

## 11. ROS2 로그 기록 방법

흔한 프로그래밍언어 처럼 print, println이 아닌  Logger를 사용

#### INFO 수준의 로그 출력
```python
self.get_logger().info('출력할 메시지')
```

#### 현재 노드 이름을 출력
```python
node_name = self.get_name()
self.get_logger().info(f'노드 이름: {node_name}')
```

실행 결과
```bash
[INFO] [1784244567.896924028] [logging_node]: 노드 이름: logging_node
```

#### [참고] - Logger의 로그 수준
```text
DEBUG --> INFO --> WARNING --> ERROR --> FATAL
```
