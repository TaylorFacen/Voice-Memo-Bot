from flask import Flask, request

app = Flask(__name__)

@app.route('/start_memo', methods = ['POST'])
def start_memo():
    # Get data from request

    # Collect memo data from autopilot memory

    # Call user

    # Create a sync list for the phone numebr if it doesn't already have one

    # Save the memo to the user's sync list

    # Return an empty action to end the autopilot conversation
    return {}, 200


@app.route('/process_memo', methods = ['POST'])
def process_memo():
    # Get data from request

    # Collect recording info from data

    # Fetch user's sync list

    # Add memo to document

    # Send user the memo

    return {}, 200 

@app.route('/list_memos', methods = ['POST'])
def list_memos():
    # Get data from request

    # Collect user phone number and limit from memory

    # Fetch memos from user's sync list

    # Return list of memos (metadata only)
    return {}, 200

@app.route('/fetch_memo', methods = ['POST'])
def fetch_memo():
    # Get data from request

    # Collect user phone number and memo id from memory

    # Fetch memo from user's sync list

    # Return memo
    return {}, 200

if __name__ == "__main__":
    app.run(debug = True)