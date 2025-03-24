import os
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from sklearn.model_selection import train_test_split
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt

# 이미지 로딩 함수
def load_images(normal_dir, wrong_dir, image_size=(40, 31)):
    images = []
    labels = []

    # 정상 데이터 로드
    for csv_file in os.listdir(normal_dir):
        if csv_file.endswith(".png"):  # PNG 파일을 이미지로 읽어들임
            image_path = os.path.join(normal_dir, csv_file)
            img = load_img(image_path, target_size=image_size, color_mode='rgb')  # 이미지가 RGB 형식으로 로드
            img = img_to_array(img) / 255.0  # 이미지를 배열로 변환하고 정규화
            images.append(img)
            labels.append(0)  # 정상 데이터는 0으로 레이블링

    # 비정상 데이터 로드
    for csv_file in os.listdir(wrong_dir):
        if csv_file.endswith(".png"):  # PNG 파일을 이미지로 읽어들임
            image_path = os.path.join(wrong_dir, csv_file)
            img = load_img(image_path, target_size=image_size, color_mode='rgb')  # 이미지가 RGB 형식으로 로드
            img = img_to_array(img) / 255.0  # 이미지를 배열로 변환하고 정규화
            images.append(img)
            labels.append(1)  # 비정상 데이터는 1로 레이블링

    images = np.array(images)
    labels = np.array(labels)
    return images, labels

# CNN 모델 생성 함수
def create_model(input_shape):
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(128, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2)))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))  # 이진 분류이므로 sigmoid 사용

    model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])
    return model

# 경로 설정
normal_image_dir = "C:/workspace/foot_pressure_image/augmented_heatmap"
wrong_image_dir = "C:/workspace/foot_pressure_image/wrong_heatmap"

# 데이터 로드
images, labels = load_images(normal_image_dir, wrong_image_dir)

# 데이터셋 분할
X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.2, random_state=42)

# 모델 생성
model = create_model(input_shape=X_train.shape[1:])

# 데이터 증강 설정
datagen = ImageDataGenerator(
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

# 모델 학습
datagen.fit(X_train)

history = model.fit(
    datagen.flow(X_train, y_train, batch_size=32),
    validation_data=(X_test, y_test),
    epochs=10
)

# 모델 평가
test_loss, test_acc = model.evaluate(X_test, y_test, verbose=2)
print(f"Test accuracy: {test_acc}")

# 모델 저장
model.save("foot_pressure_model.h5")  # 모델을 'foot_pressure_model.h5'라는 파일로 저장

# 모델 로드 (추후에 모델을 사용하려면)
loaded_model = load_model("foot_pressure_model.h5")  # 저장된 모델을 로드

# 학습 과정 시각화
plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['val_accuracy'], label = 'val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim([0, 1])
plt.legend(loc='lower right')
plt.show()
