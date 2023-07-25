// meeting_room.js
const meetingId = "{{ meeting.id }}";
const participantToken = '{{ participant_token }}';
const localVideo = document.getElementById('localVideo');
const remoteVideoContainer = document.getElementById('remoteVideoContainer');

// Function to initialize the video call
async function initializeVideoCall() {
  // Get user media (video and audio)
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
    localVideo.srcObject = stream;

    // Create WebSocket connection
    const webSocketProtocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
    const webSocketPath = '/ws/meeting/' + meetingId + '/';
    const webSocketURL = webSocketProtocol + window.location.host + webSocketPath;
    const webSocket = new WebSocket(webSocketURL);

    // Event listener for WebSocket open
    webSocket.onopen = () => {
      console.log('WebSocket connection opened');
      // Send participant information to server
      webSocket.send(JSON.stringify({ type: 'join', token: participantToken }));
    };

    // Event listener for WebSocket message
    webSocket.onmessage = (event) => {
      const message = JSON.parse(event.data);
      handleSignalingMessage(message);
    };

    // Function to handle signaling messages (offer, answer, ice_candidate)
    function handleSignalingMessage(message) {
      switch (message.type) {
        case 'offer':
          // Handle offer and create answer
          // ...
          break;
        case 'answer':
          // Handle answer
          // ...
          break;
        case 'ice_candidate':
          // Handle ICE candidate
          // ...
          break;
        default:
          console.warn('Invalid signaling message type:', message.type);
      }
    }

    // Function to send signaling messages to the server
    function sendSignalingMessage(message) {
      webSocket.send(JSON.stringify(message));
    }
  } catch (error) {
    console.error('Error accessing media devices:', error);
  }
}

// Call the function to initialize the video call
initializeVideoCall();
