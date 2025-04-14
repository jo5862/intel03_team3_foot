# 잘_걷는_도비(Walk_Scan_system)

대한상공회의소 경기인력개발원 [intel] 엣지 AI SW 아카데미 KDT훈련과정 최종 발표 프로젝트에서 FSR센서를 이용한 족저압 데이터 추출과 이를 이용한
heatmap,matplot, CNN-LSTM을 이용한 보행 정상 범위 확률 데이터를 통해 의사가 환자에게 처방 및 물리 치료 안내를 해주게하는 HW 및 SW 제작프로젝트입니다.

## 👨‍🏫프로젝트 소개
- 딥러닝을 활용한 동적 족저압 기반 보행이상 검출
    - 여러개의 압력센서 기기를 이용한 족저압 데이터추출.
    - **CNN-LSTM** 아키텍처를 활용하여 시공간적 보행 패턴 분석
    - **동적 족저압 데이터를 분석**하고 **보행 이상 검출하는 딥러닝 모델 개발.**
## ⏲️ 개발 기간
    ![image_01](images/schedule.png)
    ![use_case](images/hld_1.png)
## 🧑‍🤝‍🧑 개발자 소개
    ![image_01](images/team_member.png)
## 📌 주요 기능
    - 걸음걸이 6단계를 구분한 14개의 압력센서 기기 2개를 이용해 왼발,오른발의  무게값을 히트맵화하여 무게중심(COP)점을 확인 및 관련 데이터 이동 궤적을 학습시켜 환자의 정상 유무를 판별.
    
    ![image_02](images/outline_2.png)
    
    - 웹  UI에서 환자 이름,날짜를 입력해 환자 정보를 특정하고, 측정을 진행할 기기 연결 유/무 버튼을 통해 기기 연결을 확인하고, 측정 시작 및 중지 버튼을 통해 측정 관리를 수행.
    - 학습 데이터와 환자 데이터를 비교하여 환자의 보행 이상 정도와 데이터를 안내해주는 메세지 안내.
    
    
    - (advanced 1) 측정 결과 값을 저장 및 불러오기를 통해 측정 환자의 이전 측정 결과들을 분석하여 치료 경과를 관측.
    - (advanced 2) 챗봇 서비스와 연계하여 보행문제에 대해 간단한 상담을 진행할 수 있는 sw제작.

## High Level Design

- use case

![use_case](images/hld_1.png)

- sequence diagram
    
    ![sequences_diagram](images/hld_2.png)
    
- class diagram
    
    ![class_diagram](images/hld_3.png)
    

## Clone code


```
git clone https://github.com/jo5862/intel03_team3_foot.git

```

## Prerequite


- requirements.txt를 이용해 환경 설치

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

- openvino 설치 필요
    
    https://docs.openvino.ai/archives/index.html
    

## Steps to build

- (프로젝트를 실행을 위해 빌드 절차 기술)

```
cd ~/xxxx
source .venv/bin/activate

make
make install

```

## Steps to run

- (프로젝트 실행방법에 대해서 기술, 특별한 사용방법이 있다면 같이 기술)

```
cd ~/xxxx
source .venv/bin/activate

cd /path/to/repo/xxx/
python demo.py -i xxx -m yyy -d zzz

```

## Output

- (프로젝트 실행 화면 캡쳐)

![inital](images/output_1.png)

![device_selcet](images/output_2.png)

![print_message](images/output_3.png)

## Appendix


### 0.Data_set

[93 Human Gait (walking) Database](https://www.kaggle.com/datasets/drdataboston/93-human-gait-database?resource=download)

[요통 환자의 골반 높이 비대칭과  발바닥 압력 분포](https://m.blog.naver.com/realptman/222795018297)

### 1.AI_Model

### 2.Hard_Ware

[Taidacent 14 FSR 독립 분산 압력 감지 RX-ES39A Piezoresistive Flexible 필름 발바닥 압력 센서](https://korean.alibaba.com/product-detail/Taidacent-14-FSR-Independent-Distributed-Pressure-62014289816.html)
