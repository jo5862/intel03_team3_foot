import pandas as pd
from pyweb import pydom
from pyodide.http import open_url
from pyscript import display
from js import console,document, setInterval



page_message = "This example."
url = "https://raw.githubusercontent.com/datasets/airport-codes/master/data/airport-codes.csv"

image_urls = [f"./img/foot_img/{i:03d}.png" for i in range(1, 13)]  # 이미지 URL 목록 생성 (001.png ~ 012.png)
image_index = 0

pydom["div#page-message"].html = page_message
pydom["input#txt-url"][0].value = url

def log(message):
    # log to pandas dev console
    print(message)
    # log to JS console
    console.log(message)

def loadFromURL(event):
    pydom["div#pandas-output-inner"].html = ""
    url = pydom["input#txt-url"][0].value

    log(f"Trying to fetch CSV from {url}")
    df = pd.read_csv(open_url(url))

    pydom["div#pandas-output"].style["display"] = "block"
    df= df.head(3)

    display(df, target="pandas-output-inner", append="False")


def animate_image():
    global image_index
    img_element = document.getElementById("animated-image")
    img_element.src = image_urls[image_index]
    image_index = (image_index + 1) % len(image_urls)

def start_animation(event):
    console.log("Starting image animation");
    setInterval(animate_image, 200)  # 200ms 간격으로 이미지 변경