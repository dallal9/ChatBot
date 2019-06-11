# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import requests
import json
import yaml
from logging.handlers import RotatingFileHandler
from rasa_core_sdk import Action

from rasa_core_sdk.events import SlotSet
from typing import List, Text, Optional, Dict, Any
from pythonjsonlogger import jsonlogger


logger = logging.getLogger(__name__)
logger2 = logging.getLogger(__name__ + "2")


def init_logger(logger):
    handler = RotatingFileHandler("logs/actions.json", maxBytes=4194304, backupCount=256, encoding="utf-8")
    formatter = jsonlogger.JsonFormatter()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
init_logger(logger)


with open("config/credentials.yml") as f:
    credentials = yaml.safe_load(f)


class ActionLog(Action):
    def name(self):
        return "action_log"

    def run(self, dispatcher, tracker, domain):
        slots = tracker.current_slot_values()

        data = tracker.current_state()
        data.pop("events", None)
        logger.debug(data)
        return []


class ActionSearchLink(Action):
    def name(self):
        return "action_search_link"

    def run(self, dispatcher, tracker, domain):
        slots = tracker.current_slot_values()

        payment = slots["property_payment"]
        typ = slots["property_type"]
        location = slots["property_location"]
        search_link = "https://propertyup.com/{}/{}-{},illinois".format(
            payment,
            typ,
            location
        )
        dispatcher.utter_message(search_link)


class ActionMessengerName(Action):
    def name(self):
        return "action_messenger_name"

    def run(self, dispatcher, tracker, domain):
        most_recent_state = tracker.current_state()
        sender_id = most_recent_state["sender_id"]
        fb_access_token = credentials["facebook"]["page-access-token"]

        r = requests.get("https://graph.facebook.com/{}?fields=first_name,last_name,profile_pic&access_token={}".format(sender_id, fb_access_token)).json()
        first_name = r["first_name"]
        last_name = r["last_name"]
        return [SlotSet("first_name", first_name), SlotSet("last_name", last_name)]


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


class ActionCustomFallback(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_custom_fallback"

    def run(self, dispatcher, tracker, domain):
        ActionLog.run(self, dispatcher, tracker, domain)
        message = tracker.latest_message["text"]
        # send the message back to the user
        dispatcher.utter_message("sorry, I don't understand, "+str(message))
        return []
