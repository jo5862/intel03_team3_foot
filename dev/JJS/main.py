from flask import Flask, render_template, request, jsonify
import os
import backend
app = Flask(__name__)
app.static_folder = 'static'  # 정적 파일 (CSS, JavaScript) 경로 설정

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/button_click',methods=['POST'])
def button_click():
    try:    
        data = request.get_json()
        button_id = data['button_id']

        if button_id == 'SplitCsv':
            csv_path = "./data/raw/Work_정지민(M)_B(1997-03-17)_M(2025-03-26-14-54-03).csv"  # 실제 CSV 파일 경로로 변경
            save_path = os.path.abspath("./data/spride")    
            result = backend.csv_cut_HeelStrike(csv_path,save_path)
            

            if result:
                return jsonify({'message': 'CSV 파일 분할 완료!'})
            else:
                return jsonify({'message': 'CSV 파일 분할 실패!'})
            
        elif button_id =='Raw_Graph':
            csv_path = "./data/raw/Work_정지민(M)_B(1997-03-17)_M(2025-03-26-14-54-03).csv"
            save_path = os.path.abspath("./data/raw_img")
            result = backend.csv_to_plot_raw(csv_path, save_path)

            if result:
                return jsonify({'message': 'Raw CSV 그래프 생성 완료!'})
            else:
                return jsonify({'message': 'Raw CSV 그래프 생성 실패!'})
            
        elif button_id =='Sprite_Graph':
            data_dir = os.path.abspath("./data/spride") #스프라이드 csv파일이 있는 디렉토리
            save_path = os.path.abspath("./data/spride_img")
            result = backend.csv_to_plot_spride(data_dir, save_path)

            if result:
                return jsonify({'message': 'spride CSV 그래프 생성 완료!'})
            else:
                return jsonify({'message': 'spride CSV 그래프 생성 실패!'})                
    except Exception as e:
        print(f"오류 발생: {e}")
        return jsonify({'error': str(e)})  # 에러 메시지를 JSON으로 반환

if __name__ == '__main__':
    app.run(debug=True)