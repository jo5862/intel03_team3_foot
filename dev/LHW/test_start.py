import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from matplotlib import cm
from matplotlib.colors import Normalize


def extract_values_from_jet_heatmap(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    turbo_colormap = cm.get_cmap('turbo', 256)
    color_range = np.linspace(0, 1, 256)

    h, w, _ = image.shape
    scalar_values = np.zeros((h, w), dtype=np.float32)

    for i in range(h):
        for j in range(w):
            pixel = image[i, j]
            if (pixel[0] == 0 or pixel[1] == 0 or pixel[2] == 0):
                closest_index = np.argmin(np.linalg.norm(turbo_colormap(color_range)[:, :3] - pixel / 255.0, axis=1))
                scalar_values[i, j] = color_range[closest_index]

    return scalar_values


def downscale_image_to_grid(image, target_width, target_height):
    original_height, original_width = image.shape
    block_size_y = original_height // target_height
    block_size_x = original_width // target_width

    downscaled_image = np.zeros((target_height, target_width), dtype=np.float32)

    for i in range(target_height):
        for j in range(target_width):
            y_start = i * block_size_y
            y_end = (i + 1) * block_size_y if i < target_height - 1 else original_height
            x_start = j * block_size_x
            x_end = (j + 1) * block_size_x if j < target_width - 1 else original_width
            block = image[y_start:y_end, x_start:x_end]
            downscaled_image[i, j] = np.max(block)

    return downscaled_image


def mask_value(image):
    return image > 0


def apply_mask_to_heatmap(scalar_values, mask, i):
    masked_values = np.ma.masked_where(mask == False, scalar_values)

    norm = Normalize(vmin=0, vmax=1)

    heatmap_save_path = f"C:/workspace/foot_pressure_image/heatmap/{i:03d}.png"
    csv_save_path = f"C:/workspace/foot_pressure_image/csv/{i:03d}.csv"

    os.makedirs(os.path.dirname(heatmap_save_path), exist_ok=True)
    os.makedirs(os.path.dirname(csv_save_path), exist_ok=True)

    plt.imshow(masked_values, cmap="turbo", interpolation='nearest', norm=norm)
    plt.colorbar()
    plt.savefig(heatmap_save_path, dpi=300, bbox_inches='tight')
    plt.close()

    data = []
    for y in range(scalar_values.shape[0]):
        for x in range(scalar_values.shape[1]):
            if mask[y, x]:
                data.append([x, y, scalar_values[y, x]])

    df = pd.DataFrame(data, columns=["X", "Y", "Pressure"])
    df.to_csv(csv_save_path, index=False)

    print(f"Saved heatmap: {heatmap_save_path}")
    print(f"Saved CSV: {csv_save_path}")


def reconstruct_heatmap_from_csv(i):
    csv_path = f"C:/workspace/foot_pressure_image/csv/{i:03d}.csv"
    save_path = f"C:/workspace/foot_pressure_image/gait_sample/{i:03d}.png"

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    df = pd.read_csv(csv_path)

    heatmap = np.zeros((31, 40), dtype=np.float32)  # 40x31 크기의 히트맵 초기화

    for _, row in df.iterrows():
        x, y, pressure = int(row["X"]), int(row["Y"]), row["Pressure"]
        heatmap[y, x] = pressure  # 좌표에 pressure 값 할당

    norm = Normalize(vmin=0, vmax=1)
    heatmap[heatmap == 0] = np.nan
    plt.imshow(heatmap, cmap="turbo", interpolation='nearest', norm=norm)
    plt.colorbar()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Reconstructed heatmap saved: {save_path}")


if __name__ == '__main__':
    try:
        for i in range(1, 11):
            image_path = f"C:/workspace/foot_pressure_image/images/{i}.png"

            scalar_values = extract_values_from_jet_heatmap(image_path)
            downscaled_values = downscale_image_to_grid(scalar_values, 40, 31)
            mask = mask_value(downscaled_values)

            print(f"Processing {image_path}")

            apply_mask_to_heatmap(downscaled_values, mask, i)

            # CSV 파일을 다시 히트맵으로 변환
            reconstruct_heatmap_from_csv(i)

        print("Process completed.")

    except Exception as e:
        print(f"Error: {e}")
