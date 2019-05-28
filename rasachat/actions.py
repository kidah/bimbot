# -*- coding: utf-8 -*-
import logging, sys
from datetime import datetime
from typing import Text, Dict, Any, List
import json
import requests
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
        conn = sqlite3.connect('./data/sqlite2.db')
        # Create a cursor
        c = conn.cursor()
        # Execute the query
        if t is not None:
            c.execute(query, t)
            results = c.fetchall()
            logger.info(results)
            return results
        else:
            logger.info(query)
            c.execute(query)
            results = c.fetchall()
		    # Extract the row headers
            row_headers=[x[0] for x in c.description]
            # Return the results
            json_data= []
            for result in results:
                json_data.append(dict(zip(row_headers,result)))
            #logger.info(json_data[0]['id'])
            return json_data
    except IOError:
        return "Database connection error"


class ActionGreetUser(Action):
    """Greets the user with/without privacy policy"""

    def name(self):
        return "action_greet"
   
    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message["intent"].get("name")
        shown_privacy = tracker.get_slot("shown_privacy")
        name_entity = next(tracker.get_latest_entity_values("name"), None)
        username = tracker.get_slot("name")
        logger.info(name_entity)
        if intent == "greet":
            if shown_privacy and username:
                dispatcher.utter_template("utter_greet_name", tracker, name=username)
                return []
            elif username is None:
                dispatcher.utter_template("utter_greet", tracker)
                dispatcher.utter_template("utter_ask_name", tracker)
                return []
            else:
                dispatcher.utter_template("utter_whatspossible", tracker)
                #dispatcher.utter_template("utter_inform_privacypolicy", tracker)
                dispatcher.utter_template("utter_ask_goal", tracker)
                return [SlotSet("shown_privacy", True)]	

        elif not shown_privacy and intent == "enter_data" and name_entity:
            dispatcher.utter_template("utter_greet_name", tracker, name=name_entity)
            dispatcher.utter_template("utter_whatspossible", tracker)
            #dispatcher.utter_template("utter_inform_privacypolicy", tracker)
            dispatcher.utter_template("utter_ask_goal", tracker)
            return [SlotSet("shown_privacy", True), SlotSet("name", name_entity)]

        elif intent == "enter_data" and name_entity is None:
            dispatcher.utter_template("utter_namenotrecognised", tracker, name=name_entity)
            return []
        return []

class ActionProject(Action):
    """Returns the chitchat utterance dependent on the intent"""

    def name(self):
        return "action_project_info"

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message["intent"].get("name")
        message = tracker.latest_message['text']
        projectname = tracker.get_slot("projectname")
        summary_terms = ["brief", "summary", "description", "run-through"]
        projectname_entity = next(tracker.get_latest_entity_values("projectname"), None)
        match_brief = [item for item in summary_terms if re.search(item, message)]
        entities = tracker.latest_message["entities"]
        logger.info(entities)
        # retrieve the correct chitchat utterance dependent on the intent tell me a summary of the project and gfa tell me the frame type of the building
        if intent == 'project_information':
            if projectname is not None and match_brief:
                query = 'SELECT * FROM project where Name="{}"'.format(projectname)
                res = db_conn(query)
                result = res[0]
                message = result["Name"] + " is a " + result["ProjectValue"] + " project for " + result["ClientName"] + " situated at " + result["Address"] + ". It is a " + result["ConstructionType"] + " project with a " + result["Duration"] + " duration."
                dispatcher.utter_message(message)
                dispatcher.utter_template("utter_askwhatelse", tracker)

            elif entities and projectname is None:
                ents = [ent['entity'] for ent in entities if ent != 'projectname']
                dispatcher.utter_template("utter_ask_projectname", tracker)
                return [SlotSet("psearch_request", ents)]

            elif not entities:
                 dispatcher.utter_template("utter_canthelp", tracker)

            else:
                params = ', '.join([i['entity'] for i in entities if i['entity'] != 'projectname'])
                query = 'select ' + params + ' from project where Name = "{}"'.format(projectname)
                res = db_conn(query)
                if not res:
                    dispatcher.utter_template("utter_projectdoesnotexist", tracker)
                else:
                    result = res[0]
                    message = ', '.join([result[param] for param in result])
                    dispatcher.utter_message(message) 
        elif intent == 'enter_data' and projectname_entity:
            #  check requested slot values to affect query
            psearch_request = tracker.get_slot("psearch_request")
            if psearch_request:
                params = ', '.join([i for i in psearch_request])
                query = 'select ' + params + ' from project where Name = "{}"'.format(projectname)
                res = db_conn(query)
                if not res:
                    dispatcher.utter_template("utter_projectdoesnotexist", tracker)
                else:
                    result = res[0]
                    message = ', '.join([result[param] for param in result])
                    dispatcher.utter_message(message)
                    return [SlotSet("psearch_request", [])]
            elif not psearch_request:
                query = 'SELECT * FROM project where Name="{}"'.format(projectname_entity) 
                res = db_conn(query)
                if not res:
                    dispatcher.utter_template("utter_projectdoesnotexist", tracker)
                else:
                    result = res[0]
                    message = result["Name"] + " is a " + result["ProjectValue"] + " project for " + result["ClientName"] + " situated at " + result["Address"] + ". It is a " + result["ConstructionType"] + " project with a " + result["Duration"] + " duration."
                    dispatcher.utter_message(message)
                    dispatcher.utter_template("utter_anything_else", tracker)
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

        
class ActionChitchat(Action):
    """Returns the chitchat utterance dependent on the intent"""

    def name(self):
        return "action_chitchat"

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message["intent"].get("name")
        entities = tracker.latest_message["entities"]
        logger.info(entities)
        # retrieve the correct chitchat utterance dependent on the intent
        if intent == 'bot_chitchat':
            #
            if not entities:
                dispatcher.utter_template("utter_canthelp", tracker)
            else:
                params = ', '.join([i['entity'] for i in entities])
                query = 'select ' + params + ' from bot '
                res = db_conn(query)
                result = res[0]
                message = ', '.join([result[param] for param in result])
                logger.info(message)
                dispatcher.utter_message(message)
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


