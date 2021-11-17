from app_base import app, server, youtubeAPI, rows, columns
import waitress
import logging

if __name__ == "__main__":
    logger = logging.getLogger('waitress')
    logger.setLevel(logging.INFO)
    waitress.serve(server, host='0.0.0.0', port=80)