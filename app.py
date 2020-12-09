import json

from flask import Flask, request
from twilio.rest import Client

from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_SYNC_SID

app = Flask(__name__)

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.route('/start_memo', methods = ['POST'])
def start_memo():
    # Get data from request
    data = request.form.to_dict()
    api_url = request.host_url

    # Collect memo data from autopilot memory
    memory = json.loads(data['Memory'])
    twilio_number = memory['twilio']['sms']['To']
    user_number = memory['twilio']['sms']['From']
    responses = memory['twilio']['collected_data']['get_memo_data']['answers']
    memo_title = responses['memo_title']['answer']
    memo_tag = responses['memo_tag']['answer']

    # Call user
    twiml = '''
    <Response>
        <Say>When you're done recording, press the pound key.</Say>
        <Record timeout="10" transcribe="true" transcribeCallback="{}process_memo"/>
        <Say>You'll receive a text when your memo is processed. Goodbye</Say>
    </Response>
    '''.format(api_url)

    call = client.calls.create(
        twiml = twiml,
        to = user_number,
        from_ = twilio_number
    )

    print(call.sid)

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