##########################################################################################
##########################################################################################
#
#   Developed by Atef Bader,PhD
#   Last Edit: 11/13/2024
#
##########################################################################################
##########################################################################################



from typing import Any, Dict
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from actions.db import get_product
from actions.Using_GPT4_Vision_With_Function_Calling import delivery_exception_support_handler
from actions.Recommender_Embeddings.Recommendations_using_embedding import print_recommendations_from_strings

import pandas as pd

product_catalog_path = "actions/Recommender_Embeddings/data/product_catalog_ass.csv"

class RecommendProduct(Action):

    def name(self) -> str:
        return "recommend_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[str, Any]):

        # load data 
        df = pd.read_csv(product_catalog_path)

        customer_name = tracker.get_slot("customer_name")
        customer_preferences = tracker.get_slot("customer_preferences_for_product_purchase")

        if customer_name is None or customer_preferences is None:
            return [SlotSet("return_value", "data_not_present")]
        
        print('\n', 'Prefernces = ', customer_preferences,'\n')
        
        recommended_product_indices = print_recommendations_from_strings(customer_preferences,1)
        print('\n RecommendedProductIndices=', recommended_product_indices, '\n')

        recommended_product_photo = df.loc[recommended_product_indices[0], 'Photo']
        print('\n Model REcommended=', recommended_product_photo, '\n')

        recommended_product_name = df.loc[recommended_product_indices[0], 'Model']
        recommended_product_number = df.loc[recommended_product_indices[0], 'Price']

        return [SlotSet("product_name", recommended_product_name), 
                SlotSet("product_number", recommended_product_number), 
                SlotSet("photo", recommended_product_photo)
                ]
    
