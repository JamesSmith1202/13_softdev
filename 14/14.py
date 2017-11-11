from flask import Flask, render_template, request
import urllib2
import json

api_base = "http://api.musixmatch.com/ws/1.1/{0}?{1}&apikey=7169e60f579305a0c080332a16b41537"#formatting strings for the command and parameters


app = Flask(__name__)

def get_song_id(track, artist):
    url = api_base.format("track.search", "q_track={0}&q_artist={1}&page_size=5&page=1&s_track_rating=desc".format(track.replace(" ", "%20"), artist.replace(" ", "%20")))
    u = urllib2.urlopen(url)
    msg = u.read()
    search_dict = json.loads(msg)
    if search_dict["message"]["body"]["track_list"] == []:
        return 0
    return search_dict["message"]["body"]["track_list"][0]["track"]["track_id"]

def get_lyrics(track_id):
    url = api_base.format("track.lyrics.get","track_id={}".format(track_id))
    u = urllib2.urlopen(url)
    msg = u.read()
    lyrics_dict = json.loads(msg)
    return lyrics_dict["message"]["body"]["lyrics"]["lyrics_body"]

def get_img(track_id):
    url = api_base.format("track.get","track_id={}".format(track_id))
    u = urllib2.urlopen(url)
    msg = u.read()
    track_dict = json.loads(msg)
    print track_dict
    return track_dict["message"]["body"]["track"]["album_coverart_500x500"]

@app.route("/", methods=["GET", "POST"])
def root():
    if request.method == "GET":
        return render_template('search.html')
    if request.method == "POST":
        song_id = get_song_id(request.form["track_name"], request.form["artist"])
        if(song_id == 0):
            return render_template('error.html')
        return render_template('main.html', song_title=request.form["track_name"].title(), artist=request.form["artist"].title(), img=get_img(song_id), lyrics=get_lyrics(song_id))

if __name__ == "__main__":
    app.run()