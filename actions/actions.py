import logging
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

log = logging.getLogger(__name__)


class ActionExample(Action):
    """Dummy action used as an example"""

    def name(self) -> Text:
        return 'action_example'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message('This is an example, replace me with an actual action.')
        return []
