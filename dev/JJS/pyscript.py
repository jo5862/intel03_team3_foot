import pandas as pd
from pyweb import pydom
from pyodide.http import open_url
from pyscript import display
from js import console,document
import time
page_message = "This example loads a remote CSV file into a Pandas dataframe, and displays it."
url = "https://raw.githubusercontent.com/datasets/airport-codes/master/data/airport-codes.csv"

pydom["div#page-message"].html = page_message
pydom["input#txt-url"][0].value = url

def log(message):
    print(message)
    console.log(message)

def animate_images():
    image_index = 0
    image_urls = [f"./img/foot_img/{i}.jpg" for i in range(12)]  # 이미지 URL 목록 생성 (0.jpg ~ 10.jpg)

    def update_image():
        nonlocal image_index # nonlocal 변수 사용
        try:
            img_element = document.querySelector("#my-image")
            img_element.src = image_urls[image_index]
            image_index = (image_index + 1) % len(image_urls)  # 다음 이미지 인덱스 계산
        except Exception as e:
            console.warn(f"Error loading image: {e}")

        time.sleep(0.2) # 0.2초 간격으로 이미지 변경

    while True:
        update_image()

def loadFromURL(event):
    pydom["div#pandas-output-inner"].html = ""
    url = pydom["input#txt-url"][0].value

    log(f"Trying to fetch CSV from {url}")

    df = pd.read_csv(open_url(url))
    df = df.head(3)  # 처음 15개 행만 표시 (숫자 조정 가능)

    display(df, target="pandas-output-inner", append="False")
    animate_images()  # CSV 로드 후 이미지 애니메이션 시작

