
import pandas as pd
import numpy as np
import os

"""

"""

# 디렉토리 설정
NORM_train_dir = "./data/split_train/NORM/train"
NORM_val_dir = "./data/split_train/NORM/val"
NORM_test_dir = "./data/split_train/NORM/test"
RW_train_dir = "./data/split_train/NORM/train"
RW_val_dir = "./data/split_train/NORM/val"
RW_test_dir = "./data/split_train/NORM/test"

save_NOR_train_dir = "./model_learning/RNN/learning_data/NORM/train"
save_NOR_val_dir = "./model_learning/RNN/learning_data/NORM/val"
save_NOR_test_dir = "./model_learning/RNN/learning_data/NORM/test"
save_RW_train_dir = "./model_learning/RNN/learning_data/RW/train"
save_RW_val_dir = "./model_learning/RNN/learning_data/RW/val"
save_RW_test_dir = "./model_learning/RNN/learning_data/RW/test"


def csv_to_sequence_npy(data_dir, save_dir):
    os.makedirs(save_dir, exist_ok=True)

    csv_files = [f for f in os.listdir(data_dir) if f.endswith(".csv")]
    index = 0

    for csv_file in csv_files:
        path = os.path.join(data_dir, csv_file)
        df = pd.read_csv(path)

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
        class_folder = os.path.join(save_dir, f"class{index:03d}")
        os.makedirs(class_folder, exist_ok=True)
        np.save(os.path.join(class_folder, "sequence.npy"), sequence)
        index += 1
        print(f"Saved: {class_folder}/sequence.npy")



def main():
    try:
        print("NOR_train_dir")
        csv_to_sequence_npy(data_dir=NORM_train_dir, save_dir=save_NOR_train_dir)
        print("NOR_train_dir_Cplt!")

        print("NOR_val_dir")
        csv_to_sequence_npy(data_dir=NORM_val_dir, save_dir=save_NOR_val_dir)
        print("NOR_val_dir_Cplt!")

        print("NOR_test_dir")
        csv_to_sequence_npy(data_dir=NORM_test_dir, save_dir=save_NOR_test_dir)
        print("NOR_test_dir_Cplt!")

        print("RW_train_dir")
        csv_to_sequence_npy(data_dir=RW_train_dir, save_dir=save_RW_train_dir)
        print("RW_train_dir_Cplt!")

        print("RW_val_dir")
        csv_to_sequence_npy(data_dir=RW_val_dir, save_dir=save_RW_val_dir)
        print("RW_val_dir_Cplt!")

        print("RW_test_dir")
        csv_to_sequence_npy(data_dir=RW_test_dir, save_dir=save_RW_test_dir)
        print("RW_test_dir_Cplt!")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()



