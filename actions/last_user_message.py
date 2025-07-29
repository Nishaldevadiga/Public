
##########################################################################################
##########################################################################################
#
#   Developed by Atef Bader,PhD
#   Last Edit: 11/13/2024
#
##########################################################################################
##########################################################################################



from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import re

# class ActionLastUserMessage(Action):
#     def name(self) -> Text:
#         return "last_user_message"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         # Retrieve the last user message
#         last_user_message = tracker.latest_message.get('text')
        
     
#         clothing_keywords = ["hoodie", "shirt", "t-shirt", "pants", "shorts", "clothing", "jacket", "sweatshirt", "top","Nike clothing"]
#         if any(word in last_user_message.lower() for word in clothing_keywords):
#             valid_request = "Nike clothing"
#             print("Buy Nike clothing")
#         elif "order status" in last_user_message.lower():
#             valid_request = "order status"
#             print("Order Status")
#         else:
#             valid_request = "out of scope"
#             print("Out of Scope")


 
#         if valid_request :
#             return [ SlotSet("request_type", valid_request)]


class ActionLastUserMessage(Action):
    def name(self) -> Text:
        return "last_user_message"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Retrieve the last user message
        last_user_message = tracker.latest_message.get('text')

        clothing_keywords = ["hoodie", "shirt", "t-shirt", "pants", "shorts", "clothing", "jacket", "sweatshirt", "top", "Nike clothing"]
        events = []
        order_keywords=["order status","status","order number"]

        print(last_user_message.lower())

        if any(word in last_user_message.lower() for word in clothing_keywords):
            valid_request = "Nike clothing"
            print("Buy Nike clothing")
        elif any(word in last_user_message.lower() for word in order_keywords):
            valid_request = "order status"
            print("Order Status")
            # Extract order number if present
            order_number_match = re.search(r'order(?: number)?[^\d]*(\d+)', last_user_message.lower())
            if order_number_match:
                order_number = order_number_match.group(1)
                print(f"Extracted order number: {order_number}")
                events.append(SlotSet("order_number", order_number))
        else:
            valid_request = "out of scope"
            print("Out of Scope")

        if valid_request:
            events.append(SlotSet("request_type", valid_request))
            return events
    
    
