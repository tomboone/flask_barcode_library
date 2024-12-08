// noinspection JSUnresolvedReference,InfiniteLoopJS
// noinspection JSUnresolvedReference
(async function () {
  //WebAssembly polyfill for some browsers
  try { window['BarcodeDetector'].getSupportedFormats() }
  catch { window['BarcodeDetector'] = barcodeDetectorPolyfill.BarcodeDetectorPolyfill }

  const video = document.getElementById("video");
  const barcodeResult = document.getElementById("barcode");

  video.setAttribute("autoplay", "");
  video.setAttribute("muted", "");
  video.setAttribute("playsinline", "");

  // Initialize the Barcode Detector with supported formats
  const barcodeDetector = new BarcodeDetector({ formats: ["qr_code", "ean_13", "code_128"] });

  // Access the camera
  video.srcObject = await navigator.mediaDevices.getUserMedia({video: {facingMode: "environment"}}); // Assign stream to video element
  video.play();

  // Barcode detection loop
  video.addEventListener("play", async () => {
    while (true) {
      try {
        let barcodes = await barcodeDetector.detect(video); // Detect barcodes
        if (barcodes.length === 0) {
          await new Promise(r => setTimeout(r, 50));
          continue;
        }
        barcodeResult.value = barcodes[0].rawValue; // Show first detected barcode
        document.getElementById("submit").click(); // Submit the form
        break
      } catch {
        await new Promise(resolve => setTimeout(resolve, 100)); // Add delay for performance        }
      }
    }
  });
})();
