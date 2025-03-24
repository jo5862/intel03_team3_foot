import os
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model


# 이미지 로딩 함수
def load_images(image_paths, image_size=(40, 31)):
    images = []
    for image_path in image_paths:
        img = load_img(image_path, target_size=image_size, color_mode='rgb')  # 이미지를 RGB로 로드
        img = img_to_array(img) / 255.0  # 이미지를 배열로 변환하고 정규화
        images.append(img)
    return np.array(images)

# 이미지 예측 함수
def predict_images(model, image_paths):
    images = load_images(image_paths)
    predictions = model.predict(images)
    return predictions

# 경로 설정
normal_image_dir = "C:/workspace/foot_pressure_image/augmented_heatmap/"
wrong_image_dir = "C:/workspace/foot_pressure_image/wrong_heatmap/"

# 정상 이미지 001_0부터 001_10까지, 비정상 이미지 001_0부터 001_10까지 지정
normal_image_files = [os.path.join(normal_image_dir, f"005_{i}.png") for i in range(11)]  # 정상 이미지 0~10
wrong_image_files = [os.path.join(wrong_image_dir, f"005_wrong_{i}.png") for i in range(11)]  # 비정상 이미지 0~10

# 선택된 이미지 경로 출력
print("Selected Normal Images:", normal_image_files)
print("Selected Wrong Images:", wrong_image_files)

# 모델 로드 (이미 학습된 모델을 로드)
model = load_model('foot_pressure_model.h5')

# 예측 수행
normal_predictions = predict_images(model, normal_image_files)
wrong_predictions = predict_images(model, wrong_image_files)

# 예측 결과 출력
print("\nNormal Images Predictions:")
for i, (image_path, prediction) in enumerate(zip(normal_image_files, normal_predictions)):
    print(f"Image {i + 1}: Predicted {'Normal' if prediction < 0.5 else 'Wrong'}, Confidence: {prediction[0]}")

    # 예측한 이미지를 시각화
    img = load_img(image_path, target_size=(40, 31), color_mode='rgb')
    plt.imshow(img)
    plt.title(f"Prediction: {'Normal' if prediction < 0.5 else 'Wrong'}")
    plt.show()

print("\nWrong Images Predictions:")
for i, (image_path, prediction) in enumerate(zip(wrong_image_files, wrong_predictions)):
    print(f"Image {i + 1}: Predicted {'Normal' if prediction < 0.5 else 'Wrong'}, Confidence: {prediction[0]}")

    # 예측한 이미지를 시각화
    img = load_img(image_path, target_size=(40, 31), color_mode='rgb')
    plt.imshow(img)
    plt.title(f"Prediction: {'Normal' if prediction < 0.5 else 'Wrong'}")
    plt.show()
