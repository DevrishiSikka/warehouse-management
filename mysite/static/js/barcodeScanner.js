document.addEventListener("DOMContentLoaded", function() {
const video = document.getElementById('scanner-video');
const barcodeInput = document.getElementById('barcode');
const startScanButton = document.getElementById('start-scan');
let stream;

startScanButton.addEventListener('click', () => {
    if ('BarcodeDetector' in window) {
            const barcodeDetector = new BarcodeDetector({ formats: ['ean_13', 'code_128'] });
            navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
                .then(s => {
                    stream = s;
                    video.srcObject = stream;
                    video.style.display = 'block'; 

                    const scanBarcode = () => {
                        barcodeDetector.detect(video)
                            .then(barcodes => {
                                if (barcodes.length > 0) {
                                    barcodeInput.value = barcodes[0].rawValue;

                                    if (navigator.vibrate) {
                                        navigator.vibrate(100);
                                    }

                                    stopVideoStream();
                                }
                            })
                            .catch(err => console.error(err));

                        requestAnimationFrame(scanBarcode);
                    };

                    scanBarcode();
                })
                .catch(err => console.error("Error accessing camera: ", err));
        } else {
            alert("Barcode detection is not supported on this browser.");
        }
    });

function stopVideoStream() {
        if (stream) {
            const tracks = stream.getTracks();
            tracks.forEach(track => track.stop());
        }
        video.style.display = 'none';
    }
});
