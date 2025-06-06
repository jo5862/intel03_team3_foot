# Foot Pressure Analysis Project

이 저장소는 족저압 센서를 활용한 보행 분석 프로젝트로,  
보행 시 발바닥 압력 데이터를 기반으로 이상 보행 탐지 및 시각화를 수행합니다.

## 데이터 설명

`data/` 디렉토리에는 실제 측정된 족저압 센서 데이터(.csv)가 포함되어 있습니다.  
모든 데이터는 시간에 따른 압력 분포를 포함한 시계열 + 공간적 정보를 가지고 있습니다.

- 파일 형식 예시:
" "
- 구조:
- `정OO`: 이름 비식별화
- `L(RW)`: 보행 라벨
- `G(M)`: 성별 (Male)
- `A(28)`: 나이
- `M(...)`: 측정일시

> 모든 데이터는 **인적 식별 정보(이름, 생년월일 등)** 를 제거한 후 공개되었으며,  
> 교육 및 연구 목적의 자유로운 사용을 위해 제공됩니다.

---

## 라이선스 (License)

이 저장소에 포함된 데이터(`data/` 디렉토리 이하)는  
[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) 라이선스를 따릅니다.

사용자는 **출처를 표시하는 조건** 하에 자유롭게 데이터를 복제, 수정, 배포, 활용할 수 있습니다.  
상업적 이용도 허용되며, 2차 창작도 가능합니다.

> ⚠ 단, 데이터 파일 이름 및 구조를 기반으로 개인을 식별할 수 없도록 모든 인적 식별 정보는 제거되어 있습니다.  
> 연구 및 교육 목적의 자유로운 활용을 권장합니다.


### 라이선스 전문

[https://creativecommons.org/licenses/by/4.0/](https://creativecommons.org/licenses/by/4.0/)


<br/>

## 데이터 노이즈 

아래와 같은 내용으로 데이터 내에  2개의 노이즈 요소가 존재한다.

<br/>

### 시제품 구조적 노이즈

시제품은 슬리퍼를 이용하여 제작했다.

<img src="../src_img/ML_B_noise.png" alt="plot01" width="500">

오른발이 다 바닥에 닿은 상태면 왼발이 바닥에 닿는 구간이 없어야 하는데 위 히트맵을 보면 왼발 엄지 부분에 값이 들어와 있는 모습을 볼 수 있다.

시제품이 슬리퍼이기에 보행 시 슬리퍼가 발에서 벗겨지지 않도록 무의식적으로 앞발이 움직이는 경우가 있고, 슬리퍼를 차면서 앞으로 보행할 때, 엄지 부분이 슬리퍼의 관성으로 밀릴 수 있기에 이런 노이즈가 발생했다고 생각한다.

<br/>

### 센서에 의한 노이즈

사용한 FSR센서는 얇은 필름형 센서이다.

문제는 이 필름형 FSR센서가 구부러지면 저항값이 변하여 센서에 데이터가 들어온다는 점이다.

그래서 센서에 휘었다가 다시 원상복구가 되는 아크릴을 붙혔지만 아크릴이 부셔지면서 필름이 원상복구가 못되고 휘어있는 상태가 지속해서 센서 데이터에 노이즈가 꼈다.


<img src="../src_img/ML_B_prototype.jpg" alt="plot01" width="500">

<img src="../src_img/ML_B_problem.jpg" alt="plot01" width="500">

프로토타입(위) 모습과 부셔진 아크릴 사진(아래)

<br/>

<img src="../src_img/ML_B_sensor_noise.jpg" alt="plot01" width="500">

위 사진과 같이 하중이 없는 상태에서도 오른발 1번 센서에 쓰레기 데이터가 들어오고 있는 모습이다.

직접 얻은 데이터의 99퍼가 노이즈가 꼈지만 다시 측정하기엔 시간이 부족해서 노이즈가 낀 데이터로 프로젝트를 진행하였다.