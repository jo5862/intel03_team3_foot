import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.colors import Normalize

def augment_csv(input_csv, output_csv_path, num_augments=10, wrong_data=False):
    # 디렉토리 경로 생성 (경로 중복 문제 해결)
    output_dir = os.path.dirname(output_csv_path)
    os.makedirs(output_dir, exist_ok=True)

    # CSV 파일 읽기
    df = pd.read_csv(input_csv)

    for aug_num in range(num_augments):
        augmented_df = df.copy()

        # 좌표 이동 및 압력 값 증강
        shift_x = np.random.randint(-1, 2) if not wrong_data else np.random.randint(-5, 6)  # X축 이동
        shift_y = np.random.randint(-1, 2) if not wrong_data else np.random.randint(-5, 6)  # Y축 이동
        pressure_scale = np.random.uniform(0.9, 1.1)  # 압력 0.9배 ~ 1.1배
        noise = np.random.normal(0, 0.02, size=len(augmented_df))  # 압력 노이즈 추가

        if wrong_data:  # 틀린 데이터 생성 (이동 범위와 압력 값 조정)
            pressure_scale = np.random.uniform(0.3, 2.0)  # 비정상적으로 압력값을 크게 조정 (0.3 ~ 2.0)
            noise = np.random.normal(0, 0.2, size=len(augmented_df))  # 더 많은 노이즈 추가

            # 비정상적인 패턴을 추가
            wrong_pattern_x = np.random.randint(0, 40)
            wrong_pattern_y = np.random.randint(0, 31)
            augmented_df.loc[augmented_df["X"] == wrong_pattern_x, "Pressure"] = np.random.uniform(1.2, 2.0)  # 특정 영역에 강한 압력 값 추가

        augmented_df["X"] = augmented_df["X"] + shift_x
        augmented_df["Y"] = augmented_df["Y"] + shift_y
        augmented_df["Pressure"] = (augmented_df["Pressure"] * pressure_scale) + noise

        # 이미지 크기(40x31) 넘지 않도록 클리핑
        augmented_df["X"] = augmented_df["X"].clip(0, 39)
        augmented_df["Y"] = augmented_df["Y"].clip(0, 30)
        augmented_df["Pressure"] = augmented_df["Pressure"].clip(0, 1)  # 압력 값은 0~1 범위로 제한

        # 증강된 CSV 저장
        save_path = output_csv_path.format(aug_num)
        augmented_df.to_csv(save_path, index=False)
        print(f"Saved augmented CSV: {save_path}")


def generate_heatmap_from_csv(csv_file, output_image_path, wrong_data=False):
    # 디렉토리 경로 생성 (경로 중복 문제 해결)
    output_dir = os.path.dirname(output_image_path)
    os.makedirs(output_dir, exist_ok=True)

    # CSV 데이터로 히트맵 초기화
    df = pd.read_csv(csv_file)
    heatmap = np.zeros((31, 40), dtype=np.float32)

    # 압력 데이터를 히트맵에 반영 (각 좌표의 압력값을 그대로 반영)
    for _, row in df.iterrows():
        x, y, pressure = int(row["X"]), int(row["Y"]), row["Pressure"]
        heatmap[y, x] = pressure

    # 틀린 데이터를 구별하기 위해 압력 값과 위치를 크게 조정
    if wrong_data:
        # 비정상적인 압력 값을 추가하여 쉽게 구별되도록
        wrong_x = np.random.randint(0, 40)
        wrong_y = np.random.randint(0, 31)
        heatmap[wrong_y, wrong_x] = np.random.uniform(1.2, 2.0)  # 압력을 아주 높게 설정

        # 비정상적인 패턴을 히트맵에 추가
        wrong_pattern_x = np.random.randint(0, 40)
        wrong_pattern_y = np.random.randint(0, 31)
        heatmap[wrong_pattern_y, wrong_pattern_x] = np.random.uniform(1.2, 2.0)  # 특정 패턴을 강하게 조정

    # 히트맵 시각화 및 저장
    norm = Normalize(vmin=0, vmax=1)
    heatmap[heatmap == 0] = np.nan  # 압력이 없는 부분은 NaN 처리

    plt.imshow(heatmap, cmap="turbo", interpolation='nearest', norm=norm)
    plt.axis('off')  # 좌표 제거
    plt.savefig(output_image_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Saved augmented heatmap: {output_image_path}")


if __name__ == '__main__':
    try:
        input_csv_dir = "C:/workspace/foot_pressure_image/csv"
        augmented_csv_dir = "C:/workspace/foot_pressure_image/augmented_csv"
        augmented_heatmap_dir = "C:/workspace/foot_pressure_image/augmented_heatmap"

        # 틀린 데이터 저장 경로
        wrong_csv_dir = "C:/workspace/foot_pressure_image/wrong_csv"
        wrong_heatmap_dir = "C:/workspace/foot_pressure_image/wrong_heatmap"

        num_original_files = 10  # 원본 CSV 파일 수
        num_augments_per_file = 50  # 각 CSV 파일당 10개의 증강 데이터 생성
        num_wrong_augments_per_file = 50  # 각 파일당 틀린 데이터 증강 10개

        # 각 원본 CSV 파일에 대해 증강 수행
        for i in range(1, num_original_files + 1):
            input_csv = os.path.join(input_csv_dir, f"{i:03d}.csv")
            output_csv_template = os.path.join(augmented_csv_dir, f"{i:03d}_{{}}.csv")

            print(f"Augmenting {input_csv}")
            augment_csv(input_csv, output_csv_template, num_augments=num_augments_per_file)

            # 증강된 CSV로부터 히트맵 생성
            for aug_num in range(num_augments_per_file):
                augmented_csv = output_csv_template.format(aug_num)
                output_heatmap = os.path.join(augmented_heatmap_dir, f"{i:03d}_{aug_num}.png")
                generate_heatmap_from_csv(augmented_csv, output_heatmap)

            # 틀린 데이터 증강 (잘못된 CSV와 히트맵 저장)
            wrong_csv_template = os.path.join(wrong_csv_dir, f"{i:03d}_wrong_{aug_num}.csv")
            for aug_num in range(num_wrong_augments_per_file):
                augment_csv(input_csv, wrong_csv_template, num_augments=1, wrong_data=True)

                # 틀린 데이터로부터 히트맵 생성
                wrong_augmented_csv = wrong_csv_template.format(aug_num)
                output_wrong_heatmap = os.path.join(wrong_heatmap_dir, f"{i:03d}_wrong_{aug_num}.png")
                generate_heatmap_from_csv(wrong_augmented_csv, output_wrong_heatmap, wrong_data=True)

        print("Data augmentation and heatmap generation completed.")

    except Exception as e:
        print(f"Error: {e}")
