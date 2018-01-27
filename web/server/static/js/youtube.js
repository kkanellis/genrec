
function loadYTVideo(videoId) {
    if (ytplayer != null) {
        ytplayer.stopVideo();
        ytplayer.destroy();
    }

    createPlayer(videoId); 
}

function createPlayer(videoId) {
    ytplayer = new YT.Player('ytplayer', {
      height: '480',
      width: '854',
      videoId: videoId,
      playerVars: { 
          'fs': 0,              // disable fullscreen
          'iv_load_policy': 3,  // disable annotations
      },
      events: {
        'onReady': onPlayerReady,
        'onStateChange': onPlayerStateChange
      }
    });
}

// 4. The API will call this function when the video ytplayer is ready.
function onPlayerReady(event) {
    event.target.playVideo();
}

// 5. The API calls this function when the player's state changes.
//    The function indicates that when playing a video (state=1),
//    the ytplayer should play for six seconds and then stop.
var done = false;
function onPlayerStateChange(event) {
    if (event.data == YT.PlayerState.PLAYING && !done) {
      /*setTimeout(stopVideo, 6000);
      done = true;*/
    }
}

