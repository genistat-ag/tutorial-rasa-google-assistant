# Google Assistant for Rasa with docker-compose
This is heavily based on the official Rasa [tutorial](https://blog.rasa.com/going-beyond-hey-google-building-a-rasa-powered-google-assistant/). I assume that you are familiar with Rasa, the mentioned tutorial and docker-compose.

## Google Assistant Bot
As the Google Assistant integration is not a default channel in Rasa it has to be added as a [custom channel](https://rasa.com/docs/rasa/user-guide/connectors/custom-connectors/).

### What it can and cannot do?
The Google Assistant implementation is functionally working for text based interactions but is crashing as soon as the chatbot returns anything other than text. E.g. when it tries to return custom JSON. So one would have to implement a proper OutputChannel as is already present for e.g. [Telegram](https://github.com/RasaHQ/rasa/blob/master/rasa/core/channels/telegram.py), with the code skeleton that is already present in `custom/google_assistant_channel.py`.

For now we just collect all message like we do in the [CollectingOutputChannel](https://github.com/RasaHQ/rasa/blob/master/rasa/core/channels/channel.py#L275).

These resources will be of help, if you plan on going further with the implementation. Feel free to fork this repository and work further on it:
* https://developers.google.com/actions/assistant/responses - Response API
* https://developers.google.com/actions/reference/ssml - SSML language reference
* https://github.com/sumsted/pyssml - Python Package for SSML generation

## What's in this repository?
This repository consists of the following files and directories:  
- **actions** - The Package with your custom Rasa Actions
- **config** - Your Rasa configuration files (e.g. config.yml, domain.yml and endpoints.yml)
- **custom** - The Google Assistant Connector Package
- **data** - The training data for the Rasa NLU and Core (.md files)
- **secrets** - Your secrets files (e.g. credentials.yml)

## Train model
To train the model simply run the `train.sh` script and watch the output for errors.

## Run Bot locally
To run the bot locally you first have to train the model, see the "Train Model" section. Then you will have to setup a public domain with e.g. `ngrok http 5005` which links a public domain to localhost:5005.

For the next steps you need to set up a Google Actions Project as described in the official Rasa [tutorial](https://blog.rasa.com/going-beyond-hey-google-building-a-rasa-powered-google-assistant/).

Then update the ngrok domains in `custom/action.json` and use
```
gactions update --action_package custom/action.json --project example-chatbot
gactions test --action_package custom/action.json --project example-chatbot
``` 
to push the action changes to the test setup of Google. The last step you will have repeat with every change in the domain.
