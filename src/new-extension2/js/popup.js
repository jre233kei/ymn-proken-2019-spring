
var data = []


document.addEventListener('DOMContentLoaded', function () {
    // (Inside the click listener)
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        chrome.tabs.executeScript(tabs[0].id, { file: "js/content.js" }, function (data) {
            // Data is an array of values, in case it was executed in multiple tabs/frames
            // download(data[0], "download.html", "text/html");
            document.getElementById("title").textContent = data[0];

            console.log(data[0])

            console.log(data[0].replace(/\r?\n/g, ' '));
            axios.defaults.headers['Content-Type'] = 'text/plain;charset=utf-8';

            axios.post('https://g8kwped00b.execute-api.us-east-1.amazonaws.com/production', {
                text: encodeURIComponent(data[0].replace(/\r?\n/g, ' '))
            }).then(response => {
                console.log(response["data"]["body"]);
                
                drawCanvas(response["data"]["body"]);
            }).catch(error => {
                alert(error);
            });;

        });
    });
});

function drawCanvas (res) {
    formatGraphData(res);
    //document.getElementById("cr-label").style.display = 'flex';
    var ctx = document.getElementById("canvas").getContext("2d");
    var myBar = new Chart(ctx, {
        type: 'bar',                           //◆棒グラフ
        data: {                                //◆データ
            labels: ['1', '2', '3', '4', '5'],     //ラベル名
            datasets: [{                       //データ設定
                data: data,          //データ内容
                backgroundColor: '#00adb5'   //背景色
            }]
        },
        options: {                             //◆オプション
            responsive: true,                  //グラフ自動設定
            legend: {                          //凡例設定
                display: false,                //表示設定
                fontColor: "#eeeeee"
            },
            title: {                           //タイトル設定
                display: false,                 //表示設定
                fontSize: 8,                  //フォントサイズ
                text: 'タイトル'                //ラベル
            },
            scales: {                          //軸設定
                yAxes: [{                      //y軸設定
                    display: true,             //表示設定
                    scaleLabel: {              //軸ラベル設定
                        display: false,          //表示設定
                        labelString: '確率',  //ラベル
                        fontSize: 8               //フォントサイズ
                    },
                    ticks: {                      //最大値最小値設定
                        min: 0,                   //最小値
                        max: 0.5,                  //最大値
                        fontSize: 8,             //フォントサイズ
                        stepSize: 0.2,               //軸間隔
                        fontColor: "#eeeeee",
                        ticksColor: "#eeeeee"
                    },
                }],
                xAxes: [{                         //x軸設定
                    display: true,                //表示設定
                    barPercentage: 0.4,           //棒グラフ幅
                    categoryPercentage: 1.8,      //棒グラフ幅
                    scaleLabel: {                 //軸ラベル設定
                        display: false,             //表示設定
                        labelString: 'Star',  //ラベル
                        fontSize: 8,               //フォントサイズ
                        fontColor: "#eeeeee"
                    },
                    ticks: {
                        fontSize: 11,             //フォントサイズ
                        fontColor: "#eeeeee"
                    },
                }],
            },
            layout: {                             //レイアウト
                padding: {                          //余白設定
                    left: 100,
                    right: 50,
                    top: 0,
                    bottom: 0
                }
            }
        }
    });
}

function formatGraphData (input) {
    res = []
    //input = "(b'__label__1, 0.275391 __label__3, 0.207031 __label__2, 0.199219 __label__4, 0.197266 __label__5, 0.115234\n', b'')"
    console.log(input.replace("(b'", "").replace("\n', b'')", "").split(' '))
    fstr = input.replace("(b'", "").replace("\n', b'')", "").split(' ');
    for (i = 0; i < 10; i++) {
        if (i % 2 === 0) {
            ii = fstr[i].replace("__label__", "").replace(",", "");
            res[parseInt(ii) - 1] = parseFloat(fstr[i + 1]);
        }
    }
    console.log(res);
    data = res;

    score=0;
    for(i=0;i<5;i++)
        score += i*res[i];
    document.getElementById('result-total').innerHTML = score.toFixed(7);
    
}