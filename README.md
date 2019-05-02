# ChatBot
ChatBot

# Instructions

A quick way to test it is to:
- Fill out the `rasa-app-data/config/credentials.yml` with your facebook credentials.
- Run `docker-compose up`
- Wait until everything is started
- Send `Hi` to the bot on messenger, wait until the nlu model is loaded, you should receive an answer after a little while

NOTE: It seems that, when the model just got loaded, we receive the answer multiple times. We should probably look for a fix.
Once the model is loaded, it works fine.

# Folders

Here are the folders description:
```
rasa-app-data/
- actions/
  - actions.py             Contains the custom actions, each action can probably be separated in its own file
- config/
  - credentials.yml        The credentials to connect the bot with messenger
  - endpoints.yml          The urls to the nlu service and the action service
- models/
  - current/
    - dialogue/            The trained rasa_core model
    - nlu/                 The trained rasa_nlu model
- project/                  I'm not sure yet
```
