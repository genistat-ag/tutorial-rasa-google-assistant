import logging
from typing import Any, Dict, List, Text

from rasa.core.channels.channel import InputChannel, OutputChannel, UserMessage
from sanic import Blueprint, response
from sanic.request import Request

logger = logging.getLogger(__name__)


class GoogleAssistantOutput(OutputChannel):
    """Output channel that collects send messages in a list"""

    # TODO: Implement all of the following functions to match the Google Speech APIs JSON format. See README.

    def __init__(self):
        self.messages = []

    @classmethod
    def name(cls):
        return 'google_assistant'

    @staticmethod
    def _message(recipient_id, text=None, image=None, buttons=None, attachment=None, custom=None):
        obj = {
            'recipient_id': recipient_id,
            'text': text,
            'image': image,
            'buttons': buttons,
            'attachment': attachment,
            'custom': custom,
        }
        return {k: v for k, v in obj.items() if v is not None}

    def latest_output(self):
        if self.messages:
            return self.messages[-1]
        else:
            return None

    async def send_text_message(self, recipient_id: Text, text: Text, **kwargs: Any) -> None:
        for message_part in text.split('\n\n'):
            await self.messages.append(self._message(recipient_id, text=message_part))

    async def send_image_url(self, recipient_id: Text, image: Text, **kwargs: Any) -> None:
        await self.messages.append(self._message(recipient_id, image=image))

    async def send_attachment(self, recipient_id: Text, attachment: Text, **kwargs: Any) -> None:
        await self.messages.append(self._message(recipient_id, attachment=attachment))

    async def send_text_with_buttons(
            self,
            recipient_id: Text,
            text: Text,
            buttons: List[Dict[Text, Any]],
            **kwargs: Any
    ) -> None:
        await self.messages.append(self._message(recipient_id, text=text, buttons=buttons))

    async def send_custom_json(self, recipient_id: Text, json_message: Dict[Text, Any], **kwargs: Any) -> None:
        await self.messages.append(self._message(recipient_id, custom=json_message))


class GoogleAssistantInput(InputChannel):
    """Google Assistant Input Channel that parses requests coming from and going to the Google API"""

    @classmethod
    def name(cls):
        """
        Unique identifier for the input channel
        """
        return 'google_assistant'

    def blueprint(self, on_new_message):
        """
        Sub-routing for Google Assistant Input Channel
        """
        google_assistant_webhook = Blueprint('google_assistant_webhook', __name__)

        @google_assistant_webhook.route('/', methods=['GET'])
        async def health(request: Request):
            """
            Endpoint that signals readiness and healthiness
            """
            return response.json({"status": "ok"})

        @google_assistant_webhook.route('/webhook', methods=['POST'])
        async def receive(request: Request):
            """
            Webhook endpoint that is called by Google API
            """
            payload = request.json
            user_id = payload['user']['userId']
            intent = payload['inputs'][0]['intent']
            query = payload['inputs'][0]['rawInputs'][0]['query']

            if intent == 'actions.intent.MAIN':
                message = '<speak>Hello! <break time="0.3"/>I am an example Bot.</speak>'
            else:
                output_channel = GoogleAssistantOutput()
                await on_new_message(
                    UserMessage(query, output_channel, user_id, input_channel=GoogleAssistantInput.name()))
                message = [message['text'] for message in output_channel.messages][0]
                logger.debug(output_channel.messages)

            response_json = {
                "conversationToken": "{\"state\":null,\"data\":{}}",
                "expectUserResponse": 'true',
                "expectedInputs": [
                    {
                        "inputPrompt": {
                            "initialPrompts": [
                                {
                                    # This is a very basic MVP that can only return text answers from the bot!
                                    "ssml": f'<speak>{message}</speak>'
                                }
                            ]
                        },
                        "possibleIntents": [
                            {
                                "intent": "actions.intent.TEXT"
                            }
                        ]
                    }
                ]
            }
            return response.json(response_json)

        return google_assistant_webhook
