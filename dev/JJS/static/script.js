document.addEventListener('DOMContentLoaded', function() {
    const csvFile = document.getElementById('csvFile');
    const showGraphButton = document.getElementById('showGraphButton');
    const splitCsvButton = document.getElementById('splitCsvButton');

    // CSV 파일 선택 시 실행되는 함수
    async function handleFileSelect(event) {
        const file = event.target.files[0];

        if (file) {
            // Show Graph 버튼 활성화
            showGraphButton.disabled = false;

            // Split CSV 버튼 활성화
            splitCsvButton.disabled = false;
        } else {
            // 파일 선택 취소 시 버튼 비활성화
            showGraphButton.disabled = true;
            splitCsvButton.disabled = true;
        }
    }

    // Show Graph 버튼 클릭 시 실행되는 함수
    async function processCSV() {
        const file = csvFile.files[0];

        if (file) {
            const reader = new FileReader();
            reader.onload = async function(event) {
                const csvData = event.target.result;
                createChart(csvData); // CSV 데이터를 createChart 함수로 전달
            };
            reader.readAsText(file);
        }
    }

    async function runSplitPy() {
        const file = csvFile.files[0];
    
        if (file) {
            try {
                const formData = new FormData();
                formData.append('csv_file', file); // 파일 자체를 formData에 추가
    
                const response = await fetch('/split_csv', {
                    method: 'POST',
                    body: formData,
                });
    
                const data = await response.json();
    
                if (data.error) {
                    console.error('CSV 파일 분할 중 오류:', data.error);
                    alert('CSV 파일 분할 중 오류가 발생했습니다: ' + data.error);
                } else {
                    console.log('CSV 파일 분할 완료!', data.result);
                    alert('CSV 파일 분할 완료!');
                }
            } catch (error) {
                console.error('split_csv 엔드포인트 호출 중 오류:', error);
                alert('CSV 파일 분할 중 오류가 발생했습니다.');
            }
        } else {
            alert('CSV 파일을 먼저 선택해주세요.');
        }
    }
    
    let myChart;

    async function createChart(csvData) {
        const parseCSV = (csv) => {
            const lines = csv.split('\n');
            const headers = lines[0].split(',');
            const data = [];

            for (let i = 1; i < lines.length; i++) {
                const values = lines[i].split(',');
                if (!values[0]) continue; // 빈 라인 처리
                const entry = {};
                for (let j = 0; j < headers.length; j++) {
                    entry[headers[j].trim()] = values[j].trim();
                }
                data.push(entry);
            }
            return { headers, data };
        };

        const { headers, data } = parseCSV(csvData);

        const datasets = [];
        for (let i = 1; i < headers.length; i++) {
            const header = headers[i].trim();
            const isRightSensor = header.includes('_R');
            datasets.push({
                label: header,
                data: data.map(row => parseFloat(row[header])),
                borderColor: `hsl(${i * 20}, 100%, 50%)`,
                borderWidth: 1,
                borderDash: isRightSensor ? [5, 5] : [],
                tension: 0.4,
                pointRadius: 0
            });
        }

        const ctx = document.getElementById('copChart').getContext('2d'); // 캔버스 ID 변경

        // 기존 차트 파괴
        if (myChart) {
            myChart.destroy();
        }

        // Chart.js가 로드되었는지 확인
        if (typeof Chart !== 'undefined') {
            myChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.map(row => row.Time),
                    datasets: datasets
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        } else {
            console.error('Chart.js가 로드되지 않았습니다.');
            alert('Chart.js가 로드되지 않았습니다. 페이지를 다시 로드해주세요.');
        }
    }

    // CSV 파일 선택 입력 요소에 이벤트 리스너 추가
    csvFile.addEventListener('change', handleFileSelect);

    window.processCSV = processCSV;
    window.runSplitPy = runSplitPy;

        //CSV파일을 읽어서 general info에 뿌리는코드
        csvFile.addEventListener('change', function(event) {
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
    let slowerButton = document.getElementById("slower-button");
    let fasterButton = document.getElementById("faster-button");
    let frameSlider = document.getElementById("frame-slider");
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