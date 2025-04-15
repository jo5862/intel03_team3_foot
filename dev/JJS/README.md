# FSR 센서 데이터 분석 및 보행 패턴 인식 프로젝트

## 개요

본 프로젝트는 FSR(Force Sensitive Resistor) 센서로부터 수집된 CSV 데이터를 가공하여 사용자의 보행 패턴을 분석하고, 그 결과를 시각화하여 웹 기반 사용자 인터페이스에 제공합니다. AI 모델을 활용하여 보행 패턴을 정상과 오른쪽 편중으로 분류하고, 그 결과를 웹 UI에서 확인할 수 있습니다.

## 주요 기능

* **CSV 데이터 전처리:**
    * 오른발 뒤꿈치 접지(Heel Strike)를 기준으로 CSV 파일을 스프라이드(보폭) 단위로 분할합니다. [`webui_backend.py`](webui_backend.py)
    * 분할된 CSV 파일은 지정된 디렉토리에 저장됩니다. [`webui_backend.py`](webui_backend.py)
* **데이터 시각화:**
    * 원시 CSV 데이터 전체에 대한 센서 값 변화를 선 그래프로 시각화합니다. [`webui_backend.py`](webui_backend.py)
    * 스프라이드 단위로 분할된 CSV 데이터에 대한 센서 값 변화를 선 그래프로 시각화합니다. [`webui_backend.py`](webui_backend.py)
    * 스프라이드 단위의 센서 데이터를 히트맵 이미지로 변환하여 보행 중 압력 분포를 시각적으로 표현합니다. [`webui_backend.py`](webui_backend.py)
    * 생성된 히트맵 이미지를 웹 UI에서 애니메이션 형태로 확인할 수 있습니다. [`webui_js`](webui_js)
* **AI 모델 학습 및 예측:**
    * 스프라이드 단위의 CSV 데이터를 **AI 모델의 입력 형태(NumPy 배열)**로 전처리합니다. [`webui_backend.py`](webui_backend.py)
    * 학습된 RNN(Recurrent Neural Network) 모델을 이용하여 보행 패턴을 **'Normal'(정상) 또는 'Right\_weight'(오른쪽 편중)**으로 분류하고, 각 분류에 대한 확률 값을 출력합니다. [`webui_backend.py`](webui_backend.py)
* **웹 UI 환경:**
    * Flask 프레임워크를 사용하여 웹 서버를 구축하고 사용자 인터페이스를 제공합니다. [`webui_main.py`](webui_main.py)
    * 사용자는 웹 UI를 통해 CSV 데이터 파일을 로드, 데이터 분할, 그래프 및 히트맵 시각화, AI 모델 예측 등의 기능을 수행할 수 있습니다. [`webui_html`](webui_html), [`webui_js`](webui_js)
    * 웹 UI는 환자 정보 표시, 의료 기록 조회, 히트맵 애니메이션 제어 등의 기능을 포함합니다. [`webui_html`](webui_html), [`webui_js`](webui_js)

## 파일 구조

* `webui_backend.py`: 데이터 전처리, 시각화, AI 모델 예측 관련 백엔드 Python 코드
* `webui_main.py`: Flask 웹 서버 실행 및 HTTP 요청 처리 코드
* `webui_html`: 웹 UI의 HTML 구조
* `webui_style.css`: 웹 UI의 스타일 정의 (CSS)
* `webui_js`: 웹 UI의 동적인 동작 처리 (JavaScript)
* `./data/raw/`: 원본 CSV 데이터 저장 디렉토리 (예시: `Work_정지민(M)_B(1997-03-17)_M(2025-03-26-14-54-03).csv`) [`webui_main.py`](webui_main.py)
* `./data/spride/`: 분할된 스프라이드 단위 CSV 파일 저장 디렉토리 [`webui_backend.py`](webui_backend.py)
* `./data/npy/`: AI 모델 학습을 위한 NumPy 배열 데이터 저장 디렉토리 [`webui_backend.py`](webui_backend.py)
* `./data/heatmap/`: 생성된 히트맵 이미지 저장 디렉토리 [`webui_backend.py`](webui_backend.py)
* `./data/raw_img/`: 원시 데이터 그래프 이미지 저장 디렉토리 [`webui_backend.py`](webui_backend.py)
* `./data/spride_img/`: 스프라이드 데이터 그래프 이미지 저장 디렉토리 [`webui_backend.py`](webui_backend.py)
* `./modelRNN/model.h5`: 학습된 AI 모델 파일 [`webui_backend.py`](webui_backend.py)
* `./static/`: CSS 및 JavaScript 등 정적 파일 저장 디렉토리 [`webui_main.py`](webui_main.py)
* `./templates/`: Flask 템플릿 파일 저장 디렉토리 (예: `index.html`) [`webui_main.py`](webui_main.py)

## 필요 조건

* Python 3.x
* Python 라이브러리:
    * `tensorflow >= 2.0` [`webui_backend.py`](webui_backend.py)
    * `keras` (`tensorflow.keras`) [`webui_backend.py`](webui_backend.py)
    * `pandas` [`webui_backend.py`](webui_backend.py)
    * `numpy` [`webui_backend.py`](webui_backend.py)
    * `matplotlib` [`webui_backend.py`](webui_backend.py)
    * `Flask` [`webui_main.py`](webui_main.py)
* 웹 브라우저

## 설치 및 실행 방법

1.  **필수 라이브러리 설치:**
    ```bash
    pip install tensorflow pandas numpy matplotlib Flask
    ```
2.  **데이터 디렉토리 생성:** 프로젝트 루트 디렉토리에 `data`, `data/raw`, `data/spride`, `data/npy`, `data/heatmap`, `data/raw_img`, `data/spride_img`, `modelRNN` 디렉토리를 생성합니다.
    ```bash
    mkdir data
    mkdir data/raw
    mkdir data/spride
    mkdir data/npy
    mkdir data/heatmap
    mkdir data/raw_img
    mkdir data/spride_img
    mkdir modelRNN
    ```
3.  **학습된 AI 모델 파일 준비:** `./modelRNN/` 디렉토리에 학습된 AI 모델 파일 `model.h5`를 위치시킵니다.
4.  **원본 CSV 데이터 준비:** 분석할 FSR 센서 CSV 데이터 파일을 `./data/raw/` 디렉토리에 저장합니다. 예시 파일명: `Work_XXX(M)_B(1997-03-17)_M(2025-03-26-14-54-03).csv`.
5.  **웹 UI 실행:** 프로젝트 루트 디렉토리에서 다음 명령어를 실행합니다.
    ```bash
    python webui_main.py
    ```
6.  **웹 브라우저 접속:** 웹 브라우저를 열고 `http://127.0.0.1:5000/` 주소로 접속합니다.

## 사용 방법

1.  **데이터 로드:** 웹 페이지 좌측 상단의 "Load Data" 섹션에서 CSV 파일을 선택하고 로드합니다. 로드된 CSV 파일의 General Info가 화면에 표시됩니다. [`webui_js`](webui_js)
2.  **CSV 분할:** "Split CSV" 버튼을 클릭하여 로드된 CSV 파일을 오른발 뒤꿈치 접지를 기준으로 스프라이드 단위로 분할합니다. 분할된 파일은 `./data/spride/` 디렉토리에 저장됩니다. [`webui_main.py`](webui_main.py)
3.  **그래프 확인:**
    * "Show Graph" 섹션의 "Raw\_graph" 버튼을 클릭하여 원본 CSV 데이터의 평균 센서 값 변화 그래프를 확인합니다. 생성된 이미지는 `./data/raw_img/` 디렉토리에 저장됩니다. [`webui_main.py`](webui_main.py)
    * "Sprite\_Graph" 버튼을 클릭하여 분할된 스프라이드 CSV 데이터의 평균 센서 값 변화 그래프를 확인합니다. 생성된 이미지는 `./data/spride_img/` 디렉토리에 저장됩니다. [`webui_main.py`](webui_main.py)
4.  **히트맵 확인:** "Heat Map" 섹션에서 히트맵 애니메이션을 확인할 수 있습니다. 애니메이션 컨트롤을 이용하여 재생/일시정지, 속도 조절, 순환 주기 선택 등이 가능합니다. 히트맵 이미지는 `./data/heatmap/` 디렉토리에 저장됩니다. [`webui_js`](webui_js)
5.  **모델 예측:** "Load Model" 버튼을 클릭한 후 (현재는 파일 선택 기능 없음) 히트맵이 생성되면 자동으로 AI 모델이 예측을 수행하고 결과를 화면에 표시합니다. [`webui_backend.py`](webui_backend.py) "Button 4" 또는 "Button 5" 등의 버튼을 통해 개별 스프라이드에 대한 예측을 수행할 수도 있습니다 (구현에 따라 다름). [`webui_js`](webui_js)
6.  **의료 기록 확인:** "Medical Record" 섹션의 "[image: Show Medical Record]" 버튼을 클릭하여 의료 기록 팝업을 확인합니다. [`webui_html.txt`](webui_html.txt), [`webui_js`](webui_js.txt)
7.  **Cycle 선택:** "Choose Cycle" 섹션에서 특정 보행 주기를 선택하여 해당 주기의 히트맵 애니메이션을 확인할 수 있습니다. [`webui_html.txt`](webui_html.txt), [`webui_js`](webui_js.txt)
8.  **Memo:** 텍스트 영역에 메모를 작성할 수 있습니다. [`webui_html`](webui_html)

## AI 모델

본 프로젝트에서는 RNN(Recurrent Neural Network) 기반의 AI 모델을 사용하여 보행 패턴을 분류합니다. 모델은 입력된 보행 시퀀스 데이터를 기반으로 'Normal'(정상) 또는 **'Right\_weight'(오른쪽 편중)**의 두 가지 클래스로 분류하고, 각 클래스에 대한 예측 확률을 제공합니다. 학습된 모델 파일 `model.h5`는 `./modelRNN/` 디렉토리에 위치해야 합니다.

## 추가 개선 사항 (선택 사항)

* 더욱 다양한 보행 이상 패턴 분류 모델 개발 및 통합
* 사용자별 보행 데이터 관리 및 이력 조회 기능 추가
* AI 모델 재학습 기능 추가
* 웹 UI 디자인 및 사용자 경험 개선
* 실시간 센서 데이터 스트리밍 및 분석 기능 추가
