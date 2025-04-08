import os
import numpy as np
import math
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import Sequence
from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score
import matplotlib.pyplot as plt
import seaborn as sns


"""
혼동 모델 출력 코드
"""


class SimpleNpySequenceLoader(Sequence):
    def __init__(self, root_dirs, batch_size=8):
        self.batch_size = batch_size
        self.data = []

        for path in root_dirs:
            for root, _, files in os.walk(path):
                label = 0 if "NOR" in root else 1 
                for f in files:
                    full_path = os.path.join(root, f)
                    if f == "sequence.npy" and os.path.isfile(full_path):
                        try:
                            arr = np.load(full_path)
                            if arr.shape == (20, 28):
                                self.data.append((full_path, label))
                            else:
                                print(f"무시됨 (shape={arr.shape}): {full_path}")
                        except Exception as e:
                            print(f"로딩 실패: {full_path} - {e}")

        self.data.sort()
        print(f"\n총 유효한 테스트 시퀀스: {len(self.data)}")

    def __len__(self):
        return max(1, math.ceil(len(self.data) / self.batch_size))

    def __getitem__(self, idx):
        batch = self.data[idx * self.batch_size:(idx + 1) * self.batch_size]
        X, y = [], []

        for file_path, label in batch:
            try:
                arr = np.load(file_path)
                if arr.shape == (20, 28):
                    X.append(arr)
                    y.append(label)
            except Exception as e:
                print(f"{file_path} 로딩 실패: {e}")
                continue
        print(X, y)
        if not X:
            return np.empty((0, 20, 28)), np.empty((0,))

        return np.array(X, dtype=np.float32), np.array(y, dtype=np.int32)


model_path = "./model/model.keras"
test_dirs = ["./model_learning/RNN/learning_data/NORM/test", "./model_learning/RNN/learning_data/RW/test"]

print("모델 로딩 중...")
model = load_model(model_path)
print("모델 로드 완료!")


test_gen = SimpleNpySequenceLoader(test_dirs, batch_size=8)


print("\n테스트 데이터 예측 시작...")
X_all = []
y_all = []
# print("debug01")


for i, (X_batch, y_batch) in enumerate(test_gen):
    if len(X_batch) == 0:
        break
    X_all.append(X_batch)
    y_all.append(y_batch)
    # print("debug02")


X_all = np.concatenate(X_all, axis=0)
y_all = np.concatenate(y_all, axis=0)
print(f"총 테스트 샘플: {X_all.shape[0]}")


print("\n모델 예측 중...")
y_probs = model.predict(X_all, batch_size=8).flatten()
y_pred = (y_probs > 0.5).astype(int)


print("\n[혼동 행렬]")
print(confusion_matrix(y_all, y_pred))

print("\n[분류 리포트]")
print(classification_report(y_all, y_pred, target_names=["NOR", "RW"]))

auc = roc_auc_score(y_all, y_probs)
print(f"\nROC AUC Score: {auc:.4f}")


conf_mat = confusion_matrix(y_all, y_pred)
plt.figure(figsize=(6, 5))
sns.heatmap(conf_mat, annot=True, fmt='d', cmap="Blues", xticklabels=["NOR", "RW"], yticklabels=["NOR", "RW"])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.tight_layout()
plt.savefig("./model/confusion_matrix.png")
plt.show()
print("혼동 행렬 저장 완료: ./model/confusion_matrix.png")
