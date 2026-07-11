# ROS2 패키지 및 Python 빌드 시스템 조사

## 1. ROS2 패키지 생성
`ros2 pkg create`란 새로운 패키지를 만들 때 사용하는 명령어 입니다.  

```bash
ros2 pkg create --build-type ament_python --dependencies rclpy my_robot_controller
```

#### 해석
여기서 ` --build-type`란 패키지 빌드를 할 때 사용할 기본 시스템을 정하는 것 입니다.  
python으로 설정할 경우 `ament_python`을 입력하고  
C++로 설정할 경우 `ament_cmake`를 입력합니다.  

`--dependencies`란 패키지를 생성하고 실행하기 위한 의존성 부여 명령어로  
줄여서 `-d`라고 적어도 됩니다.

#### 명령어 구조
```
ros2 pkg create <패키지_이름> --build-type <빌드_타입> --dependencies <의존성_패키지>
```

## 2. ROS2의 colcon 명령어
`colcon`은 ROS2에서 사용하는 크로스 플랫폼 빌드 자동화 도구 입니다.  

#### colcon의 역할
| 역할 | 설명 |
|---|---|
| 의존성 기반 정렬 | package.xml에 설정해둔 패키지 간의 의존 관계를 분석한 뒤 빌드할 패키지의 빌드 순서를 자동 정렬 |
| 환경 격리 및 병렬 빌드 | 각 패키지를 각각의 프로세스로 빌드한 뒤 상호 간섭을 방지하고 멀티코어 CPU로 병렬 빌드하여 빌드 시간을 줄임 |
| 작업 공간 격리 | src 폴더에 추가 되지 않고 build, install, log라는 별개의 폴더로 관리됨 |

#### 명령어
```bash
colcon build
```

## 3. ROS2 Python 빌드 시스템(ament_python)
`ros2 pkg create`를 명령할 때 빌드 타입을 정하여 명령하au
Python으로 ROS2 패키지를 생성할 때 사용하는 빌드 시스템은 ament_python입니다.

## 4. rclpy란?
ROS2의 Node 개발할 때 사용하는 라이브러리 입니다. 
노드 생성, 토픽(Publish/Subscribe), 서비스(Service), 액션(Action) 등을 할 수 있으며  
파이썬으로 ROS2 제어 프로그램을 개발할 때 사용합니다.

## 5. 파일구조
#### package.xml 파일의 역할과 구조
package.xml은 ROS2 패키지의 기본 정보와 의존성, 빌드 시스템을 정의하는 메타데이터 파일입니다.  

| 코드 | 설명 |
|---|---|
| `<name>my_robot_controller</name>` | 패키지명 정의 |
 | `<version>0.0.0</version>` | 패키지 버전 |
|`<maintainer email="temporary020627@gmail.com">student</maintainer>`| 패키지 관리자 성함 및 이메일 |
|`<depend>rclpy</depend>`| 패키지 실행 및 빌드 시 rclpy 적용 |
|`<test_depend>ament_flake8</test_depend> <test_depend>ament_pep257</test_depend><test_depend>python3-pytest</test_depend>`| 코드 스타일 검사 및 테스트 |
|`<build_type>ament_python</build_type>`| ament_python 빌드 시스템 적용 |

```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>my_robot_controller</name>
  <version>0.0.0</version>
  <description>TODO: Package description</description>
  <maintainer email="temporary020627@gmail.com">student</maintainer>
  <license>TODO: License declaration</license>

  <depend>rclpy</depend>

  <test_depend>ament_copyright</test_depend>
  <test_depend>ament_flake8</test_depend>
  <test_depend>ament_pep257</test_depend>
  <test_depend>python3-pytest</test_depend>

  <export>
    <build_type>ament_python</build_type>
  </export>
</package>
```

#### setup.py 파일의 역할과 구조
파이썬 패키지를 어떤 방식으로 설치하고 실행할지 설정하는 파일입니다.

| 코드 | 설명 |
|---|---|
| `package_name` | 패키지 이름 설정 |
| `packages` | 설치할 Python 패키지 검색 |
| `data_files` | 리소스 설치 |
| `install_requires` | 필요한 라이브러리 설치 |
| `entry_points` | ros2 run 실행 프로그램 등록 |

```python
from setuptools import find_packages, setup

package_name = 'my_robot_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='student',
    maintainer_email='temporary020627@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
```

## 6. 워크스페이스 구조(tree 실행 결과)
#### 명령어
```bash
~/ros2_ws$ tree ~/ros2_ws/src/my_robot_controller
```

#### 구조
```bash
/home/student/ros2_ws/src/my_robot_controller
├── my_robot_controller
│   └── __init__.py
├── package.xml
├── resource
│   └── my_robot_controller
├── setup.cfg
├── setup.py
└── test
    ├── test_copyright.py
    ├── test_flake8.py
    └── test_pep257.py

3 directories, 8 files
```














