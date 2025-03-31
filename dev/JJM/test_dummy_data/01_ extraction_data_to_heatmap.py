
# 히트맵 이미지에서 데이터를 추출하고 다운스케일하여 저장하는 코드입니다.


import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize



# 'turbo' cmap을 사용하는 heatmap에서 데이터 추출 함수수
def extract_values_from_jet_heatmap(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # BGR -> RGB

    # turbo 컬러맵 정의 (0에서 1로 매핑)
    turbo_colormap = cm.get_cmap('turbo', 256)
    color_range = np.linspace(0, 1, 256)

    # 이미지 크기 가져오기
    h, w, _ = image.shape
    scalar_values = np.zeros((h, w), dtype = np.float32)

    # 각 픽셀에 대해 가장 가까운 색상 매칭
    for i in range(h):
        for j in range(w):
            pixel = image[i, j]  # RGB 픽셀 값
            if (pixel[0] == 0 or pixel[1] == 0 or pixel[2] == 0):  # 하나 이상이 0인 경우만

                # RGB 값에 대해 turbo 컬러맵에서 가장 가까운 색상 찾기
                closest_index = np.argmin(np.linalg.norm(turbo_colormap(color_range)[:, :3] - pixel / 255.0, axis = 1))

                # 가장 가까운 색상의 인덱스를 이용해 색상에 해당하는 스칼라 값 추출
                scalar_values[i, j] = color_range[closest_index]

    return scalar_values



# 이미지를 그리드로 다운스케일, 각 그리드에서 최대값 추출
def downscale_image_to_grid(image, target_width, target_height):
    original_height, original_width = image.shape
    grid_height = target_height
    grid_width = target_width
    block_size_y = original_height // grid_height
    block_size_x = original_width // grid_width
    
    downscaled_image = np.zeros((grid_height, grid_width), dtype = np.float32)
    
    for i in range(grid_height):
        for j in range(grid_width):
            y_start = i * block_size_y
            y_end = (i + 1) * block_size_y if i < grid_height - 1 else original_height
            x_start = j * block_size_x
            x_end = (j + 1) * block_size_x if j < grid_width - 1 else original_width
            block = image[y_start:y_end, x_start:x_end]
            downscaled_image[i, j] = np.max(block)
    
    return downscaled_image



# 0 이상의 값 마스킹
def mask_value(image):
    h, w = image.shape
    mask = np.zeros_like(image, dtype = bool)

    for i in range(h):
        for j in range(w):
            if image[i, j] > 0:
                mask[i, j] = True

    return mask



# 마스크된 영역만 출력하는 함수
def apply_mask_to_heatmap(scalar_values, mask, i):
    # 마스크를 적용하여 영역만 남기기
    masked_values = np.ma.masked_where(mask == False, scalar_values)
    
    norm = Normalize(vmin = 0, vmax = 1)

    save_path = "./dev/JJM/test_dummy_data/result_img/{:03d}.png".format(i)

    # 정규화 없이 그대로 출력 (vmin과 vmax 설정)
    plt.imshow(masked_values, cmap = "turbo", interpolation = 'nearest', norm = norm)
    plt.colorbar()
    plt.savefig(save_path, dpi = 300, bbox_inches = 'tight')
    plt.show()
    plt.close()



def main():
    try:
        for i in range(1, 13):
            # 1번부터 12번까지의 이미지 경로
            image_path = "./dev/JJM/test_dummy_data/test_img/{:03d}.png".format(i)
                
            scalar_values = extract_values_from_jet_heatmap(image_path)

            # max값을 기준으로 정규화
            downscaled_values = downscale_image_to_grid(scalar_values, 40, 31)
            mask = mask_value(downscaled_values)
            print(f"Processing {image_path}")

            # 마스크된 영역만 히트맵 출력
            apply_mask_to_heatmap(downscaled_values, mask, i)

        print("Process completed.")
        
    except Exception as e:
        print(f"Error: {e}")



if __name__ == '__main__':
    main()



