from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
import pandas as pd
import logging
import traceback

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.static_folder = 'static'
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

def split_csv(csvpath):
    try:
        # 파일 경로 정규화
        csvpath = os.path.normpath(csvpath)

        # temp_data 디렉토리가 없으면 생성
        temp_data_dir = os.path.join(os.path.dirname(csvpath), "temp_data")  # csvpath와 같은 디렉토리에 temp_data 생성
        if not os.path.exists(temp_data_dir):
            os.makedirs(temp_data_dir)

        data_format=".csv"
        index = 0
        flag = False
        heel_strike = 0

        df = pd.read_csv(csvpath)
        logger.info("CSV 파일 읽기 완료!")

        num_rows = df.shape[0]                  # (행 개수, 열 개수) 튜플에서 첫 번째 값 가져오기
        logger.info(f"행 개수: {num_rows}")  # 행 개수 로깅

        data_name = os.path.basename(csvpath).replace('.csv', '')  # 파일명만 추출

        for row in range(num_rows):
            heel_value = df.loc[row, ["Sen13_R", "Sen14_R"]].sum()

            if flag == False and heel_value > 0:
                flag = True

                index += 1

                df_split = df.loc[heel_strike - 1: row - 1]
                save_path = os.path.join(temp_data_dir, f"{data_name}_{index:02d}.csv")  # temp_data 폴더에 저장
                df_split.to_csv(save_path, index=False)  # index 저장 안함
                logger.info(f"{index:02d} 저장 완료!")
                logger.info(f"{save_path}저장 경로")
                heel_strike = row


            if flag == True and heel_value == 0:
                flag = False
        logger.info("CSV 파일 분할 완료!")
        return "CSV 파일 분할 완료!"
    
    except Exception as e:
        logger.exception("split_csv 함수 실행 중 오류:")
        return str(e)

@app.route('/split_csv', methods=['POST'])
def split_csv_route():
    if 'csv_file' not in request.files:
        return jsonify({'error': '파일이 없습니다.'})

    file = request.files['csv_file']

    if file.filename == '':
        return jsonify({'error': '파일 이름이 없습니다.'})

    try:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
    except Exception as e:
        return jsonify({'error': f'파일 저장 중 오류 발생: {str(e)}'})

    try:
        result = split_csv(file_path)  # split_csv 함수 직접 호출
        return jsonify({'result': result})
    except Exception as e:
        logger.exception("split_csv_route 함수 실행 중 오류:")
        return jsonify({'error': str(e)})

@app.route('/get_image/<filename>')
def get_image(filename):
    return send_from_directory(os.path.join(app.root_path, 'static', 'img'), filename)

if __name__ == '__main__':
    app.run(debug=True)