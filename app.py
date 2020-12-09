from datetime import datetime
import json

from flask import Flask, request
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_SYNC_SID

app = Flask(__name__)

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
sync = client.sync.services(TWILIO_SYNC_SID)

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

    # Create a sync list for the phone numebr if it doesn't already have one
    try:
        sync_list = sync.sync_lists.get(user_number).fetch()
    except TwilioRestException:
        sync_list = sync.sync_lists.create(unique_name = user_number)


    # Save the memo to the user's sync list
    data = {
        "title": memo_title,
        "tag": memo_tag,
        "call_sid": call.sid,
        "created_on": datetime.now().strftime("%b %d - %-I:%M %p")
    }

    document = sync_list.sync_list_items.create(data = data)

    # Return an empty action to end the autopilot conversation
    actions = {
        "actions": []
    }

    return actions


@app.route('/process_memo', methods = ['POST'])
def process_memo():
    # Get data from request
    data = request.form.to_dict()

    # Collect recording info from data
    twilio_number = data['From']
    user_number = data['To']
    recording_url = data['RecordingUrl']
    if data['TranscriptionStatus'] == "failed":
        transcription = "There was an error transcribing this memo."
    else:
        transcription = data['TranscriptionText']

    call_sid = data['CallSid']

    # Fetch user's sync list
    sync_list = sync.sync_lists.get(user_number).fetch()
    sync_list_items = sync_list.sync_list_items.list(limit = 5, order = "desc")
    sync_list_item = list(filter(lambda item: item.data.get('call_sid') == call_sid, sync_list_items))[0]

    # Add memo to document
    new_data = {
        **sync_list_item.data,
        'recording_url': recording_url,
        'transcription': transcription
    }

    sync_list_item.update(data = new_data)

    # Send user the memo
    memo_title = new_data['title']
    memo_tag = new_data['tag']
    created_on = new_data['created_on']

    client.messages.create(
        body = "%(title)s\nTag: %(tag)s\nCreated on: %(created_on)s\nRecording link: %(recording_url)s\n\n%(transcription)s" % {
            "title": memo_title,
            "tag": memo_tag,
            "created_on": created_on,
            "recording_url": recording_url,
            "transcription": transcription
        }, 
        from_ = twilio_number,
        to= user_number
    )

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