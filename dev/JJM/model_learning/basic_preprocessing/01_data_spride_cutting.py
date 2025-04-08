
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

"""
raw csv 데이터를 Heel Strike 기준으로 자르는 작업입니다.

Heel Strike 기준은 "Sen13_R", "Sen_14R" 의 값의 합이 임계점 K 이상이면 해당 지점을 기준으로
다음 Heel Strike 전 까지 자르는 spride length 기준으로 데이터를 자를 수 있습니다.

02_data_visualize.py 와 병행하여 자른 csv파일을 시각화하여 직접 전처리를 진행합니다.
데이터를 직접 보고 전처리 해야하기에 직접 해당 파일 이름을 입력하고 진행해야 합니다.


data_name = "정OO_L(NORM)_G(M)_A(28)_M(2025-03-26-14-54-03)" 라고 가정하면

파일은 
"정OO_L(NORM)_G(M)_A(28)_M(2025-03-26-14-54-03)_01.csv"
"정OO_L(NORM)_G(M)_A(28)_M(2025-03-26-14-54-03)_02.csv"
"정OO_L(NORM)_G(M)_A(28)_M(2025-03-26-14-54-03)_03.csv"

위 형식으로 저장됩니다.
"""


# 파일 경로 지정
data_name = "DATA_NAME"
data_format = ".csv"

data_root = "./data/"
data_folder = "raw/right_weight/"
save_folder = data_root + "temp/raw_spride"
csv_path = data_root + data_folder + data_name + data_format

os.makedirs(save_folder, exist_ok=True)

K = 0
index = 0
flag = False
heel_strike = 0


# 파일 csv 불러오기기
df = pd.read_csv(csv_path)

num_rows = df.shape[0]                  # (행 개수, 열 개수) 튜플에서 첫 번째 값 가져오기
print("행 개수:", num_rows)             # 2 ~ n - 1 => n - 2


# Heel Strike 기준으로 자르기기
for row in range(num_rows):
    heel_value = df.loc[row, ["Sen13_R", "Sen14_R"]].sum()

    if flag == False and heel_value > K:
        flag = True

        index += 1

        df_split = df.loc[heel_strike - 1 : row - 1]
        save_path = data_root + save_folder + data_name + "_{:02d}".format(index) + data_format
        df_split.to_csv(save_path)
        print("{:02d} 저장 완료!".format(index))
        heel_strike = row

    
    if flag == True and heel_value == 0:
        flag = False


        


