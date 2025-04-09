
from tensorflow.keras import layers, models
from tensorflow.keras.utils import Sequence
from tensorflow.keras.utils import plot_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import matplotlib.pyplot as plt
import os

"""
tensorflow == 2.13.0 버전을 사용해야 합니다.
최신버전 사용시 pyQt5를 사용하는 APP.py에서 DLL오류가 발생합니다.
"""


class HeatmapSequenceLoader(Sequence):
    def __init__(self, root_dirs, label_map, batch_size=8, image_size=(64, 64), seq_len=20):
        self.batch_size = batch_size
        self.image_size = image_size
        self.seq_len = seq_len
        self.data = []

        for root_dir in root_dirs:
            label = label_map[root_dir]  # NORM : 0 , RW : 1
            class_folders = [os.path.join(root_dir, d) for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))]
            for folder in class_folders:
                self.data.append((folder, label))

        self.data.sort()

    def __len__(self):
        return len(self.data) // self.batch_size

    def __getitem__(self, idx):
        batch_data = self.data[idx * self.batch_size:(idx + 1) * self.batch_size]
        X, y = [], []

        for folder_path, label in batch_data:
            images = sorted([f for f in os.listdir(folder_path) if f.endswith('.png')])[:self.seq_len]
            sequence = []

            for img_file in images:
                img = load_img(os.path.join(folder_path, img_file), target_size=self.image_size, color_mode='grayscale')
                img_array = img_to_array(img) / 255.0
                sequence.append(img_array)

            X.append(sequence)
            y.append(label)

        return np.array(X), np.array(y)




def build_CRNN_pool_model(input_shape=(20, 64, 64, 1), lstm_units=64, num_classes=1):
    model = models.Sequential()

    # CNN (TimeDistributed)
    model.add(layers.TimeDistributed(layers.Conv2D(16, (3, 3), activation='relu', padding='same',
                                                    input_shape = input_shape )))
    model.add(layers.TimeDistributed(layers.MaxPooling2D((2, 2))))
    model.add(layers.TimeDistributed(layers.Conv2D(32, (3, 3), activation='relu', padding='same')))
    model.add(layers.TimeDistributed(layers.Flatten()))

    # LSTM
    model.add(layers.LSTM(lstm_units, return_sequences=True))
    model.add(layers.LSTM(32))
    model.add(layers.Dense(32, activation='relu'))
    model.add(layers.Dense(num_classes, activation='sigmoid'))
    # model.add(layers.Dense(num_classes, activation='softmax'))

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    # model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model



def build_CRNN_non_pool_model(input_shape = (20, 5, 8, 1), lstm_units = 64, num_classes = 1):
    model = models.Sequential()

    # CNN 적용 (TimeDistributed)
    model.add(layers.TimeDistributed(layers.Conv2D(16, (3, 3), strides=1, activation='relu', padding='same',
                                                    input_shape = input_shape )))
    model.add(layers.TimeDistributed(layers.Conv2D(32, (3, 3), strides=1, activation='relu', padding='same')))
    model.add(layers.TimeDistributed(layers.Conv2D(64, (3, 3), strides=1, activation='relu', padding='same')))

    model.add(layers.TimeDistributed(layers.Flatten()))

    # LSTM
    model.add(layers.LSTM(lstm_units, return_sequences=True))
    model.add(layers.LSTM(32))
    model.add(layers.Dense(32, activation='relu'))
    model.add(layers.Dense(num_classes, activation='sigmoid'))
    # model.add(layers.Dense(num_classes, activation='softmax'))

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    # model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model


def sanity_model():
    model = models.Sequential([
        layers.Input(shape=(20, 64, 64, 1)),
        layers.TimeDistributed(layers.Flatten()),
        layers.LSTM(32),
        layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model


def model_train(epochs=50, save_dir='./model_output', use_pool=True):
    os.makedirs(save_dir, exist_ok=True)

    train_dirs = ["./data/split_train/NORM/train", "./data/split_train/RW/train"]
    val_dirs  = ["./data/split_train/NORM/val", "./data/split_train/RW/val"]

    label_map = {
        "./data/split_train/NORM/train": 0,
        "./data/split_train/RW/train": 1,
        "./data/split_train/NORM/val": 0,
        "./data/split_train/RW/val": 1
    }

    train_generator = HeatmapSequenceLoader(train_dirs, label_map, batch_size=8)
    test_generator = HeatmapSequenceLoader(val_dirs, label_map, batch_size=8)


    if use_pool:
        model = build_CRNN_pool_model(input_shape=(20, 64, 64, 1))
    else:
        model = build_CRNN_non_pool_model(input_shape=(20, 64, 64, 1))


    history = model.fit(train_generator, validation_data=test_generator, epochs=epochs)
    plot_model(model, to_file= "./model/src_img/model_01.png" , show_shapes=True)

    model_path = os.path.join(save_dir, "model.keras")
    model.save(model_path)
    print(f"모델 저장 완료: {model_path}")

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




if __name__ == '__main__':
    model_train(epochs=10, save_dir='./model/', use_pool=False)
    print("Modle learning Cplt")


