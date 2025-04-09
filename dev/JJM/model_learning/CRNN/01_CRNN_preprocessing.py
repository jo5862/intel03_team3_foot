

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import os

"""
spride length로 잘린 발바닥 데이터를 cmap "Greys"로 5 * 8 이미지를 생성하는 단계

데이터 값을 0, 1 MinMaxNormalization, 0 ~ 1사이의 값으로 정규화 후 히트맵 이미지로 저장하는 단계
"""


NORM_train_dir = "./data/split_train/NORM/train"
NORM_val_dir = "./data/split_train/NORM/val"
NORM_test_dir = "./data/split_train/NORM/test"
RW_train_dir = "./data/split_train/NORM/train"
RW_val_dir = "./data/split_train/NORM/val"
RW_test_dir = "./data/split_train/NORM/test"

save_NOR_train_dir = "./model_learning/CRNN/learning_data/NORM/train"
save_NOR_val_dir = "./model_learning/CRNN/learning_data/NORM/val"
save_NOR_test_dir = "./model_learning/CRNN/learning_data/NORM/test"
save_RW_train_dir = "./model_learning/CRNN/learning_data/RW/train"
save_RW_val_dir = "./model_learning/CRNN/learning_data/RW/val"
save_RW_test_dir = "./model_learning/CRNN/learning_data/RW/test"



def csv_to_heatmap(data_dir, save_dir):
    target_area_coords = [
        (3, 0), (2, 0), (1, 0),
        (3, 1), (2, 1), (1, 1), (0, 1), 
        (2, 2), (1, 2), (0, 2),  
        (1, 3), (0, 3), 
        (1, 4), (0, 4),  

        (4, 0), (5, 0), (6, 0), 
        (4, 1), (5, 1), (6, 1), (7, 1),
        (5, 2), (6, 2), (7, 2),
        (6, 3), (7, 3), 
        (6, 4), (7, 4),
    ]

    csv_files = [f for f in os.listdir(data_dir) if f.endswith(".csv")]
    if not csv_files:
        print("No CSV files found in the directory.")
        return
    
    os.makedirs(save_dir, exist_ok = True)

    index = 0

    for csv_file in csv_files:
        file_path = os.path.join(data_dir, csv_file)
        file_name = csv_file.replace(".csv", "")

        df = pd.read_csv(file_path)

        # 20구간(bin)으로 나누기
        num_bins = 20
        df_split = np.array_split(df, num_bins)

        SenL_list = [f"Sen{i}_L" for i in range(1, 15)]
        SenR_list = [f"Sen{i}_R" for i in range(1, 15)]
        CLK = "CLK"

        index += 1
        batch_dir = save_dir + "/class{:03d}".format(index)
        os.makedirs(batch_dir, exist_ok = True) 

        clk_npy = []

        for i in range(num_bins):
            SenL_values = df_split[i][SenL_list].iloc[0].values.astype(float)  # float
            SenR_values = df_split[i][SenR_list].iloc[0].values.astype(float)
            CLK_value = df_split[i][CLK].values.astype(float)
            SEN_values = np.concatenate([SenL_values.flatten(), SenR_values.flatten()]) 

            max_value = np.max(SEN_values)
            if max_value != 0:                                          # 0으로 나누는 것 방지
                SEN_values_normalized = SEN_values / max_value
            else:
                SEN_values_normalized = SEN_values


            clk_max_value = np.max(CLK_value)
            if max_value != 0:                          
                CLK_values_normalized = CLK_value / clk_max_value
            else:
                CLK_values_normalized = CLK_value           

            clk_npy.append(CLK_values_normalized[0])


            mapped_data = np.zeros((5, 8))
            for (x, y), value in zip(target_area_coords, SEN_values_normalized):
                mapped_data[y, x] = value


            plt.figure(figsize=(5, 3))


            plt.imshow(mapped_data, cmap = "Greys", aspect = "auto")
            plt.axis("off") 

            save_path = batch_dir + "/" + file_name + "_{:02d}_".format(i) + ".png"
            plt.savefig(save_path, bbox_inches = "tight", pad_inches = 0)
            plt.close() 

            print(f"Heatmap saved: {save_path}")

        npy_path = batch_dir + "/clk.npy"
        np.save(npy_path , clk_npy)







def main():
    try:
        print("NORM_train_dir")
        csv_to_heatmap(data_dir = NORM_train_dir, save_dir = save_NOR_train_dir)
        print("NORM_train_dir_Cplt!")

        print("NORM_test_dir")
        csv_to_heatmap(data_dir = NORM_val_dir, save_dir = save_NOR_val_dir)
        print("NOR_test_dir_Cplt!")

        print("NORM_test_dir")
        csv_to_heatmap(data_dir = NORM_test_dir, save_dir = save_NOR_test_dir)
        print("NORM_test_dir_Cplt!")

        print("RW_train_dir")
        csv_to_heatmap(data_dir = RW_train_dir, save_dir = save_RW_train_dir)
        print("RW_train_dir_Cplt!")

        print("RW_val_dir")
        csv_to_heatmap(data_dir = RW_val_dir, save_dir = save_RW_val_dir)
        print("RW_val_dir_Cplt!")
        
        print("RW_test_dir")
        csv_to_heatmap(data_dir = RW_test_dir, save_dir = save_RW_test_dir)
        print("RW_test_dir_Cplt!")

        return 0
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()

