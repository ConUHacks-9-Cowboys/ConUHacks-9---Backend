async function startWebcam() {
  try {
    const devices = await navigator.mediaDevices.enumerateDevices();
    const videoDevices = devices.filter(
      (device) => device.kind === "videoinput"
    );

    if (videoDevices.length >= 3) {
      const thirdCamera = videoDevices[4];
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { deviceId: { exact: thirdCamera.deviceId } },
      });
      document.getElementById("webcam").srcObject = stream;
    } else {
      console.error("Third camera not found.");
    }
  } catch (error) {
    console.error("Error accessing webcam:", error);
  }
}
startWebcam();
