from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Reddit API credentials
CLIENT_ID = 'hnlix-XawsyMhKcSLKLScA'
CLIENT_SECRET = 'iZDHSlFysY5AOFUkZdlvdtgTtdsBrg'
REFRESH_TOKEN = '97946466270250-SSQZBQh0EKT_wULYQ0YjfwrNCakDyA'
USER_AGENT = 'rithvikhacker'


def get_access_token():
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': REFRESH_TOKEN
    }
    headers = {'User-Agent': USER_AGENT}

    response = requests.post('https://www.reddit.com/api/v1/access_token',
                             auth=auth, data=data, headers=headers)
    response.raise_for_status()
    return response.json().get('access_token')


def post_to_reddit(subreddit, title, text):
    access_token = get_access_token()
    headers = {
        'Authorization': f'bearer {access_token}',
        'User-Agent': USER_AGENT
    }
    data = {
        'sr': subreddit,
        'title': title,
        'kind': 'self',
        'text': text
    }
    response = requests.post('https://oauth.reddit.com/api/submit',
                             headers=headers, data=data)
    return response.json()


@app.route('/post', methods=['POST'])
def post():
    # Get data from the request body
    data = request.json

    # Extract parameters
    subreddit = data.get('subreddit')
    title = data.get('title')
    text = data.get('text')

    if not subreddit or not title or not text:
        return jsonify({'error': 'Missing required parameters'}), 400

    # Post to Reddit
    result = post_to_reddit(subreddit, title, text)

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
