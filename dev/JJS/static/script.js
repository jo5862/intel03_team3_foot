document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('file-input');
    const showGraphButton = document.getElementById('showGraphButton');
    const splitCsvButton = document.getElementById('splitCsvButton');


    async function callPythonFunction(functionName) {
        try {
            const response = await fetch('/button_click', { // 서버 엔드포인트 URL
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ button_id: functionName })  // 실행할 함수 이름을 JSON으로 보냄
            });
    
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
    
            const data = await response.json();
            console.log('Python function result:', data); // Python 함수 실행 결과 처리
    
            if (data.error) {
                console.error('Python function error:', data.error);
                document.getElementById('output').textContent = 'Error occurred: ' + data.error;
            } else {
                // (선택 사항) 결과를 HTML에 표시
                document.getElementById('output').textContent = data.message;
            }
    
        } catch (error) {
            console.error('Error calling Python function:', error);
            document.getElementById('output').textContent = 'Error occurred. See console.';
        }
    }
    
    window.callPythonFunction = callPythonFunction; // 전역 스코프에서 접근 가능하도록 설정
        //CSV파일을 읽어서 general info에 뿌리는코드
        fileInput.addEventListener('change', function(event) {
            const file = event.target.files[0];

            if (file) {
                Papa.parse(file, {
                    header: true,
                    dynamicTyping: true,
                    skipEmptyLines: true,
                    trimHeaders: true,
                    complete: function(results) {

                        console.log(results); // results 객체 확인
                        const data = results.data[0];

                        console.log(data); // 데이터 확인

                        // General Info 업데이트
                        document.getElementById("name").innerText = data.Name || "";
                        document.getElementById("sex").innerText = data.Sex || "";
                        document.getElementById("birth").innerText = data.Birth || "";
                        document.getElementById("location").innerText = data.Location || "";
                        document.getElementById("id").innerText = data.Id || "";

                        // Disorders Info 업데이트
                        document.getElementById("physical").innerText = data.Physical || "";
                        document.getElementById("speech").innerText = data.Speech || "";
                        document.getElementById("cognitive").innerText = data.Cognitive || "";
                    },
                    error: function(error) {
                        console.error("Error parsing CSV:", error.message);
                    }
                });
            }
        });
        

    const showRecordButton = document.getElementById("show-record-button");
    const recordPopup = document.getElementById("record-popup");
    const closeButton = document.querySelector(".close-button");

    showRecordButton.addEventListener("click", () => {
        recordPopup.style.display = "block"; // 팝업 표시
    });

    closeButton.addEventListener("click", () => {
        recordPopup.style.display = "none"; // 팝업 숨김
    });

    window.addEventListener("click", (event) => {
        if (event.target == recordPopup) {
            recordPopup.style.display = "none"; // 팝업 영역 밖 클릭 시 팝업 닫기
        }
    });

    const imgElement = document.getElementById("animated-image");
    const playPauseButton = document.getElementById("play-pause-button");
    const reverseButton = document.getElementById("reverse-button");
    const slowerButton = document.getElementById("slower-button");
    const fasterButton = document.getElementById("faster-button");
    const frameSlider = document.getElementById("frame-slider");
    const currentFrame = document.getElementById("current-frame");
    const totalFrames = document.getElementById("total-frames");

    const dir1Button = document.getElementById("dir1-button");
    const dir2Button = document.getElementById("dir2-button");
    const dir3Button = document.getElementById("dir3-button");

    let imageIndex2 = 1;
    const imageCount2 = 12;
    let isPlaying = false;
    let isReversed = false;
    let intervalId;
    let animationSpeed = 200;
    let currentDirectory = ""; // 디렉토리 초기화
    const initialImage = "./img/image.png"; // 초기 이미지 경로
    imgElement.src = initialImage; // 초기 이미지 설정

    // 컨트롤 버튼 비활성화 함수
    function disableControls() {
        playPauseButton.disabled = true;
        reverseButton.disabled = true;
        slowerButton = true;
        fasterButton = true;
        frameSlider = true;
    }

    // 컨트롤 버튼 활성화 함수
    function enableControls() {
        playPauseButton.disabled = false;
        reverseButton.disabled = false;
        slowerButton.disabled = false;
        fasterButton.disabled = false;
        frameSlider.disabled = false;
    }

    totalFrames.innerText = imageCount2;

    function updateImage2() {
        const imageUrl = `${currentDirectory}${String(imageIndex2).padStart(3, '0')}.png`;
        imgElement.src = imageUrl;
        currentFrame.innerText = imageIndex2;
        frameSlider.value = imageIndex2;
    }

    function playAnimation() {
        if (!isPlaying) {
            isPlaying = true;
            playPauseButton.innerText = "⏹";
            intervalId = setInterval(() => {
                if (isReversed) {
                    imageIndex2--;
                    if (imageIndex2 < 1) {
                        imageIndex2 = imageCount2;
                    }
                } else {
                    imageIndex2++;
                    if (imageIndex2 > imageCount2) {
                        imageIndex2 = 1;
                    }
                }
                updateImage2();
            }, animationSpeed);
        } else {
            pauseAnimation();
        }
    }

    function pauseAnimation() {
        isPlaying = false;
        playPauseButton.innerText = "▶";
        clearInterval(intervalId);
    }

    function slowerAnimation() {
        animationSpeed *= 2;
        if (isPlaying) {
            pauseAnimation();
            playAnimation();
        }
    }

    function fasterAnimation() {
        animationSpeed /= 2;
        if (isPlaying) {
            pauseAnimation();
            playAnimation();
        }
    }

    function reverseAnimation() {
        imageIndex2 = 1;
        updateImage2();
        pauseAnimation()
    }

    function setDirectory(directory) {
        currentDirectory = directory;
        imageIndex2 = 1; // 디렉토리 변경 시 첫 번째 이미지로 초기화
        imgElement.src = initialImage; // 초기 이미지 설정
        updateImage2();
        enableControls();
    }

    playPauseButton.addEventListener("click", playAnimation);
    reverseButton.addEventListener("click",reverseAnimation);
    slowerButton.addEventListener("click", slowerAnimation);
    fasterButton.addEventListener("click", fasterAnimation);

    dir1Button.addEventListener("click", () => setDirectory(dir1Button.dataset.dir));
    dir2Button.addEventListener("click", () => setDirectory(dir2Button.dataset.dir));
    dir3Button.addEventListener("click", () => setDirectory(dir3Button.dataset.dir));

    frameSlider.addEventListener("input", () => {
        imageIndex2 = parseInt(frameSlider.value);
        updateImage2();
        pauseAnimation();
    });
    disableControls();
});