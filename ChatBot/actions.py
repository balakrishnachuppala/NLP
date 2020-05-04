# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.forms import FormAction

#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

class ActionCaronaSearch(Action):
    def name(self) -> Text:
        return "action_carona_search"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response=requests.get('https://api.covid19india.org/data.json').json()
        entities = tracker.latest_message['entities']
        print(entities)
        state="No State"
        for e in entities:
             if (e['entity']=='state'):
                 state=e['value']


        print('\nState value: ',state)
        message="Enter correct state name"

        if ((state=='india') or (state=='India')):
            state='Total'
        try:
            for data in response['statewise']:
                if ((data['state'].lower().find(state.lower()))!=-1):
                    print("\nIn data loop: data: {} \t state: {} \n".format(data['state'],state))
                    message = "\n"+state.title()+" Carona Details : \n" + "\n\nState Code : " + data["statecode"] + "\nActive : " + data["active"] + "\nConfirmed: " + data["confirmed"] + "\nDeaths:" + data["deaths"] + "\nDelta Confirmed: " + data["deltaconfirmed"] + "\nDelta Deaths: " + data["deltadeaths"] + "\nDelta Recovered:" + data["deltarecovered"] + "\nStats updated on : " + data["lastupdatedtime"] + "\nRecovered : " + data["recovered"] + "\nState Notes : " + data["statenotes"] + "\n"

            if('state'==""):
                message="No Info, Please check the state name"
        except:
            pass


        dispatcher.utter_message(text=message)
        return []
