
"""

AWS lambda code by end of part 2 of programming alexa series

"""



from __future__ import print_function
import requests
import json
import os

# --------------- Helpers that build all of the responses ----------------------

def build_speech_response(title, output, reprompt_text, should_end_session):

    return {

        'outputSpeech': {

            'type': 'PlainText',

            'text': output

        },

        'card': {

            'type': 'Simple',

            'title': "SessionSpeech - " + title,

            'content': "SessionSpeech - " + output

        },

        'reprompt': {

            'outputSpeech': {

                'type': 'PlainText',

                'text': reprompt_text

            }

        },

        'shouldEndSession': should_end_session

    }



def build_response(session_attributes, speech_response):

    return {

        'version': '1.0',

        'sessionAttributes': session_attributes,

        'response': speech_response

    }





# --------------- Functions that control the skill's behavior ------------------

def get_OneProductIntent_response(intent):

    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent

    in your alexa skill in order for it to work.

    """
    session_attributes = {}
    params={
        "api_token":"insert_your_pipedrive_api_key",
        "term":intent['slots']['name']['value']  
    }
    r = requests.get("https://api.pipedrive.com/v1/products/find", params=params)
    response=json.loads(r.content)

    param={
        "api_token":"insert_your_pipedrive_api_key"
    }
    if response["data"] is None:
        speech_output = "There is no Product named as " + intent['slots']['name']['value']  
        card_title = "OneProductIntent"
        reprompt_text = "Try again by giving a product name in your CRM"  
        should_end_session = True
        return build_response(session_attributes, build_speech_response(card_title, speech_output, reprompt_text, should_end_session))

    id=response["data"][0]["id"]
    req = requests.get("https://api.pipedrive.com/v1/products/" + str(id), params=param)
    res=json.loads(req.content)
    
    card_title = "OneProductIntent"

    price=res["data"]["prices"][0]["price"]

    speech_output = "Okay " + res["data"]["name"] + " product has a price of INR " + str(price)  + " and having " + res["data"]["unit"] + "unit"

    reprompt_text = "Try again by giving a product name"  

    should_end_session = True

    return build_response(session_attributes, build_speech_response(

        card_title, speech_output, reprompt_text, should_end_session))

def get_DealProductIntent_response(intent):


    session_attributes = {}
    params={
        "api_token":"insert_your_pipedrive_api_key",
        "term":intent['slots']['name']['value']
    }

    r = requests.get("https://api.pipedrive.com/v1/products/find", params=params)
    response=json.loads(r.content)
    param={
        "api_token":"insert_your_pipedrive_api_key"
    }
    if response["data"] is None:
        card_title = "DealProductIntent"
        speech_output="There is no Product with name " + intent['slots']['name']['value']
        reprompt_text = "Try a Product name in your CRM"
        should_end_session = True
        return build_response(session_attributes, build_speech_response(card_title, speech_output, reprompt_text, should_end_session))
    id=response["data"][0]["id"]
    req = requests.get("https://api.pipedrive.com/v1/products/"+str(id)+ "/deals", params=params)
    res=json.loads(req.content)
    
    card_title = "DealProductIntent"
    if res["data"] is None:
        speech_output = "There is no Deal with " + intent['slots']['name']['value']
    elif res["data"][0]["title"] is None or res["data"][0]["org_name"] is None or res["data"][0]["value"] is None:
        speech_output = "Some details are missing in the Deal. Please check your CRM"
    else :
        speech_output = "The product " + response["data"][0]["name"] + " is involved in " + res["data"][0]["title"] + " with organisation " + res["data"][0]["org_name"] + " having a worth of " + str(res["data"][0]["value"]) + " INR"

    reprompt_text = "Try a Product name in your CRM"

    should_end_session = True

    return build_response(session_attributes, build_speech_response(

        card_title, speech_output, reprompt_text, should_end_session))


def get_AddProductIntent_response(intent):


    session_attributes = {}


    params={
        "api_token":"insert_your_pipedrive_api_key"
    }
    data={
        "name":intent['slots']['name']['value'],
        "unit":intent['slots']['unit']['value'],
        "prices":[{"price":intent['slots']['price']['value'], "currency": "INR"}]
    }
    headers={"Content-Type" : "application/json"}

    r = requests.post("https://api.pipedrive.com/v1/products/products", params=params, data=json.dumps(data), headers=headers)
    response=json.loads(r.content)
    card_title = "AddProductIntent"
    speech_output = "Product with name " + intent['slots']['name']['value'] + "created succesfully. You can check your CRM"

    reprompt_text = "Try again by telling me price, unit and name of the Product"

    should_end_session = True

    return build_response(session_attributes, build_speech_response(

        card_title, speech_output, reprompt_text, should_end_session))

def get_DeleteProductIntent_response(intent):


    session_attributes = {}
    
    params={
        "api_token":"insert_your_pipedrive_api_key",
        "term":intent['slots']['name']['value']
    }
    r = requests.get("https://api.pipedrive.com/v1/products/find", params=params)
    
    response=json.loads(r.content)
    
    param={
        "api_token":"insert_your_pipedrive_api_key"
    }
    if response["data"] is None:
        speech_output = "There is no Product with name " + intent['slots']['name']['value']
        card_title = "DeleteProductIntent"
        reprompt_text = "Try again by telling me the name"
        should_end_session = True
        return build_response(session_attributes, build_speech_response(card_title, speech_output, reprompt_text, should_end_session))
    id=response["data"][0]["id"]
    res = requests.delete("https://api.pipedrive.com/v1/products/" + str(id), params=param)
    card_title = "DeleteProductIntent"
    speech_output = "Product with name " + intent['slots']['name']['value'] + "deleted succesfully. You can check your CRM"

    reprompt_text = "Try again by telling me the name"

    should_end_session = True

    return build_response(session_attributes, build_speech_response(

        card_title, speech_output, reprompt_text, should_end_session))


def get_PersonDetailIntent_response(intent):

    session_attributes = {}
    params={
        "api_token":"insert_your_pipedrive_api_key",
        "term":intent['slots']['name']['value']
    }
    r = requests.get("https://api.pipedrive.com/v1/persons/find", params=params)
    
    response=json.loads(r.content)
    print(response)
    param={
        "api_token":"insert_your_pipedrive_api_key"
    }
    if response["data"] is None:
        speech_output = "There is no Person with name " + intent['slots']['name']['value']
        card_title = "PersonDetailIntent"
        reprompt_text = "Try again by telling me person's name"
        should_end_session = True
        return build_response(session_attributes, build_speech_response(card_title, speech_output, reprompt_text, should_end_session))

    id=response["data"][0]["id"]
    req = requests.get("https://api.pipedrive.com/v1/persons/"+str(id), params=param)
    res=json.loads(req.content)
   
    card_title = "PersonDetailIntent"
    speech_output = "Phone number of " + intent['slots']['name']['value'] + " is " + res["data"]["phone"][0]["value"] + " email is " + res["data"]["email"][0]["value"]

    reprompt_text = "Try again by telling me person's name"

    should_end_session = True

    return build_response(session_attributes, build_speech_response(

        card_title, speech_output, reprompt_text, should_end_session))

def get_ListActivitiesIntent_response(intent):

    session_attributes = {}
    params={
        "api_token":"insert_your_pipedrive_api_key",
        "term":intent['slots']['name']['value'] 
    }
    r = requests.get("https://api.pipedrive.com/v1/persons/find", params=params)
   
    response=json.loads(r.content)

    param={
        "api_token":"insert_your_pipedrive_api_key"
    }
    if response["data"] is None:
        card_title = "ListActivitiesIntent"
        speech_output = "There is no user in CRM with name " + intent['slots']['name']['value'] 
        reprompt_text = "Try again by telling me person's name"
        should_end_session = True
        return build_response(session_attributes, build_speech_response(card_title, speech_output, reprompt_text, should_end_session))
    id=response["data"][0]["id"]
    req = requests.get("https://api.pipedrive.com/v1/persons/"+str(id)+ "/activities", params=param)
    res=json.loads(req.content)

    
    card_title = "ListActivitiesIntent"
    
    if res["data"] is None:
        speech_output = "There is no Activity present with " + intent['slots']['name']['value'] 
    else:
        speech_output = res["data"][0]["person_name"] + " has a " + res["data"][0]["type"] + " with " + res["data"][0]["owner_name"] + " on the subject " + res["data"][0]["subject"]

    reprompt_text = "Try again by telling me person's name"

    should_end_session = True

    return build_response(session_attributes, build_speech_response(

        card_title, speech_output, reprompt_text, should_end_session))

def get_ListProductIntent_response(intent):

    session_attributes = {}
    
    
    card_title = "ListProductIntent"
    params={
        "api_token":"insert_your_pipedrive_api_key",
        "term":intent['slots']['name']['value'] 
    }

    r = requests.get("https://api.pipedrive.com/v1/persons/find", params=params)
    
    response=json.loads(r.content)
    param={
        "api_token":"insert_your_pipedrive_api_key"
    }
    if response["data"] is None:
        speech_output = "There is no Person with name " + intent['slots']['name']['value']
        reprompt_text = "Try again by telling me name" 
        should_end_session = True
        return build_response(session_attributes, build_speech_response(card_title, speech_output, reprompt_text, should_end_session))
    id=response["data"][0]["id"]
    req = requests.get("https://api.pipedrive.com/v1/persons/"+str(id)+ "/products", params=param)
    res=json.loads(req.content)
    if res["data"] is None:
        speech_output = "There is no Product attached with " + intent['slots']['name']['value']
    else:
        speech_output = "Product associated with " + intent['slots']['name']['value'] + " is " + res["data"][0]["3"]["product"]["name"]

    reprompt_text = "Try again by telling me name" 

    should_end_session = True

    return build_response(session_attributes, build_speech_response(

        card_title, speech_output, reprompt_text, should_end_session))

def get_AddPersonIntent_response(intent):

    session_attributes = {}
    
    params={
        "api_token":"insert_your_pipedrive_api_key"
    }
    data={
        "name":intent['slots']['name']['value'],
        "phone":intent['slots']['phone']['value'],
        "email":intent['slots']['email']['value']+"@gmail.com"
	}
    headers={
		"Accept": "application/json",
		"Content-Type": "application/x-www-form-urlencoded"
	}
    r = requests.post("https://api.pipedrive.com/v1/persons/persons", params=params, data=data, headers=headers)
 
    response=json.loads(r.content)

    
    card_title = "AddPersonIntent"

    speech_output = "Successfully Added a person with name " + intent['slots']['name']['value'] + " you can check your CRM know"

    reprompt_text = "Try again by telling me person's name"

    should_end_session = True

    return build_response(session_attributes, build_speech_response(

        card_title, speech_output, reprompt_text, should_end_session))

def get_DeletePersonIntent_response(intent):

    session_attributes = {}
    
    params={
        "api_token":"insert_your_pipedrive_api_key",
        "term":intent['slots']['name']['value']
    }
    r = requests.get("https://api.pipedrive.com/v1/persons/find", params=params)

    response=json.loads(r.content)

    param={
        "api_token":"insert_your_pipedrive_api_key"
    }
    if response["data"] is None:
        speech_output = "There is no Person with name " + intent['slots']['name']['value']
        card_title = "DeletePersonIntent"
        reprompt_text = "Try again by telling me person's name"
        should_end_session = True
        return build_response(session_attributes, build_speech_response(card_title, speech_output, reprompt_text, should_end_session))

    id=response["data"][0]["id"]
    res= requests.delete("https://api.pipedrive.com/v1/persons/" + str(id), params=param)

    card_title = "DeletePersonIntent"

    speech_output = "successfully deleted one contact with name " + intent['slots']['name']['value']

    reprompt_text = "Try again by telling me person's name"

    should_end_session = True

    return build_response(session_attributes, build_speech_response(

        card_title, speech_output, reprompt_text, should_end_session))

def get_ActivitiesAssignedIntent_response(intent):

    session_attributes = {}
    
    param={
        "api_token":"insert_your_pipedrive_api_key",
        "term": intent['slots']['name']['value']
    }
    r = requests.get("https://api.pipedrive.com/v1/users/find", params=param)
    response=json.loads(r.content)
    if response["data"] is None:
        speech_output = "There is no User with name " + intent['slots']['name']['value']
        card_title = "ActivitiesAssignedIntent"
        reprompt_text = "Try again by telling me users name."
        should_end_session = True
        return build_response(session_attributes, build_speech_response(card_title, speech_output, reprompt_text, should_end_session))
    param={
        "api_token":"insert_your_pipedrive_api_key",
        "user_id": response["data"][0]["id"]
    }
    req = requests.get("https://api.pipedrive.com/v1/activities", params=param)
    res=json.loads(req.content)

    
    card_title = "ActivitiesAssignedIntent"

    speech_output = intent['slots']['name']['value'] + " has a " + res["data"][0]["type"] + " with " + res["data"][0]["person_name"] + " on subject " + res["data"][0]["subject"]

    reprompt_text = "Try again by telling me users name."

    should_end_session = True

    return build_response(session_attributes, build_speech_response(

        card_title, speech_output, reprompt_text, should_end_session))

def get_AddActivityIntent_response(intent):


    session_attributes = {}
    
    params={
        "api_token":"insert_your_pipedrive_api_key",
        "term":intent['slots']['name']['value'] 
    }
    r = requests.get("https://api.pipedrive.com/v1/persons/find", params=params)

    response=json.loads(r.content)
  

    p={
        "api_token":"insert_your_pipedrive_api_key",
        "term": "name_of_the_owner"
    }
    req = requests.get("https://api.pipedrive.com/v1/users/find", params=p)

    res=json.loads(req.content)
  

    param={
        "api_token":"insert_your_pipedrive_api_key",
    }
    data={
        "subject":intent['slots']['subject']['value'],
        "type":intent['slots']['type']['value'],
        "person_id":response["data"][0]["id"],
        "user_id":res["data"][0]["id"]
    }
    headers={"Content-Type" : "application/json"}
    requ = requests.post("https://api.pipedrive.com/v1/activities", data=json.dumps(data), params=param, headers=headers)
    
    resp=json.loads(requ.content)
  
    
    card_title = "AddActivityIntent"

    speech_output = "ok done!! Your " + intent['slots']['type']['value'] + " with " + intent['slots']['name']['value'] + " has been succesfully created"

    reprompt_text = "Try again by providing name, subject and type for the meeting"

    should_end_session = True
 

    return build_response(session_attributes, build_speech_response(

        card_title, speech_output, reprompt_text, should_end_session))


def get_DeleteActivityIntent_response(intent):

    session_attributes = {}
    params={
        "api_token":"insert_your_pipedrive_api_key",
        "term":intent['slots']['name']['value'] 
    }
    r = requests.get("https://api.pipedrive.com/v1/persons/find", params=params)
   
    response=json.loads(r.content)

    param={
        "api_token":"insert_your_pipedrive_api_key"
    }
    if response["data"] is None:
        speech_output = "There is no Person with name " + intent['slots']['name']['value'] 
        card_title = "DeleteActivityIntent"
        reprompt_text = "Try again by telling me peson's name"
        should_end_session = True
        return build_response(session_attributes, build_speech_response(card_title, speech_output, reprompt_text, should_end_session))
   
    id=response["data"][0]["id"]
    req = requests.get("https://api.pipedrive.com/v1/persons/"+str(id)+ "/activities", params=param)
    res=json.loads(req.content)
    
    if res["data"] is None:
        speech_output = "There is no Activity with name " + intent['slots']['name']['value'] 
        card_title = "DeleteActivityIntent"
        reprompt_text = "Try again by telling me peson's name"
        should_end_session = True
        return build_response(session_attributes, build_speech_response(card_title, speech_output, reprompt_text, should_end_session))
    activity_id=res["data"][0]["id"]
    reques = requests.delete("https://api.pipedrive.com/v1/activities/"+str(activity_id), params=param)

    
    card_title = "DeleteActivityIntent"

    speech_output =res["data"][0]["type"] + " with " + intent['slots']['name']['value'] + " successfully deleted"

    reprompt_text = "Try again by telling me peson's name"

    should_end_session = True

    return build_response(session_attributes, build_speech_response(

        card_title, speech_output, reprompt_text, should_end_session))


def get_AddDealIntent_response(intent):

    session_attributes = {}
    params={
        "api_token":"insert_your_pipedrive_api_key"
    }
    data={
        "title":intent['slots']['title']['value'],
        "value":str(intent['slots']['value']['value']), 
        "currency": "INR"
    }
    headers={"Content-Type" : "application/json"}
    r = requests.post("https://api.pipedrive.com/v1/deals", params=params, data=json.dumps(data), headers=headers)
    
    response=json.loads(r.content)
   

    
    card_title = "AddDeleteIntent"
  
    speech_output = "successfully added a new deal with title " + intent['slots']['title']['value'] + " and having a value of " + intent['slots']['value']['value'] + " INR"

    reprompt_text = "Try again by providing the title and value for the deal"

    should_end_session = True

    return build_response(session_attributes, build_speech_response(

        card_title, speech_output, reprompt_text, should_end_session))


def get_DetailOfDealIntent_response(intent):

    session_attributes = {}
    param={
        "api_token":"insert_your_pipedrive_api_key",
        "term": intent['slots']['dealname']['value']
    }
    r = requests.get("https://api.pipedrive.com/v1/deals/find", params=param)
    
    response=json.loads(r.content)
    
    
    card_title = "DetailOfDeleteIntent"
    if response["data"] is None:
        speech_output = "There is no Deal with name " + intent['slots']['dealname']['value']
    else:
        speech_output = intent['slots']['dealname']['value'] + " has worth of " + str(response["data"][0]["value"]) + " INR"

    reprompt_text = "Try again by telling me deals"

    should_end_session = True

    return build_response(session_attributes, build_speech_response(

        card_title, speech_output, reprompt_text, should_end_session))



def get_DeleteDealIntent_response(intent):

    session_attributes = {}

    params={
        "api_token":"insert_your_pipedrive_api_key",
        "term":intent['slots']['dealname']['value']
    }
    r = requests.get("https://api.pipedrive.com/v1/deals/find", params=params)
    
    response=json.loads(r.content)
  
    param={
        "api_token":"insert_your_pipedrive_api_key"
    }
    if response["data"] is None:
        speech_output = "There is no Deal with name " + intent['slots']['dealname']['value']
        card_title = "DeleteDealIntent"
        reprompt_text = "Try again by telling me deal name"
        should_end_session = True
        return build_response(session_attributes, build_speech_response(card_title, speech_output, reprompt_text, should_end_session))
    
    id=response["data"][0]["id"]
    res= requests.delete("https://api.pipedrive.com/v1/deals/" + str(id), params=param)
    card_title = "DeleteDealIntent"
  
    speech_output = "successfully deleted " + intent['slots']['dealname']['value']

    reprompt_text = "Try again by telling me deal name"

    should_end_session = True

    return build_response(session_attributes, build_speech_response(

        card_title, speech_output, reprompt_text, should_end_session))



def get_welcome_response():

    session_attributes = {}

    card_title = "Welcome"

    speech_output = "Welcome to CRM management. I’ll explain a couple things you can do and keep in mind, you can ask for ‘help’ any time for assistance. CRM management can manage deals, activites, contacts and product in customer relationship management(CRM) software using voice commands . What will you like to do today?"


    reprompt_text = "I don't know if you heard me, Welcome to your CRM. What will you like to do today"
    should_end_session = False

    return build_response(session_attributes, build_speech_response(

        card_title, speech_output, reprompt_text, should_end_session))


def get_help_response():

    session_attributes = {}

    card_title = "Welcome"

    speech_output = "Welcome to your CRM Help. Customer relationship management (CRM) is an approach to managing a company's interaction with current and potential customers. It uses data analysis about customers' history with a company to improve business relationships with customers, specifically focusing on customer retention and ultimately driving sales growth. This includes contact management, lead management, deal tracking,product management and activity management. I can automate your CRM portal over voice commands. What will you like to do today?"


    reprompt_text = "I don't know if you heard me, Welcome to your CRM help."
    should_end_session = False

    return build_response(session_attributes, build_speech_response(

        card_title, speech_output, reprompt_text, should_end_session))




def handle_session_end_request():

    card_title = "Session Ended"

    speech_output = "Remember I can help you with CRM management anytime. Thank you for using CRM management." 

    # Setting this to true ends the session and exits the skill.

    should_end_session = True

    return build_response({}, build_speech_response(

        card_title, speech_output, None, should_end_session))



# --------------- Events ------------------



def on_session_started(session_started_request, session):

    """ Called when the session starts.

        One possible use of this function is to initialize specific 

        variables from a previous state stored in an external database

    """

    # Add additional code here as needed

    pass



    



def on_launch(launch_request, session):

    """ Called when the user launches the skill without specifying what they

    want

    """

    # Dispatch to your skill's launch message

    return get_welcome_response()





def on_intent(intent_request, session):

    """ Called when the user specifies an intent for this skill """



    intent = intent_request['intent']

    intent_name = intent_request['intent']['name']



    # Dispatch to your skill's intent handlers

    if intent_name == "OneProductIntent":

        return get_OneProductIntent_response(intent)

    elif intent_name == "DealProductIntent":

        return get_DealProductIntent_response(intent)

    elif intent_name == "DeletePersonIntent":

        return get_DeletePersonIntent_response(intent)

    elif intent_name == "ActivitiesAssignedIntent":

        return get_ActivitiesAssignedIntent_response(intent)

    elif intent_name == "AddActivityIntent":

        return get_AddActivityIntent_response(intent)

    elif intent_name == "AddDealIntent":

        return get_AddDealIntent_response(intent)

    elif intent_name == "DetailOfDealIntent":

        return get_DetailOfDealIntent_response(intent)

    elif intent_name == "DeleteDealIntent":

        return get_DeleteDealIntent_response(intent)


    elif intent_name == "AMAZON.HelpIntent":

        return get_help_response()

    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":

        return handle_session_end_request()

    else:

        raise ValueError("Invalid intent")





def on_session_ended(session_ended_request, session):

    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true

    """

    print("on_session_ended requestId=" + session_ended_request['requestId'] +

          ", sessionId=" + session['sessionId'])

    # add cleanup logic here





# --------------- Main handler ------------------



def lambda_handler(event, context):


    print("Incoming request...")



    """

    Uncomment this if statement and populate with your skill's application ID to

    prevent someone else from configuring a skill that sends requests to this

    function.

    """

    # if (event['session']['application']['applicationId'] !=

    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):

    #     raise ValueError("Invalid Application ID")



    if event['session']['new']:

        on_session_started({'requestId': event['request']['requestId']},

                           event['session'])



    if event['request']['type'] == "LaunchRequest":

        return on_launch(event['request'], event['session'])

    elif event['request']['type'] == "IntentRequest":

        return on_intent(event['request'], event['session'])

    elif event['request']['type'] == "SessionEndedRequest":

        return on_session_ended(event['request'], event['session'])





