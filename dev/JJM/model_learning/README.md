# 모델 학습

위 디렉토리는 모델 학습을 위해 데이터 전처리 & 모델 학습 & 모델 검증 작업이 포함되어 있습니다.


```
./model_learning/
├── basic_preprocessing/    
│   ├── 01_data_spride_cutting.py       <= 데이터 구간 나누는 작업
│   ├── 02_data_visualize.py            <= 구간을 나눈 데이터 시각화 작업업
│   ├── 03_split_train_val_test.py      <= 데이터를 8 : 1 : 1로 train : val : test로 나누는 작업업
│   └── README.md                       <= 데이터 설명 README.md
├── CRNN/
│   ├── 01_CRNN_preprocessing.py        <= CRNN 모델용 데이터 전처리
│   ├── 2_CRNN_learning                 <= CRNN 모델 학습
│   └── README.md                       <= CRNN 모델 학습 설명 README.md
├── RNN/
│   ├── 01_CRNN_preprocessing.py        <= RNN 모델용 데이터 전처리
│   ├── 2_CRNN_learning                 <= RNN 모델 학습
│   ├── 03_confusion_matrix.py          <= RNN 모델 검증
│   └── README.md                       <= RNN 모델 학습 설명 README.md
└── README.md                           <= 현재 문서 위치
```


