import os
import freesound
from flask import Flask, request, jsonify, abort


HOST = os.getenv('HOST', '0.0.0.0')
PORT = os.getenv('PORT', 5000)
DEBUG = os.getenv('DEBUG', '1') == '1'  # Set it to '1' for DEBUG mode True, otherwise will be False
APPLICATION_ROOT = os.getenv('APPLICATION_ROOT', '')
BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000/')
SLACK_VERIFICATION_TOKEN = os.getenv('SLACK_VERIFICATION_TOKEN', '')
SLACK_TEAM_ID = os.getenv('SLACK_TEAM_ID', '')

try:
    FS_CLIENT_ID = os.environ['FS_CLIENT_ID']
except KeyError:
    raise Exception("Environment variables FS_CLIENT_ID not properly set.")

app = Flask(__name__)


freesound_client = None

# UTILS

def log(message):
    print(message)

def configure_freesound():
    # Get user access token and configure client
    client = None
    try:
        client = freesound.FreesoundClient()
        client.set_token(access_token, auth_type='token')
        log('Freesound configured successfully!')
    except Exception as e:
        log('Could not connect to Freesound... %s' % str(e))
    return client


def is_request_valid(request):
    is_token_valid = request.form['token'] == SLACK_VERIFICATION_TOKEN
    is_team_id_valid = request.form['team_id'] == SLACK_TEAM_ID
    return is_token_valid and is_team_id_valid


# VIEWS

# From https://renzo.lucioni.xyz/serverless-slash-commands-with-python/

@app.route('/' + APPLICATION_ROOT + '/freesound/', methods=['POST'])
def freesound_command():
    if not is_request_valid(request):
        abort(400)

    return jsonify(
        response_type='in_channel',
        text='<https://youtu.be/frszEJb0aOo|General Kenobi!>',
    )



# RUN FLASK

if __name__ == '__main__':
    freesound_client = configure_freesound()
    app.run(debug=DEBUG, host=HOST, port=PORT)
