


from tensorflow.keras import layers, models
from tensorflow.keras.utils import Sequence
from tensorflow.keras.utils import plot_model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from keras.callbacks import EarlyStopping
import numpy as np
import matplotlib.pyplot as plt
import os


"""
tensorflow == 2.13.0 버전을 사용해야 합니다.
최신버전 사용시 pyQt5를 사용하는 APP.py에서 DLL오류가 발생합니다.
"""



class SimpleNpySequenceLoader(Sequence):
    def __init__(self, root_dirs, label_map, batch_size=8):
        self.batch_size = batch_size
        self.data = []

        for path in root_dirs:
            label = label_map[path]
            for root, _, files in os.walk(path):
                for f in files:
                    if f == "sequence.npy":
                        self.data.append((os.path.join(root, f), int(label)))

        self.data.sort()

    def __len__(self):
        return max(1, len(self.data) // self.batch_size)

    def __getitem__(self, idx):
        batch = self.data[idx * self.batch_size:(idx + 1) * self.batch_size]
        X, y = [], []

        for file_path, label in batch:
            arr = np.load(file_path)            # shape: (20, 28)
            X.append(arr)
            y.append(label)

        X = np.array(X, dtype=np.float32)       # shape: (batch_size, 20, 28)
        y = np.array(y, dtype=np.int32)         # shape: (batch_size,)
        return X, y



def build_lstm_model(input_shape=(20, 28)):
    model = models.Sequential()
    model.add(layers.Input(shape=input_shape))
    model.add(layers.LSTM(64, return_sequences=True))
    model.add(layers.LSTM(64))
    model.add(layers.Dense(32, activation='relu'))
    model.add(layers.Dense(1, activation='sigmoid'))

    optimizer = Adam(learning_rate=0.001, clipnorm=1.0)
    model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])
    return model



def model_train(epochs=50, save_dir='./model_output'):
    os.makedirs(save_dir, exist_ok=True)

    train_dirs = ["./data/npy/NOR/train", "./data/npy/RW/train"]
    val_dirs  = ["./data/npy/NOR/val", "./data/npy/RW/val"]
    label_map = {d: 0 if "NOR" in d else 1 for d in train_dirs + val_dirs}

    train_gen = SimpleNpySequenceLoader(train_dirs, label_map, batch_size=8)
    test_gen  = SimpleNpySequenceLoader(val_dirs, label_map, batch_size=8)

    model = build_lstm_model(input_shape=(20, 28))
    early_stopping = EarlyStopping(monitor = 'val_accuracy', patience = 7)
    history = model.fit(train_gen, validation_data=test_gen, epochs=epochs, callbacks = [early_stopping])

    plot_model(model, to_file= "./model/src_img/model_01.png" , show_shapes=True)

    model.save("./model/model.keras")
    print("모델 저장 완료:")

    plt.figure(figsize=(10, 4))

    # Accuracy
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='accuracy')
    plt.title('Training Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.grid(True)
    plt.legend()

    # Loss
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='loss', color='orange')
    plt.title('Training Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.grid(True)
    plt.legend()

    plot_path = os.path.join(save_dir, "src_img/model_02.png")
    plt.savefig(plot_path)
    plt.close()

    plt.figure(figsize=(10, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(history.history['val_accuracy'], label='val_accuracy')
    plt.title('Val Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.grid(True)
    plt.legend()

    # Loss
    plt.subplot(1, 2, 2)
    plt.plot(history.history['val_loss'], label='val_loss', color='orange')
    plt.title('Val Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.grid(True)
    plt.legend()

    plot_path = os.path.join(save_dir, "src_img/model_03.png")
    plt.savefig(plot_path)
    plt.close()


    print(f"학습 그래프 저장 완료: {plot_path}")



if __name__ == '__main__':
    model_train(epochs=10, save_dir='./model')
    print("Modle learning Cplt")





