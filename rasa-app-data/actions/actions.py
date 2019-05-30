# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import requests
import json
import yaml
from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet

logger = logging.getLogger(__name__)


with open("config/credentials.yml") as f:
    credentials = yaml.safe_load(f)

class ActionSearchLink(Action):
    def name(self):
        return "action_search_link"

    def run(self, dispatcher, tracker, domain):
        slots = tracker.current_slot_values()

        logger.error("SLOTS: {}".format(slots))

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
