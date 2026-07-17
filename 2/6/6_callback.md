# ROS2 타이머와 콜백 함수

## 1. 실습 목표
#### ROS2 Python 노드에서 두 개의 타이머를 생성하고 각각 다른 주기의 콜백 함수를 실행한다.

* 노드 이름: timer_node
* Python 파일 이름: timer_test.py
* 2초 타이머: 카운터를 1 증가
* 3초 타이머: 카운터를 1 감소
* 공용 카운터 초기값: 0

## 2. ROS2 타이머
### 1. 타이머란?
#### 지정한 시간 간격마다 특정 함수를 반복해서 실행하도록 만드는 기능
- 2초마다 센서 값을 확인 
- 1초마다 메시지 전송 
- 일정 주기로 로봇의 상태 검사
- 타이머가 실행할 함수를 콜백 함수로 등록

### 2. create_timer 사용 방법
#### 타이머를 생성
```python
self.timer = self.create_timer(
    timer_period_sec,
    callback_function,
)
```

#### 구조
```python
self.create_timer(반복할_시간, 실행할_콜백_함수)
```
```python
self.timer = self.create_timer(
    2.0,
    self.timer_callback,
)
```

* 첫 번째 값 2.0: 타이머 실행 주기이며 단위는 초이다.
* 두 번째 값 self.timer_callback: 주기마다 호출할 함수이다.
* 콜백 함수 이름 뒤에는 괄호 ()를 붙이지 않는다.

#### 콜백 함수
```python
def timer_callback(self):
    self.get_logger().info("2초가 지났습니다.")
```

노드가 rclpy.spin()으로 실행되는 동안 타이머의 시간에 따라 콜백 함수 반복 호출

## 3. 콜백 함수
### 1. 콜백 함수란?
 프로그램이 특정 조건이나 사건이 발생했을 때 자동으로 호출되는 함수

#### 일반 함수 직접 실행하는 경우
```python
timer_callback()
```
#### 콜백함수 실행하는 경우
```python
self.create_timer(2.0, self.timer_callback)
```

self.timer_callback은 타이머가 호출할 함수의 정보를 전달하는 코드이다.

### 2. 콜백 함수의 역할 및 필요한 이유
#### 역할
* 일정 시간이 지남
* 센서 데이터가 도착함
* 다른 노드의 메시지가 도착함
* 서비스 요청이 들어옴
* 사용자가 명령을 입력함

#### 필요한 이유
프로그램이 모든 것을 직접 순서대로 확인하면 코드가 복잡해질 수 있기 때문이다.  
콜백 함수를 등록하면 ROS2가 사건이나 실행 시간이 발생했을 때  
필요한 함수를 호출해 주기 때문에 여러 작업을 효율적으로 처리할 수 있다.


## 4. 타이머 노드 구현
#### 파일 위치
```text
ros2_ws/src/my_robot_controller/my_robot_controller/timer_test.py
```

#### 코드
```python
import rclpy
from rclpy.node import Node


class TimerNode(Node):
    """2초 및 3초 주기의 타이머를 실행하는 ROS2 노드."""

    def __init__(self):
        """노드를 생성하고 카운터와 타이머를 초기화한다."""
        super().__init__("timer_node")

        # 두 타이머가 함께 사용할 클래스 속성
        self.counter = 0

        # 2초마다 카운터 증가 함수 호출
        self.timer_2_seconds = self.create_timer(
            2.0,
            self.timer_2_seconds_callback,
        )

        # 3초마다 카운터 감소 함수 호출
        self.timer_3_seconds = self.create_timer(
            3.0,
            self.timer_3_seconds_callback,
        )

    def timer_2_seconds_callback(self):
        """2초마다 카운터를 1 증가시키고 로그를 출력한다."""
        self.counter += 1

        self.get_logger().info(
            f"2 seconds passed : {self.counter}"
        )

    def timer_3_seconds_callback(self):
        """3초마다 카운터를 1 감소시키고 로그를 출력한다."""
        self.counter -= 1

        self.get_logger().info(
            f"3 seconds passed : {self.counter}"
        )


def main(args=None):
    """ROS2를 초기화하고 timer_node를 실행한다."""
    rclpy.init(args=args)

    timer_node = TimerNode()

    try:
        rclpy.spin(timer_node)
    except KeyboardInterrupt:
        pass
    finally:
        timer_node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
```

---

## 5. setup.py 실행 프로그램 등록

timer_test.py를 ros2 run 명령어로 실행하려면 setup.py의 entry_points에 등록해야 한다.

```python
entry_points={
    'console_scripts': [
        'timer_node = my_robot_controller.timer_test:main',
    ],
},
```

```text
timer_node = my_robot_controller.timer_test:main
```
| 코드 | 의미 |
|---|---|
| timer_node | ros2 run에서 사용할 실행 프로그램 이름 |
| my_robot_controller | Python 패키지 이름 |
| timer_test | timer_test.py 파일 이름 |
| main | 실행할 main() 함수 이름 | 

## 6. 빌드 및 실행 방법
#### ROS2 Humble 환경을 적용
```bash
source /opt/ros/humble/setup.bash
```

#### 패키지를 빌드
```bash
colcon build --packages-select my_robot_controller --symlink-install
```

#### 빌드 결과를 현재 터미널에 적용
```bash
source install/setup.bash
```

#### 노드 실행
```bash
ros2 run my_robot_controller timer_node
```

#### 종료
```text
Ctrl + C
```

---

## 7. 실행 결과
```text
[INFO] [시간] [timer_node]: 2 seconds passed : 1
[INFO] [시간] [timer_node]: 3 seconds passed : 0
[INFO] [시간] [timer_node]: 2 seconds passed : 1
[INFO] [시간] [timer_node]: 2 seconds passed : 2
[INFO] [시간] [timer_node]: 3 seconds passed : 1
[INFO] [시간] [timer_node]: 2 seconds passed : 2
[INFO] [시간] [timer_node]: 3 seconds passed : 1
```
프로그램을 실행하면 2초 타이머와 3초 타이머가 각각 반복해서 콜백 함수를 호출한다.  
2초 타이머와 3초 타이머는 6초마다 실행 시점이 겹친다.  
따라서 컴퓨터의 실행 상황에 따라 6초 시점에는 2초 콜백과 3초 콜백의 로그 순서가 달라질 수 있다.

## 8. 실습 결과
이번 실습에서는 하나의 ROS2 노드에 두 개의 타이머를 생성하였다.  
2초 타이머는 공용 카운터를 1 증가시키고, 3초 타이머는 같은 카운터를 1 감소시켰다.  
각 타이머에 콜백 함수를 등록하여 지정된 시간이 지날 때마다 해당 함수가 자동으로 실행되는 것을 확인하였다.  
