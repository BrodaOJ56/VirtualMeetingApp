const startButton = document.getElementById('startButton');
const callButton = document.getElementById('callButton');
const upgradeButton = document.getElementById('upgradeButton');
const hangupButton = document.getElementById('hangupButton');
const shareScreenButton = document.getElementById('shareScreenButton');

callButton.disabled = true;
hangupButton.disabled = true;
upgradeButton.disabled = true;
shareScreenButton.disabled = true;

startButton.onclick = start;
callButton.onclick = call;
upgradeButton.onclick = upgrade;
hangupButton.onclick = hangup;
shareScreenButton.onclick = shareScreen;

let startTime;
const localVideo = document.getElementById('localVideo');
const remoteVideo = document.getElementById('remoteVideo');

localVideo.addEventListener('loadedmetadata', function () {
  console.log(`Local video videoWidth: ${this.videoWidth}px,  videoHeight: ${this.videoHeight}px`);
});

remoteVideo.addEventListener('loadedmetadata', function () {
  console.log(`Remote video videoWidth: ${this.videoWidth}px,  videoHeight: ${this.videoHeight}px`);
});

remoteVideo.onresize = () => {
  console.log(`Remote video size changed to ${remoteVideo.videoWidth}x${remoteVideo.videoHeight}`);
  console.warn('RESIZE', remoteVideo.videoWidth, remoteVideo.videoHeight);
  if (startTime) {
    const elapsedTime = window.performance.now() - startTime;
    console.log(`Setup time: ${elapsedTime.toFixed(3)}ms`);
    startTime = null;
  }
};

let localStream;
let pc1;
let pc2;
const offerOptions = {
  offerToReceiveAudio: 1,
  offerToReceiveVideo: 1
};

function getName(pc) {
  return (pc === pc1) ? 'pc1' : 'pc2';
}

function getOtherPc(pc) {
  return (pc === pc1) ? pc2 : pc1;
}

function gotStream(stream) {
  console.log('Received local stream');
  localVideo.srcObject = stream;
  localStream = stream;
  callButton.disabled = false;
  shareScreenButton.disabled = false;
}

// ... (The rest of the code remains unchanged)

// Function to handle the screen sharing stream's addTrack event
function onAddTrack(event) {
  console.log('onAddTrack', event.track, event.streams[0]);
  remoteVideo.srcObject = event.streams[0];
}

// Attach the onAddTrack event handler to both peer connections
if (pc1) {
  pc1.ontrack = onAddTrack;
}
if (pc2) {
  pc2.ontrack = onAddTrack;
}
