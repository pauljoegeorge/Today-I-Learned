from flask import Flask, render_template, json
from flask_ask import Ask, statement, question, session
import json
import requests

app = Flask(__name__)
ask = Ask(app, '/')

def lambda_handler(event, _context):
    return ask.run_aws_lambda(event)

# will run on invocation
@ask.launch
def launched():
    response = render_template('launch')
    return question(response)

# when something goes wrong
@ask.default_intent
def default_message():
    response = render_template('default')
    return statement(response)

# user training Alexa to learn to new vocabulary
@ask.intent('NewVocabIntent')
def learn(word, meaning):
    print("word is .." + word)
    print("meaning.." + meaning)
    response = render_template('confirm_before_save', new_word = word, meaning = meaning)
    session.attributes['request'] = "save"
    return question(response)

# confirm and save new word to DynamoDB
@ask.intent('ConfirmYesIntent')
def save_new():
    if(session.attributes['request'] == "save"):
        response = render_template('confirmed')
        return statement(response)

# discard the word
@ask.intent('ConfirmNoIntent')
def discard_new():
    if(session.attributes['request'] == "save"):
        response = render_template('discard')
        return statement(response)

if __name__ == '__main__':
    app.run(debug=True)
