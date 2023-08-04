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
}

function start() {
  console.log('Requesting local stream');
  startButton.disabled = true;
  navigator.mediaDevices.getUserMedia({
      audio: true,
      video: true
    })
    .then(gotStream)
    .catch(e => alert(`getUserMedia() error: ${e.name}`));
}

function call() {
  callButton.disabled = true;
  upgradeButton.disabled = false;
  hangupButton.disabled = false;
  shareScreenButton.disabled = false;

  console.log('Starting call');
  startTime = window.performance.now();

  const audioTracks = localStream.getAudioTracks();
  if (audioTracks.length > 0) {
    console.log(`Using audio device: ${audioTracks[0].label}`);
  }

  const servers = null;
  pc1 = new RTCPeerConnection(servers);
  console.log('Created local peer connection object pc1');
  pc1.onicecandidate = e => onIceCandidate(pc1, e);

  pc2 = new RTCPeerConnection(servers);
  console.log('Created remote peer connection object pc2');
  pc2.onicecandidate = e => onIceCandidate(pc2, e);
  pc2.ontrack = gotRemoteStream;

  localStream.getTracks().forEach(track => pc1.addTrack(track, localStream));
  console.log('Added local stream to pc1');

  console.log('pc1 createOffer start');
  pc1.createOffer(offerOptions)
    .then(onCreateOfferSuccess, onCreateSessionDescriptionError);
}

function onCreateSessionDescriptionError(error) {
  console.log(`Failed to create session description: ${error.toString()}`);
}

function onCreateOfferSuccess(desc) {
  console.log(`Offer from pc1:\n${desc.sdp}`);
  console.log('pc1 setLocalDescription start');
  pc1.setLocalDescription(desc)
    .then(() => onSetLocalSuccess(pc1), onSetSessionDescriptionError);
  console.log('pc2 setRemoteDescription start');
  pc2.setRemoteDescription(desc)
    .then(() => onSetRemoteSuccess(pc2), onSetSessionDescriptionError);
  console.log('pc2 createAnswer start');
  pc2.createAnswer()
    .then(onCreateAnswerSuccess, onCreateSessionDescriptionError);
}

function onSetLocalSuccess(pc) {
  console.log(`${getName(pc)} setLocalDescription complete`);
}

function onSetRemoteSuccess(pc) {
  console.log(`${getName(pc)} setRemoteDescription complete`);
}

function onSetSessionDescriptionError(error) {
  console.log(`Failed to set session description: ${error.toString()}`);
}

function gotRemoteStream(e) {
  console.log('gotRemoteStream', e.track, e.streams[0]);

  // Display the remote video in the participant's view (remoteVideo)
  if (e.streams[0].getVideoTracks().length > 0) {
    remoteVideo.srcObject = e.streams[0];
  }
}

function onCreateAnswerSuccess(desc) {
  console.log(`Answer from pc2:\n${desc.sdp}`);
  console.log('pc2 setLocalDescription start');
  pc2.setLocalDescription(desc)
    .then(() => onSetLocalSuccess(pc2), onSetSessionDescriptionError);
  console.log('pc1 setRemoteDescription start');
  pc1.setRemoteDescription(desc)
    .then(() => onSetRemoteSuccess(pc1), onSetSessionDescriptionError);
}

function onIceCandidate(pc, event) {
  getOtherPc(pc)
    .addIceCandidate(event.candidate)
    .then(() => onAddIceCandidateSuccess(pc), err => onAddIceCandidateError(pc, err));
  console.log(`${getName(pc)} ICE candidate:\n${event.candidate ? event.candidate.candidate : '(null)'}`);
}

function onAddIceCandidateSuccess(pc) {
  console.log(`${getName(pc)} addIceCandidate success`);
}

function onAddIceCandidateError(pc, error) {
  console.log(`${getName(pc)} failed to add ICE Candidate: ${error.toString()}`);
}

function onIceStateChange(pc, event) {
  if (pc) {
    console.log(`${getName(pc)} ICE state: ${pc.iceConnectionState}`);
    console.log('ICE state change event: ', event);
  }
}

function upgrade() {
  upgradeButton.disabled = true;
  navigator.mediaDevices.getUserMedia({
      video: true
    })
    .then(stream => {
      const videoTracks = stream.getVideoTracks();
      if (videoTracks.length > 0) {
        console.log(`Using video device: ${videoTracks[0].label}`);
      }
      localStream.addTrack(videoTracks[0]);
      localVideo.srcObject = null;
      localVideo.srcObject = localStream;
      pc1.addTrack(videoTracks[0], localStream);
      return pc1.createOffer();
    })
    .then(offer => pc1.setLocalDescription(offer))
    .then(() => pc2.setRemoteDescription(pc1.localDescription))
    .then(() => pc2.createAnswer())
    .then(answer => pc2.setLocalDescription(answer))
    .then(() => pc1.setRemoteDescription(pc2.localDescription));
}

function shareScreen() {
  navigator.mediaDevices.getDisplayMedia({ video: true })
    .then(stream => {
      const videoTracks = stream.getVideoTracks();
      if (videoTracks.length > 0) {
        console.log(`Using video device: ${videoTracks[0].label}`);
      }
      if (pc1 && pc1.signalingState !== 'closed') {
        // Remove the previous track
        const sender = pc1.getSenders().find(s => s.track && s.track.kind === 'video');
        if (sender) {
          pc1.removeTrack(sender);
        }
        pc1.addTrack(videoTracks[0], localStream);
      }
      if (pc2 && pc2.signalingState !== 'closed') {
        // Remove the previous track
        const sender = pc2.getSenders().find(s => s.track && s.track.kind === 'video');
        if (sender) {
          pc2.removeTrack(sender);
        }
        pc2.addTrack(videoTracks[0], remoteVideo.srcObject);
      }
      localVideo.srcObject = stream;
    })
    .catch(e => console.error('Error accessing screen: ', e));
}

function hangup() {
  console.log('Ending call');
  pc1.close();
  pc2.close();
  pc1 = null;
  pc2 = null;

  const videoTracks = localStream.getVideoTracks();
  videoTracks.forEach(videoTrack => {
    videoTrack.stop();
    localStream.removeTrack(videoTrack);
  });
  localVideo.srcObject = null;
  localVideo.srcObject = localStream;

  hangupButton.disabled = true;
  callButton.disabled = false;
  upgradeButton.disabled = true;
  shareScreenButton.disabled = true;
}

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
