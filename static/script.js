function restartVideo(){
    document.getElementById("debug").innerHTML = "Restart Video";
    var stream = document.getElementById("image");
    stream.src = "/video_feed";
}