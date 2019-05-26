# -*- coding: utf-8 -*-
import logging, sys
from datetime import datetime
from typing import Text, Dict, Any, List
import json
import sqlite3
import re


from rasa_core_sdk import Action, Tracker, ActionExecutionRejection
from rasa_core_sdk.executor import CollectingDispatcher
from rasa_core_sdk.forms import FormAction, REQUESTED_SLOT
from rasa_core_sdk.events import (
    SlotSet,
	UserUttered,
    UserUtteranceReverted,
    ConversationPaused,
    FollowupAction,
    Form,
)

logger = logging.getLogger(__name__)

def db_conn(query, t=None):
    try:
        # Open connection to DB
        conn = sqlite3.connect('./data/sqlite.db')
        # Create a cursor
        c = conn.cursor()
        # Execute the query
        if t is not None:
            c.execute(query, t)
            results = c.fetchall()
            logger.info(results)
            return results
        else:
            c.execute(query)
            results = c.fetchall()
		    # Extract the row headers
            row_headers=[x[0] for x in c.description]
            # Return the results
            logger.info(query)
            logger.info(results)
            json_data= []
            for result in results:
                json_data.append(dict(zip(row_headers,result)))
            #logger.info(json_data[0]['id'])
            return json_data
    except IOError:
        return "Database connection error"

class UserNameForm(FormAction):
   """Example of a custom form action"""

   def name(self):
       # type: () -> Text
       """Unique identifier of the form"""

       return "getusername_form"

   @staticmethod
   def required_slots(tracker):
       # type: () -> List[Text]
       """A list of required slots that the form has to fill"""
       return ["name"]

   def slot_mappings(self):
        return {
            "name": [
                self.from_entity(entity="name"),
                self.from_text(intent="enter_data"),
            ]
        }
   def validate_name(self, value, dispatcher, tracker, domain):
        """Check to see if an name entity was actually picked up by duckling."""

        if any(tracker.get_latest_entity_values("name")):
            # entity was picked up, validate slot
            return {"name": value}
        #else:
            # no entity was picked up, we want to ask again
            #dispatcher.utter_template("utter_ask_name", tracker)
        #    return {"name": None}

   def submit(self, dispatcher, tracker, domain):
       # type: (CollectingDispatcher, Tracker, Dict[Text, Any]) -> List[Dict]
       """Define what the form has to do
           after all required slots are filled"""
       # utter submit template
       name_entity = tracker.get_slot("name")
       if name_entity:
            dispatcher.utter_template('utter_greet_name', tracker)
       else:
            dispatcher.utter_template('utter_greet', tracker)
       return [SlotSet("name", name_entity)]


class ActionGreetUser(Action):
    """Greets the user with/without privacy policy"""

    def name(self):
        return "action_greet"
   
    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message["intent"].get("name")
        shown_privacy = tracker.get_slot("shown_privacy")
        name_entity = next(tracker.get_latest_entity_values("name"), None)
  
        if intent == "greet":
            if shown_privacy and name_entity and name_entity.lower() != "sara":
                dispatcher.utter_template("utter_greet_name", tracker, name=name_entity)
                return [SlotSet("name", name_entity)]
            elif shown_privacy:
                dispatcher.utter_template("utter_greet_noname", tracker)
                return []
            else:
                dispatcher.utter_template("utter_greet", tracker)
                dispatcher.utter_template("utter_whatspossible", tracker)
                dispatcher.utter_template("utter_inform_privacypolicy", tracker)
                dispatcher.utter_template("utter_ask_goal", tracker)
                return [SlotSet("shown_privacy", True)]	
        elif not shown_privacy and intent == "enter_data":
            dispatcher.utter_template("utter_greet_name", tracker)
            dispatcher.utter_template("utter_inform_privacypolicy", tracker)
            return [SlotSet("shown_privacy", True), SlotSet("name", name_entity)]
        elif shown_privacy:
            dispatcher.utter_template("utter_greet", tracker)
        return []

class ActionProject(Action):
    """Returns the chitchat utterance dependent on the intent"""

    def name(self):
        return "action_project_info"

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message["intent"].get("name")
        ents = ["start_date", "end_date", "value", "name", "type", "construction_type", "contract_type", "job_number", "address", "business_unit", "duration"]
        message = tracker.latest_message['text']
        summary_terms = ["brief", "summary", "description", "run-through"]
        match_brief = [item for item in summary_terms if re.search(item, message)]
        # retrieve the correct chitchat utterance dependent on the intent
        if intent == 'project_information':
            entities = [i for i in ents if next(tracker.get_latest_entity_values(i), None) is not None]
            if not entities and match_brief:
                params = ', '.join(ents)
                query = "select * from project"
                res = db_conn(query)
                result = res[0]
                message = "this project is a " + result["construction_type"]  + ", of an " + result["name"] + " located at "
                + result["address"] + ". It has a " + result["contract_type"] + " contract and lasts for " + result["duration"] + " and costs "
                + result["value"]
                dispatcher.utter_message("hello")
            elif entities:
                params = ', '.join(entities)
                query = "select " + params + " from project"
                res = db_conn(query)
                result = res[0]
                data = ', '.join([result[param] for param in entities])
                dispatcher.utter_message("the " + params +  " of the building is " + str(data))
            else:
                dispatcher.utter_template("utter_default", tracker)      
        return []
        
class ActionProjectIssues(Action):
	def name(self):
		return 'action_project_issues'
		
	def run(self, dispatcher, tracker, domain):
		intent = tracker.latest_message["intent"].get("name")
		entities = tracker.latest_message["entities"]
		message = tracker.latest_message['text']
		query_type = ['how many', 'count']
        # retrieve the correct chitchat utterance dependent on the intent
		if intent == 'search_project_issues':
			params = {}
			for ent in entities:
				params[ent["entity"]] = str(ent["value"])
			count_response = False
			if any([word in message for word in query_type]):
				query = 'SELECT COUNT(*) FROM issues'
				count_response = True
			else:
				query = 'SELECT * FROM issues'
                # Add filter clauses for each of the parameters
				if len(params) > 0:
					filters = ["{}=?".format(k) for k in params]
					query += " WHERE " + " and ".join(filters)
                # Create the tuple of values
			t = tuple(params.values())
			result = db_conn(query, t=t)
			data = ', '.join([res[1] for res in result])
			dispatcher.utter_message("the project issues are " + str(data))
		return []

class ActionProjectDesign(Action):
    """Returns the chitchat utterance dependent on the intent"""

    def name(self):
        return "action_project_design"

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message["intent"].get("name")
        ents = ["gfa", "levels", "volume", "prefab", "insitu", "frameType"]
        message = tracker.latest_message['text']
        summary_terms = ["brief", "summary", "description", "run-through"]
        match_brief = [item for item in summary_terms if re.search(item, message)]
        logger.info(match_brief)
        # retrieve the correct chitchat utterance dependent on the intent
        if intent == 'search_design_data':
            entities = [i for i in ents if next(tracker.get_latest_entity_values(i), None) is not None]
            if not entities and match_brief:
                params = ', '.join(ents)
                query = "select * from design"
                res = db_conn(query)
                result = res[0]
                logger.info(res[0])
                message = "the project has a volume of " + result["volume"] + ", gross floor area of " + result["gfa"] + ", " + result["frameType"] + " frames and " + result["levels"] + " levels"
                dispatcher.utter_message(message)
            elif entities:
                params = ', '.join(entities)
                query = "select " + params + " from design"
                res = db_conn(query)
                result = res[0]
                #logger.info(result[0]['volume'])
                data = ', '.join([result[param] for param in entities])
                dispatcher.utter_message("the " + params +  " of the building is " + str(data))
            else:
                dispatcher.utter_template("utter_default", tracker)      
        return []
        
class ActionChitchat(Action):
    """Returns the chitchat utterance dependent on the intent"""

    def name(self):
        return "action_chitchat"

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message["intent"].get("name")
        ents = ["book","movie", "nationality", "courseStudied", "gender", "name", "food", "employer", "hobbies"]
        # retrieve the correct chitchat utterance dependent on the intent
        if intent == 'bot_chitchat':
            entities = [i for i in ents if next(tracker.get_latest_entity_values(i), None) is not None]
            #logger.info(entities)
            if not entities:
                dispatcher.utter_template("utter_canthelp", tracker)
            else:
                params = ', '.join(entities)
                query = "select " + params + " from bot"
                res = db_conn(query)
                result = res[0]
                data = ', '.join([result[param] for param in entities])
                #logger.info(result)
                dispatcher.utter_message("my "+ params + " is " + str(data))
        return []

class ActionJoke(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_joke"

    def run(self, dispatcher, tracker, domain):
        # what your action should do
        request = json.loads(
            requests.get("https://api.chucknorris.io/jokes/random").text
        )  # make an api call
        joke = request["value"]  # extract a joke from returned json response
        dispatcher.utter_message(joke)  # send the message back to the user
        return []
	
class ActionPause(Action):
    """Pause the conversation"""

    def name(self):
        return "action_pause"

    def run(self, dispatcher, tracker, domain):
        return [ConversationPaused()]


