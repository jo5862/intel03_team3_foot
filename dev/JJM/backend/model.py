
# pyQt5와 tensorflow 최신버전은 동시에 import를 하면 충돌이 일어나기에 코드를 격리
# DLL 오류


from tensorflow.keras import layers, models
from tensorflow.keras.utils import Sequence
from tensorflow.keras.utils import plot_model
from tensorflow.keras.models import load_model
from keras.callbacks import EarlyStopping
import pandas as pd
import numpy as np
import os




# spride data 전처리
def csv_to_npy(data_root = "./data/spride", save_root = "./data/npy"):
    ''' data_root = spride CSV 주소, 
        save_root = 저장 디렉토리
        return sequence

        speide된 csv파일을 모델에 넣기 위해 .npy 형태로 전처리 하는 단계
        '''
    os.makedirs(save_root, exist_ok=True)

    try:
        df = pd.read_csv(data_root)

        num_bins = 20
        df_split = np.array_split(df, num_bins)

        SenL_cols = [f"Sen{i}_L" for i in range(1, 15)]
        SenR_cols = [f"Sen{i}_R" for i in range(1, 15)]

        sequence = []

        for i in range(num_bins):
            senL = df_split[i][SenL_cols].iloc[0].values.astype(np.float32)
            senR = df_split[i][SenR_cols].iloc[0].values.astype(np.float32)
            values = np.concatenate([senL, senR])  # shape: (28,)

            max_val = np.max(values)
            if max_val > 1e-6:
                values = values / max_val
            else:
                values = np.zeros_like(values)

            sequence.append(values)

        sequence = np.array(sequence)  # shape: (20, 28)
        class_folder = os.path.join(save_root, "class")
        os.makedirs(class_folder, exist_ok=True)
        np.save(os.path.join(class_folder, "sequence.npy"), sequence)
        # print(f"Saved: {class_folder}/sequence.npy")
    except Exception as e:
        print(f"Error: {e}")


    return sequence



# 모델 예측
def predict_model(sequence):
    ''' sequence = csv_to_npy로 출력된 sequence
        return prob, label

        prob = float 
        label = 0, 1
        
        Normal = 0
        Right_weight = 1'''
    
    try:
        model_path = "./model/model.keras"  # 학습 완료된 모델 경로
        model = load_model(model_path, compile=False)
    except Exception as e:
        print(f"Model load fail!: {e}")

    try:
        # 모델 입력 형식에 맞게 reshape
        input_data = np.expand_dims(sequence, axis=0)  # (1, 20, 28)

        # 예측 수행
        prediction = model.predict(input_data)
        prob = prediction[0][0]
        label = 1 if prob >= 0.5 else 0

        if label == 0:
            label = "Normal"
            prob = 1 - prob
        if label == 1:
            label = "Right_weight"


        print(f"예측 확률: {prob:.4f} → 분류 결과: {label}")

    except Exception as e:
        print(f"Error: {e}")  

    return prob, label

