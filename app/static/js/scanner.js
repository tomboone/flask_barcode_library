// noinspection JSUnresolvedReference,InfiniteLoopJS

(async function () {
  const video = document.getElementById("video");
  const barcodeResult = document.getElementById("barcode");

  vidoe.setAttribute("autoplay", "");
  video.setAttribute("muted", "");
  video.setAttribute("playsinline", "");

  // Check for BarcodeDetector support
  if (!("BarcodeDetector" in window)) {
    alert("Barcode Detection API is not supported in this browser.");
    return;
  }

  // Initialize the Barcode Detector with supported formats
  const barcodeDetector = new BarcodeDetector({ formats: ["qr_code", "ean_13", "code_128"] });

  try {
    // Access the camera
    video.srcObject = await navigator.mediaDevices.getUserMedia({video: {facingMode: "environment"}}); // Assign stream to video element
    video.play();

    // Barcode detection loop
    video.addEventListener("play", async () => {
      while (true) {
        try {
          const barcodes = await barcodeDetector.detect(video); // Detect barcodes
          if (barcodes.length > 0) {
            barcodeResult.value = barcodes[0].rawValue; // Show first detected barcode
            document.getElementById("submit").click(); // Submit the form
            break
          }
        } catch (err) {
          console.error("Error detecting barcode:", err);
        }
        await new Promise(resolve => setTimeout(resolve, 100)); // Add delay for performance
      }
    });
  } catch (error) {
    console.error("Error accessing camera:", error);
    alert("Unable to access the camera. Please check permissions or run the code on a secure server.");
  }
})();
