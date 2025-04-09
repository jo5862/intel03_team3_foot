

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


"""
Heel Strike 기준으로 잘린 데이터를 합 평균 시각화 하는 작업입니다.

데이터가 보행상태의 연속된 데이터만 있는 상태가 아니라 아래와 같은 구간이 포함되어 있습니다.

- 정지 구간
- 연속적으로 걷기 전 가속하는 구간
- 걷는 구간
- 감속 후 정지 구간

- 혹은 센서 데이터가 튀는 구간
- 혹은 센서 데이터를 받지 못해 결측치가 존재하는 구간

"""



def visualize_mean(csv_path, save_dir):
    try:
        filename = os.path.splitext(os.path.basename(csv_path))[0]

        df = pd.read_csv(csv_path)

        SenL_list = [f"Sen{i}_L" for i in range(1, 15)]
        SenR_list = [f"Sen{i}_R" for i in range(1, 15)]
        CLK = "CLK"

        df["SenL_Mean"] = df[SenL_list].mean(axis=1)
        df["SenR_Mean"] = df[SenR_list].mean(axis=1)

        plt.figure(figsize=(12, 6))
        plt.plot(df[CLK], df["SenL_Mean"], label = str(SenL_list),  linestyle = 'solid')
        plt.plot(df[CLK], df["SenR_Mean"], label = str(SenR_list),  linestyle = 'dashed')
        plt.xlabel("CLK")
        plt.ylabel("Sensor Value")
        plt.title(f"Gait Visualization: {filename}")
        plt.grid(True)
        plt.legend()

        save_path = os.path.join(save_dir, f"{filename}.png")
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Saved: {save_path}")

    except Exception as e:
        print("e")


def main():
    data_root = "./data/temp/raw_spride"
    save_root = "./data/temp/visualize"
    os.makedirs(save_root, exist_ok=True)

    csv_files = [f for f in os.listdir(data_root) if f.endswith(".csv")]

    if not csv_files:
        print("files found.")
        return

    for file in csv_files:
        full_path = os.path.join(data_root, file)
        visualize_mean(full_path, save_root)


if __name__ == '__main__':
    main()

