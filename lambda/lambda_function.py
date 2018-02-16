#-------------------------------------------------------------------------------
# LightStrip
# Lambda handler code for LightStrip custom skill
#-------------------------------------------------------------------------------

import ala_controller

# -- Main handler --------------------------------------------------------------

def lambda_handler(event, context):
    """
    Route the incoming request based on type (LaunchRequest, IntentRequest, etc.)
    The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']}, event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])

# -- Events --------------------------------------------------------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """
    Called when the user launches the skill without specifying what they want
    """

    print("on_launch requestId=" + launch_request['requestId'] + ", sessionId=" + session['sessionId'])

    return intent_start()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] + ", sessionId=" + session['sessionId'])
    #print(session)

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "AMAZON.HelpIntent":
        return intent_help()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return intent_end()
    elif intent_name == "TurnOn":
        return intent_turn_on(intent, session)
    elif intent_name == "TurnOff":
        return intent_turn_off(intent, session)
    elif intent_name == "SetBrightness":
        return intent_set_brightness(intent, session)
    elif intent_name == "SetColor":
        return intent_set_color(intent, session)
    elif intent_name == "RunAnimation":
        return intent_run_animation(intent, session)
    elif intent_name == "NextAnimation":
        return intent_next_animation(intent, session)
    elif intent_name == "StopAnimation":
        return intent_stop_animation(intent, session)
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# -- Intent handlers -----------------------------------------------------------


def intent_start():
    
    ala_controller.thingshadow_start()

    session_attributes = {'status':'start'}
    speech_text = "Welcome to LightStrip."
    reprompt_text = "You can control your lighting or you can run some light animations." \
                    "Please say something like turn on white light or run a relaxing animation."
    card_title = "Welcome"
    card_text = None
    end_session = False

    speechlet_response = build_speechlet_response(speech_text, reprompt_text, card_title, card_text, end_session)
    return build_response(session_attributes, speechlet_response)

def intent_help():
    session_attributes = {}
    if 'attributes' in session:
        session_attributes = session['attributes']

        speech_text = "With LightStrip you can control your lights or you can run some animations. " \
                  "To switch on a white light you can just say 'turn on'. " \
                  "To try out an animation say 'run an animation'."
    reprompt_text = None
    card_title = "Help"
    card_text = None
    end_session = False
    
    speechlet_response = build_speechlet_response(speech_text, reprompt_text, card_title, card_text, end_session)
    return build_response(session_attributes, speechlet_response)


def intent_end():
    # say bye and close session

    ala_controller.thingshadow_turn_off()
    
    session_attributes = {}
    speech_text = "Thank you for using LightStrip. Bye!"
    reprompt_text = None
    card_title = "The End"
    card_text = None
    end_session = True

    speechlet_response = build_speechlet_response(speech_text, reprompt_text, card_title, card_text, end_session)
    return build_response(session_attributes, speechlet_response)


def intent_turn_on(intent, session):

    ala_controller.thingshadow_turn_on()
    
    session_attributes = {'status':'on'}
    speech_text = "Turned on"
    reprompt_text = None
    card_title = "Turn on"
    card_text = "Your LightStrip is now turned on. " \
                "You can change color of the light or tryout some animations."
    end_session = False
    
    speechlet_response = build_speechlet_response(speech_text, reprompt_text, card_title, card_text, end_session)
    return build_response(session_attributes, speechlet_response)

def intent_turn_off(intent, session):

    ala_controller.thingshadow_turn_off()
    
    session_attributes = {'status':'off'}
    speech_text = "Turned off"
    reprompt_text = None
    card_title = "Turn of"
    card_text = None
    end_session = False
    
    speechlet_response = build_speechlet_response(speech_text, reprompt_text, card_title, card_text, end_session)
    return build_response(session_attributes, speechlet_response)



def intent_set_brightness(intent, session):
    session_attributes = {}
    if 'attributes' in session:
        session_attributes = session['attributes']
    
    if 'brightness' not in intent['slots']:
        return build_response(session_attributes, build_speechlet_response_with_directive_nointent())
        
    #speech_text = ""
    reprompt_text = None
    card_title = "Set brightness"
    card_text = None
    end_session = False
    

    if 'value' in intent['slots']['brightness']:
        brightness = int(intent['slots']['brightness']['value'])
        if brightness > 0 and brightness <=100:
            ala_controller.thingshadow_set_brightness(brightness)
            speech_text = "Brightness set to " + str(brightness)
        else:
            speech_text = "Sorry, brightness must be a percentage between 1 and 100."
    else:
        speech_text = "Sorry, i don't understand."
    
    speechlet_response = build_speechlet_response(speech_text, reprompt_text, card_title, card_text, end_session)
    return build_response(session_attributes, speechlet_response)


def intent_set_color(intent, session):
    session_attributes = {}
    if 'attributes' in session:
        session_attributes = session['attributes']

    if 'color' not in intent['slots']:
        return build_response(session_attributes, build_speechlet_response_with_directive_nointent())
    
    '''
    if session['attributes']['status'] != 'on':
        speech_text = "Invalid command"
        reprompt_text = None
        card_title = None
        card_text = None
        end_session = False
        speechlet_response = build_speechlet_response(speech_text, reprompt_text, card_title, card_text, end_session)
        return build_response(session_attributes, speechlet_response)
    '''
    
    #speech_text = ""
    reprompt_text = None
    card_title = "Set color"
    card_text = None
    end_session = False

    #print(intent['slots'])
    if 'value' in intent['slots']['color']:
        color = intent['slots']['color']['value']
        rgb_color = get_color(color)
        if rgb_color == "":
            speech_text = "I can't understand what color do you want."
        else:
            ala_controller.thingshadow_set_color(rgb_color)
            speech_text = "OK"
            card_text = "Color set to " + color + " (" + get_color(color) + ")"

    speechlet_response = build_speechlet_response(speech_text, reprompt_text, card_title, card_text, end_session)
    return build_response(session_attributes, speechlet_response)


def intent_run_animation(intent, session):
    session_attributes = {}
    if 'attributes' in session:
        session_attributes = session['attributes']

    if 'value' not in intent['slots']['animType']:
        return build_response(session_attributes, build_speechlet_response_with_directive_nointent())
        
    #speech_text = ""
    reprompt_text = None
    card_title = "Run animation"
    card_text = None
    end_session = False
    

    animType = intent['slots']['animType']['value']
   
    speech_text = "Animation type " + animType
    card_text = "LightStrip is now running a random " + animType + " animation. " \
                "To try another animation say 'next animation'."
    if animType == 'relaxing':
        session_attributes = {'status':'animation', 'animType':animType}
        ala_controller.animation_relaxing()
    elif animType == 'exciting':
        session_attributes = {'status':'animation', 'animType':animType}
        ala_controller.animation_exciting()
    else:
        speech_text = "Do you want a relaxing or exciting animation?"
        card_text = None

    speechlet_response = build_speechlet_response(speech_text, reprompt_text, card_title, card_text, end_session)
    return build_response(session_attributes, speechlet_response)


def intent_next_animation(intent, session):
    session_attributes = {}
    if 'attributes' in session:
        session_attributes = session['attributes']
    
    if session['attributes']['status'] != 'animation':
        speech_text = "Invalid command"
        reprompt_text = None
        card_title = None
        card_text = None
        end_session = False
        speechlet_response = build_speechlet_response(speech_text, reprompt_text, card_title, card_text, end_session)
        return build_response(session_attributes, speechlet_response)
    
    animType = session['attributes']['animType']
    if animType == 'relaxing':
        ala_controller.animation_relaxing()
    elif animType == 'exciting':
        ala_controller.animation_exciting()

    
    speech_text = "OK"
    reprompt_text = None
    card_title = "Next animation"
    card_text = "Showing another animation."
    end_session = False
    
    speechlet_response = build_speechlet_response(speech_text, reprompt_text, card_title, card_text, end_session)
    return build_response(session_attributes, speechlet_response)


def intent_stop_animation(intent, session):
    session_attributes = {}
    if 'attributes' in session:
        session_attributes = session['attributes']
    
    if session['attributes']['status'] != 'animation':
        speech_text = "Invalid command"
        reprompt_text = None
        card_title = None
        card_text = None
        end_session = False
        speechlet_response = build_speechlet_response(speech_text, reprompt_text, card_title, card_text, end_session)
        return build_response(session_attributes, speechlet_response)

    ala_controller.thingshadow_start()

    session_attributes = {'status':'start'}
    speech_text = "OK"
    reprompt_text = None
    card_title = "Stop animation"
    card_text = "Animation stopped. Say 'turn off' to exit."
    end_session = False
    
    speechlet_response = build_speechlet_response(speech_text, reprompt_text, card_title, card_text, end_session)
    return build_response(session_attributes, speechlet_response)



# -- Helper functions ----------------------------------------------------------

def build_speechlet_response(speech_text, reprompt_text, card_title, card_text, should_end_session):
    if card_text == None:
        card_text = speech_text
    
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': speech_text
        },
        'card': {
            'type': 'Simple',
            'title': card_title,
            'content': card_text
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

def build_speechlet_response_with_directive_nointent():
    return {
      'outputSpeech' : None,
      'card' : None,
      'directives' : [ {
        'type' : 'Dialog.Delegate'
      } ],
      'reprompt' : None,
      'shouldEndSession' : False
    }



def get_color(color_name):
    colors = {
        'white': 'FFFFFF',
        'warm white': 'FFCC88',
        'cool white': '88CCFF',
        'gray': '888888',
        'blue': '0000FF',
        'crimson': 'DC143C',
        'cyan': '00FFFF',
        'fuchsia': 'FF00FF',
        'gold': 'FFD700',
        'green': '00FF00',
        'lavender': 'E6E6FA',
        'lime': '32CD32',
        'magenta': 'FF00FF',
        'orange': 'FFA500',
        'pink': 'FFC0CB',
        'purple': '800080',
        'red': 'FF0000',
        'teal': '008080',
        'turquoise': '40E0D0',
        'violet': 'EE82EE',
        'yellow': 'FFFF00'
        }
     
    return colors.get(color_name, "")
