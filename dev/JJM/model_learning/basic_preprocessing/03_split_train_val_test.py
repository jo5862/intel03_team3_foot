
import os
import shutil
from sklearn.model_selection import train_test_split



# 데이터 경로 설정
data_root = "Clean_Data_path"
save_root = "./data/split_train/NORM/"
# save_root = "./data/split_train/RW/"


# 저장할 디렉토리 경로
train_dir = os.path.join(save_root, "train")
val_dir   = os.path.join(save_root, "val")
test_dir  = os.path.join(save_root, "test")

# 폴더 생성
os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

all_files = [f for f in os.listdir(data_root) if f.endswith(".csv")]

# 1차 분할: train 80% vs temp 20%
train_files, temp_files = train_test_split(
    all_files, test_size=0.2, random_state=42
)

# 2차 분할: temp => val 10% + test 10%
val_files, test_files = train_test_split(
    temp_files, test_size=0.5, random_state=42
)

# 파일 이동
def move_files(file_list, target_dir):
    for file in file_list:
        src_path = os.path.join(data_root, file)
        dest_path = os.path.join(target_dir, file)
        shutil.move(src_path, dest_path)

# 이동 실행
move_files(train_files, train_dir)
move_files(val_files, val_dir)
move_files(test_files, test_dir)

# 결과 출력
print(f"전체 파일 개수: {len(all_files)}")
print(f"훈련(train) 파일 개수: {len(train_files)}")
print(f"검증(val) 파일 개수: {len(val_files)}")
print(f"테스트(test) 파일 개수: {len(test_files)}")
