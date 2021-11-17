from app_base import app, server, youtubeAPI, rows, columns

if __name__ == "__main__":
    app.run_server(debug=True, port=8000)