# freesound-slack-command

Slack app with slash command for playing sounds from Freesound

## Dev & deploy instructions

### Build & run

The following environment variables **must** be set before running using a `.env` file:
 * `FS_API_KEY`: Freesound API key from https://freesound.org/apiv2/apply.
 * `SLACK_VERIFICATION_TOKEN`: Slack app verification token (see https://renzo.lucioni.xyz/serverless-slash-commands-with-python/).
 * `SLACK_TEAM_ID`: Slack team ID (see https://renzo.lucioni.xyz/serverless-slash-commands-with-python/).

The following environment variables are optional:
 * `HOST`, `PORT`: Host and port for the web app (defaults to  `0.0.0.0` and `5000`).
 * `BASE_URL`: Base URL to build app URLs (defaults to `http://localhost:5000/`)
 * `DEBUG`: Flask debug setting flag (defaults to `True`).
 * `APPLICATION_ROOT`: Path of the application to be added to the BASE_URL.


To run the app use:

```docker-compose up```
