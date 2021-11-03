def main():
    # this block checks if the current user has any artists saved
    check_artist = Artist.query.filter_by(user_id=current_user.id).first()
    # if no, the page will tell them they don't have any artist saved and will suggest for them to save one.
    if check_artist == None:
        has_artist = "no"

        return render_template(
            "index.html",
            current_user=current_user.username,
            has_artist=has_artist,
        )
    # if yes, one of the artists are chosen randomly and their artist id is used in the Spotify API, and the returned data will be displayed to the user
    else:
        has_artist = "yes"

        artists = Artist.query.filter_by(user_id=current_user.id).all()
        i = randrange(len(artists))
        artist_id = artists[i].artist_id
        song_data = get_artist_track(artist_id)

    if song_data != "error" or song_data != "id_error":
        # the returned song name from the top tracks API is inputted into the Genius search API to obtain the lyrics
        song_get_lyrics = song_data["song_name"]
        lyrics_data = get_lyrics(song_get_lyrics)

        # app's webpage is returned with all of the variables that will be shown on the page
        return render_template(
            "index.html",
            current_user=current_user.username,
            has_artist=has_artist,
            song_name=song_data["song_name"],
            artist=song_data["artist"],
            song_image=song_data["song_image"],
            preview_url=song_data["preview_url"],
            lyrics_url=lyrics_data["lyrics_url"],
        )
    else:
        # if there was any type of error when making requests to access a token or use the top tracks API from Spotify, then the app is directed to an error page.
        return render_template("error.html")
