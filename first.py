from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import json

app = Flask(__name__)


client = MongoClient('mongodb://localhost:27017/')
db = client.github_events
collection = db.events

@app.route('/webhook', methods=['POST'])
def webhook():
    
    data = json.loads(request.data)
    event_type = request.headers.get('X-GitHub-Event')

    if event_type in ["push", "pull_request", "pull_request_review", "pull_request_review_comment", "issues", "issue_comment", "commit_comment", "create", "delete", "label", "milestone"]:
        
        if event_type == "push":
            author = data['pusher']['name']
            branch = data['ref'].split('/')[-1]
            action = "pushed to"
        elif event_type == "pull_request":
            author = data['pull_request']['user']['login']
            from_branch = data['pull_request']['head']['ref']
            to_branch = data['pull_request']['base']['ref']
            action = "submitted a pull request from"
        
        
        timestamp = datetime.utcnow().strftime('%d %b %Y - %I:%M %p UTC')

        
        event = {
            'author': author,
            'action': action,
            'from_branch': from_branch if event_type == "pull_request" else None,
            'to_branch': to_branch if event_type == "pull_request" else branch,
            'timestamp': timestamp
        }
        collection.insert_one(event)

    return jsonify({'message': 'Webhook received'}), 200

@app.route('/events')
def get_events():
    
    events = list(collection.find().sort('_id', -1).limit(10))
    formatted_events = []

    
    for event in events:
        if event['action'] == 'pushed to':
            formatted_event = f"{event['author']} {event['action']} {event['to_branch']} on {event['timestamp']}"
        elif event['action'] == 'submitted a pull request from':
            formatted_event = f"{event['author']} {event['action']} {event['from_branch']} to {event['to_branch']} on {event['timestamp']}"
        

        formatted_events.append(formatted_event)

    return jsonify(formatted_events)

if __name__ == '__main__':
    app.run(debug=True)
