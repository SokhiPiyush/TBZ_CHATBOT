from typing import Any, Dict, List, Text
from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

class ValidateTravelForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_travel_form"

    async def required_slots(self, slots_mapped_in_domain: List[Text], dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[Text]:
        required = ["destination_country"]
        dest = tracker.get_slot("destination_country")
        if dest and dest.lower() == "thailand":
            required.append("cities")
            cities = tracker.get_slot("cities") or []
            if isinstance(cities, str):
                cities = [c.strip().title() for c in cities.split(',')]
            for city in ["Bangkok", "Pattaya", "Phuket", "Krabi"]:
                if city in cities:
                    required.append(f"nights_{city}")
        required += ["pax", "travel_date"]
        return required

    def validate_destination_country(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if str(slot_value).lower() in ["thailand", "singapore"]:
            return {"destination_country": slot_value.title()}
        dispatcher.utter_message(text="Please choose either Thailand or Singapore.")
        return {"destination_country": None}

    def validate_cities(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        valid = {"bangkok", "pattaya", "phuket", "krabi"}
        if isinstance(slot_value, str):
            cities = [c.strip().title() for c in slot_value.split(",") if c.strip().lower() in valid]
        else:
            cities = []
        if cities:
            return {"cities": cities}
        dispatcher.utter_message(text="Please select valid cities: Bangkok, Pattaya, Phuket, Krabi")
        return {"cities": None}

    def validate_pax(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        try:
            pax = int(slot_value)
            if 1 <= pax <= 10:
                return {"pax": pax}
        except Exception:
            pass
        dispatcher.utter_message(text="Number of Pax must be between 1 and 10")
        return {"pax": None}

    def validate_travel_date(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if isinstance(slot_value, str) and len(slot_value.split()) == 3:
            return {"travel_date": slot_value}
        dispatcher.utter_message(text="Please enter date in format DD MMM YYYY")
        return {"travel_date": None}

    def validate_nights_Bangkok(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        return self._validate_nights(slot_value, dispatcher, "Bangkok")

    def validate_nights_Pattaya(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        return self._validate_nights(slot_value, dispatcher, "Pattaya")

    def validate_nights_Phuket(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        return self._validate_nights(slot_value, dispatcher, "Phuket")

    def validate_nights_Krabi(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        return self._validate_nights(slot_value, dispatcher, "Krabi")

    def _validate_nights(self, value: Any, dispatcher: CollectingDispatcher, city: Text) -> Dict[Text, Any]:
        try:
            nights = int(value)
            if 1 <= nights <= 10:
                return {f"nights_{city}": nights}
        except Exception:
            pass
        dispatcher.utter_message(text=f"Number of nights for {city} must be between 1 and 10")
        return {f"nights_{city}": None}
