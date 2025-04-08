import sys
import os
import shutil
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
                             QFileDialog, QListWidget, QHBoxLayout, QTextEdit)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
from backend.backend import csv_cut_HeelStrike, csv_to_plot_raw, csv_to_plot_spride


class FootPressureApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Foot Pressure Analysis")
        self.resize(800, 1200)

        self.csv_path = None
        self.split_csv_paths = []
        self.current_selected_csv = None

        self.heatmap_index = 0
        self.heatmap_timer = QTimer()
        self.heatmap_timer.timeout.connect(self.update_heatmap_preview)
        self.heatmap_running = False

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # CSV 선택
        self.load_btn = QPushButton("CSV 불러오기")
        self.load_btn.clicked.connect(self.load_csv)
        layout.addWidget(self.load_btn)

        # 그래프 출력용 이미지
        self.plot_label = QLabel("그래프 이미지 표시 영역")
        self.plot_label.setFixedHeight(400)
        self.plot_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.plot_label)

        # 나누기 + 리스트
        split_layout = QHBoxLayout()
        self.split_btn = QPushButton("Heel Strike 기준으로 나누기")
        self.split_btn.clicked.connect(self.split_csv)

        self.csv_list = QListWidget()
        self.csv_list.itemClicked.connect(self.select_csv_from_list)

        split_layout.addWidget(self.split_btn)
        split_layout.addWidget(self.csv_list)
        layout.addLayout(split_layout)

        # 검증 버튼
        self.validate_btn = QPushButton("검증하기")
        self.validate_btn.clicked.connect(self.validate_csv)
        self.validate_btn.setEnabled(False)             # CSV 선택 전에는 비활성화
        layout.addWidget(self.validate_btn)

        # 히트맵 생성 및 재생 정지 버튼
        self.heatmap_btn = QPushButton("히트맵 생성 및 미리보기")
        self.heatmap_btn.clicked.connect(self.generate_heatmap)
        layout.addWidget(self.heatmap_btn)

        self.toggle_btn = QPushButton("▶ 히트맵 재생")
        self.toggle_btn.clicked.connect(self.toggle_heatmap_play)
        layout.addWidget(self.toggle_btn)

        # 히트맵 미리보기 이미지
        self.heatmap_label = QLabel("히트맵 미리보기")
        self.heatmap_label.setFixedHeight(400)
        self.heatmap_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.heatmap_label)

        # 검증 결과 출력
        self.result_text = QTextEdit()
        layout.addWidget(self.result_text)

        self.setLayout(layout)

    def load_csv(self):
        file_dialog = QFileDialog()
        self.csv_path, _ = file_dialog.getOpenFileName(self, "CSV 파일 선택", "", "CSV Files (*.csv)")
        if self.csv_path:
            csv_to_plot_raw(self.csv_path, "./temp")
            pixmap = QPixmap("./temp/raw.png")
            self.plot_label.setPixmap(pixmap.scaled(self.plot_label.size(), Qt.KeepAspectRatio))

    def split_csv(self):
        if not self.csv_path:
            return

        shutil.rmtree("./data/spride", ignore_errors=True)
        os.makedirs("./data/spride", exist_ok=True)

        csv_cut_HeelStrike(self.csv_path, "./data/spride")

        self.csv_list.clear()
        self.split_csv_paths = []
        for f in sorted(os.listdir("./data/spride")):
            if f.endswith(".csv"):
                full_path = os.path.join("./data/spride", f)
                self.split_csv_paths.append(full_path)
                self.csv_list.addItem(f)

    def select_csv_from_list(self, item):
        from backend import backend
        filename = item.text()
        self.current_selected_csv = os.path.join("./data/spride", filename)
    
        backend.csv_to_plot_spride(self.current_selected_csv, "./temp")
    
        pixmap = QPixmap("./temp/spride.png")
        if pixmap.isNull():
            print("[!] spride.png 이미지 로드 실패")
        else:
            self.plot_label.setPixmap(pixmap.scaled(self.plot_label.size(), Qt.KeepAspectRatio))
            print("[✓] spride.png 표시 완료")

        self.validate_btn.setEnabled(True)


    def validate_csv(self):
        if not self.current_selected_csv or not os.path.exists(self.current_selected_csv):
            self.result_text.append("[!] 먼저 분할된 CSV 중 하나를 선택하세요.")
            return

        from backend import model
        print(f"선택된 CSV 경로: {self.current_selected_csv}")
        sequence = model.csv_to_npy(self.current_selected_csv, "./data/npy")

        if sequence is None:
            self.result_text.append("[!] sequence 생성 실패. CSV 내용 확인 필요.")
            return

        prob, label = model.predict_model(sequence)
        self.result_text.setText(f"예측 결과: {label} (확률: {prob:.4f})")

    def generate_heatmap(self):
        if not self.current_selected_csv:
            self.result_text.append("[!] 먼저 CSV를 선택하세요.")
            return

        import backend 
        backend.heatmap(self.current_selected_csv, "./data/heatmap")
        # model.heatmap(self.current_selected_csv, "./data/heatmap")
        self.result_text.append("[✓] 히트맵 이미지 20장 생성 완료!")

        self.heatmap_index = 0
        self.heatmap_running = True
        self.heatmap_timer.start(1000)
        self.toggle_btn.setText("⏸ 히트맵 정지")

    def update_heatmap_preview(self):
        image_path = os.path.join("./data/heatmap", f"Heatmap_{self.heatmap_index:02d}.png")
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            self.heatmap_label.setPixmap(pixmap.scaled(self.heatmap_label.size(), Qt.KeepAspectRatio))
            self.heatmap_index = (self.heatmap_index + 1) % 20
        else:
            self.heatmap_timer.stop()
            self.result_text.append("[!] 히트맵 이미지 로드 실패")

    def toggle_heatmap_play(self):
        if self.heatmap_running:
            self.heatmap_timer.stop()
            self.toggle_btn.setText("▶ 히트맵 재생")
        else:
            self.heatmap_timer.start(1000)
            self.toggle_btn.setText("⏸ 히트맵 정지")
        self.heatmap_running = not self.heatmap_running

    def closeEvent(self, event):
        self.heatmap_timer.stop()
        shutil.rmtree("./temp", ignore_errors=True)
        shutil.rmtree("./data/spride", ignore_errors=True)
        shutil.rmtree("./data/spride_img", ignore_errors=True)
        shutil.rmtree("./data/npy", ignore_errors=True)
        shutil.rmtree("./data/heatmap", ignore_errors=True)
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FootPressureApp()
    window.show()
    sys.exit(app.exec_())
