import os
import freesound
import random
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
        client.set_token(FS_CLIENT_ID)
        log('Freesound configured successfully!')
    except Exception as e:
        log('Could not connect to Freesound... %s' % str(e))
    return client


def is_request_valid(request):
    is_token_valid = request.form['token'] == SLACK_VERIFICATION_TOKEN
    is_team_id_valid = request.form['team_id'] == SLACK_TEAM_ID
    return is_token_valid and is_team_id_valid


def query_freesound(query_terms):
    results_pager = freesound_client.text_search(
        query=query_terms,
        fields="id,name,previews,username,url",
        page_size=50,
    )
    sounds = list()
    for result in results_pager:
        sounds.append(result)
    if sounds:
        if query_terms.isdigit():
            # If query is a digit, return first results as we assume the digit is a Freesound ID
            return sounds[0]
        else:
            # Otherwise return a random sound from the results
            return random.choice(sounds)
    return None



# VIEWS

# From https://renzo.lucioni.xyz/serverless-slash-commands-with-python/

@app.route('/%s/' % APPLICATION_ROOT, methods=['POST'])
def command_handler():
    if not is_request_valid(request):
        abort(400)

    command = request.values['command']
    args = request.values['text']

    if command == '/freesound':
        try:
            sound = query_freesound(args)
            if sound:
                return jsonify(
                    response_type='in_channel',
                    mrkdwn=True,
                    text='[{0}]({1}) by [{2}]({3})'.format(sound.name, sound.url, sound.username, 'https://freesound.org/people/' + sound.username),
                )
            else:
                return jsonify(
                    response_type='ephemeral',
                    text='No sounds found for this query...'
                )

        except Exception as e:
            return jsonify(
                response_type='ephemeral',
                text='Oups, there was an error... ({0})'.format(e)
            )


# RUN FLASK

if __name__ == '__main__':
    freesound_client = configure_freesound()
    app.run(debug=DEBUG, host=HOST, port=PORT)
