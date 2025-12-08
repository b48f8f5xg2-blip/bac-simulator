"""
Natural Language Chatbot for BAC Scenario Building
Conversational interface for collecting drinking/eating data
"""
import re
from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional, List

class BACChatbot:
    """Intelligent conversational bot for building BAC scenarios"""

    def __init__(self):
        self.state = 'initial'  # Tracks conversation state
        self.collected_data = {
            'sex': None,
            'weight': None,
            'age': None,
            'height': None,
            'start_time': None,
            'chronic_drinker': None
        }
        self.conversation_history = []
        self.pending_drinks = []  # Drinks to add to calculator
        self.pending_foods = []   # Foods to add to calculator

    def reset(self):
        """Reset chatbot state"""
        self.state = 'initial'
        self.collected_data = {
            'sex': None,
            'weight': None,
            'age': None,
            'height': None,
            'start_time': None,
            'chronic_drinker': None
        }
        self.conversation_history = []
        self.pending_drinks = []
        self.pending_foods = []

    def set_profile(self, sex: str = None, weight: float = None, age: int = None, 
                    height: float = None, chronic_drinker: bool = None, start_time: datetime = None):
        """Set profile data directly (for form-based input)"""
        if sex:
            self.collected_data['sex'] = sex.lower()
        if weight:
            self.collected_data['weight'] = weight
        if age:
            self.collected_data['age'] = age
        if height:
            self.collected_data['height'] = height
        if chronic_drinker is not None:
            self.collected_data['chronic_drinker'] = chronic_drinker
        if start_time:
            self.collected_data['start_time'] = start_time

    def parse_weight(self, text: str) -> Optional[float]:
        """Extract weight from natural language"""
        patterns = [
            r'(\d+)\s*(?:lbs?|pounds?)',
            r'(?:weigh|weight)\s+(?:about\s+)?(\d+)',
            r'(\d+)\s*(?:kg|kilos?)',
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                weight = float(match.group(1))
                if 'kg' in pattern or 'kilo' in text.lower():
                    weight *= 2.205  # Convert kg to lbs
                return weight
        return None

    def parse_height(self, text: str) -> Optional[float]:
        """Extract height in inches from natural language"""
        patterns = [
            (r"(\d+)\s*'\s*(\d+)?", 'feet'),           # 6'2" format
            (r"(\d+)\s+(?:feet|ft)(?:\s+(\d+)\s+(?:in|inches?))?", 'feet'),
            (r"(\d+)\s+(?:inches?|in)(?!\s*ago)", 'inches'),
            (r"(\d+)\s*cm", 'cm'),
        ]

        for pattern, unit in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if unit == 'feet':
                    feet = int(match.group(1))
                    inches = int(match.group(2)) if match.group(2) else 0
                    return feet * 12 + inches
                elif unit == 'inches':
                    return float(match.group(1))
                elif unit == 'cm':
                    return float(match.group(1)) / 2.54
        return None

    def parse_sex(self, text: str) -> Optional[str]:
        """Extract biological sex from natural language"""
        text_lower = text.lower()
        if any(word in text_lower for word in ['male', 'man', 'boy', 'm ', ' m']):
            return 'male'
        if any(word in text_lower for word in ['female', 'woman', 'girl', 'f ', ' f']):
            return 'female'
        return None

    def parse_age(self, text: str) -> Optional[int]:
        """Extract age from natural language"""
        patterns = [
            r"(?:i'm\s+|i am\s+)?(\d+)\s+(?:years?\s+)?old",
            r"age\s+(?:is\s+)?(\d+)",
            r"^(\d+)$",  # Just a number
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                age = int(match.group(1))
                if 18 <= age <= 120:  # Sanity check
                    return age
        return None

    def parse_time_phrase(self, text: str) -> Optional[datetime]:
        """Parse time references like 'now', '7pm', '2 hours ago', etc."""
        text_lower = text.lower()
        now = datetime.now()

        # Handle "now" or "just now"
        if any(word in text_lower for word in ['now', 'just now', 'right now']):
            return now

        # Handle relative times like "X hours ago", "X minutes ago"
        ago_match = re.search(r'(\d+)\s+(?:hours?|hrs?)\s+ago', text, re.IGNORECASE)
        if ago_match:
            hours = int(ago_match.group(1))
            return now - timedelta(hours=hours)

        ago_match = re.search(r'(\d+)\s+(?:minutes?|mins?)\s+ago', text, re.IGNORECASE)
        if ago_match:
            minutes = int(ago_match.group(1))
            return now - timedelta(minutes=minutes)

        # Handle time like "7pm", "7:30pm", "19:30"
        time_match = re.search(r'(\d{1,2}):?(\d{2})?\s*(?:am|pm)?|(\d{1,2})\s*(?:am|pm)', text, re.IGNORECASE)
        if time_match:
            try:
                if time_match.group(3):  # Format: "7pm"
                    hour = int(time_match.group(3))
                    is_pm = 'pm' in text.lower()
                    if is_pm and hour < 12:
                        hour += 12
                    minute = 0
                else:  # Format: "7:30pm" or "19:30"
                    hour = int(time_match.group(1))
                    minute = int(time_match.group(2)) if time_match.group(2) else 0

                parsed_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

                # If time is in future, assume it was earlier today or yesterday
                if parsed_time > now:
                    parsed_time = parsed_time - timedelta(days=1)

                return parsed_time
            except ValueError:
                pass

        return None

    def parse_drink(self, text: str) -> Tuple[Optional[str], Optional[int], Optional[float]]:
        """
        Parse drink information from natural language.
        Returns (drink_type, quantity, alcohol_percent)
        """
        text_lower = text.lower()

        # Check for common drink types
        drink_types = {
            'beer_light': ['light beer', 'lite beer', 'bud light', 'corona light'],
            'beer_regular': ['beer', 'regular beer', 'domestic beer', 'pbr'],
            'beer_ipa': ['ipa', 'ipa beer'],
            'beer_stout': ['stout', 'guinness'],
            'wine_light': ['white wine', 'wine'],
            'wine_red': ['red wine'],
            'spirits': ['whiskey', 'vodka', 'rum', 'gin', 'tequila', 'liquor', 'shot'],
            'mixed_drink': ['cocktail', 'mixed drink', 'margarita', 'cosmopolitan', 'martini'],
        }

        detected_type = None
        for drink_key, terms in drink_types.items():
            for term in terms:
                if term in text_lower:
                    detected_type = drink_key
                    break
            if detected_type:
                break

        # Extract quantity
        quantity = 1
        qty_match = re.search(r'(\d+)\s+(?:beers?|glasses?|shots?|drinks?)', text, re.IGNORECASE)
        if qty_match:
            quantity = int(qty_match.group(1))

        # Extract alcohol percent if specified
        alcohol_percent = None
        alc_match = re.search(r'(\d+(?:\.\d+)?)\s*%', text)
        if alc_match:
            alcohol_percent = float(alc_match.group(1))

        return detected_type, quantity, alcohol_percent

    def parse_food(self, text: str) -> Optional[str]:
        """Parse food type from natural language"""
        text_lower = text.lower()

        food_types = {
            'empty_stomach': ['empty stomach', "haven't eaten", "didn't eat", 'no food', 'nothing'],
            'water': ['water', 'juice', 'soda', 'clear liquid'],
            'light_snack': ['snack', 'crackers', 'toast', 'chips', 'nuts', 'candy'],
            'light_meal': ['soup', 'salad', 'sandwich', 'light meal'],
            'moderate_meal': ['meal', 'dinner', 'lunch', 'breakfast'],
            'full_meal': ['full meal', 'big meal', 'large meal'],
            'high_fat_meal': ['pizza', 'burger', 'fries', 'fatty', 'greasy', 'fast food', 'high-fat'],
        }

        for food_key, terms in food_types.items():
            for term in terms:
                if term in text_lower:
                    return food_key

        # If mentions "ate" but we didn't match, default to light meal
        if any(word in text_lower for word in ['ate', 'eaten', 'had', 'food']):
            return 'light_meal'

        return None

    def parse_chronic_drinker(self, text: str) -> Optional[bool]:
        """Determine if user is chronic drinker - FIXED TO INCLUDE YES/NO"""
        text_lower = text.lower()

        # FIXED: Added 'yes' to the True keywords
        if any(word in text_lower for word in ['yes', 'regularly', 'every day', 'daily', 'frequently', 'often', 'heavy drinker']):
            return True
        # FIXED: Added 'no' to the False keywords
        if any(word in text_lower for word in ['no', 'rarely', 'never', 'first time', 'not really', 'nope']):
            return False

        return None

    def process_message(self, user_message: str) -> str:
        """
        Process user message during profile collection phase.
        Parses input and updates collected_data based on what's currently being asked.
        """
        response = ""

        # Try to parse sex
        if self.collected_data['sex'] is None:
            sex = self.parse_sex(user_message)
            if sex:
                self.collected_data['sex'] = sex
                response = f"Got it, {sex}. "
            else:
                return "I didn't catch that. Please say 'male' or 'female'."

        # Try to parse weight
        elif self.collected_data['weight'] is None:
            weight = self.parse_weight(user_message)
            if weight:
                self.collected_data['weight'] = weight
                response = f"Got it, {weight:.0f} lbs. "
            else:
                return "I didn't understand. Please enter your weight (e.g., '180 lbs' or '82 kg')."

        # Try to parse height
        elif self.collected_data['height'] is None:
            height = self.parse_height(user_message)
            if height:
                self.collected_data['height'] = height
                feet = int(height // 12)
                inches = int(height % 12)
                response = f"Got it, {feet}'{inches}\". "
            else:
                return "I didn't understand. Please enter your height (e.g., '6 feet', '5'10\"', or '180 cm')."

        # Try to parse age
        elif self.collected_data['age'] is None:
            age = self.parse_age(user_message)
            if age:
                self.collected_data['age'] = age
                response = f"Got it, {age} years old. "
            else:
                return "I didn't catch that. Please enter your age as a number."

        # Try to parse chronic drinker status
        elif self.collected_data['chronic_drinker'] is None:
            chronic = self.parse_chronic_drinker(user_message)
            if chronic is not None:
                self.collected_data['chronic_drinker'] = chronic
                status = "regularly" if chronic else "occasionally"
                response = f"Got it, you drink {status}. "
            else:
                return "I didn't understand. Do you drink regularly (yes) or rarely (no)?"

        # Try to parse start time
        elif self.collected_data['start_time'] is None:
            start_time = self.parse_time_phrase(user_message)
            if start_time:
                self.collected_data['start_time'] = start_time
                response = f"Got it, started at {start_time.strftime('%I:%M %p')}. "
            else:
                return "I didn't understand. When did you start drinking? (e.g., '7pm', '2 hours ago', 'now')"

        # Profile complete
        if self.is_profile_complete():
            response += "Profile complete! Now tell me about your drinks and food."

        return response

    def process_scenario_update(self, user_message: str) -> str:
        """Process updates to drinking/food scenario and extract data"""
        text_lower = user_message.lower()
        
        self.pending_drinks = []  # Reset pending drinks for this message
        self.pending_foods = []   # Reset pending foods for this message

        # Check for drink mentions
        if any(word in text_lower for word in ['beer', 'wine', 'shot', 'cocktail', 'drink', 'alcohol', 'had', 'drank']):
            drink_type, quantity, alc_percent = self.parse_drink(user_message)
            if drink_type:
                # Extract time from message
                drink_time = self.parse_time_phrase(user_message)
                if not drink_time:
                    # If no time specified, use current time
                    drink_time = datetime.now()
                
                # Store pending drink data for GUI to process
                self.pending_drinks.append({
                    'type': drink_type,
                    'quantity': quantity or 1,
                    'alcohol_percent': alc_percent,
                    'time': drink_time
                })
                
                response = f"Got it! I recorded {quantity or 1} {drink_type.replace('_', ' ')}(s) at {drink_time.strftime('%I:%M %p')}. "
            else:
                response = "I didn't catch the drink type. Try 'beer', 'wine', 'shot', or 'cocktail'. "

        # Check for food mentions
        if any(word in text_lower for word in ['ate', 'eaten', 'food', 'meal', 'lunch', 'dinner', 'breakfast', 'pizza', 'burger', 'salad']):
            food_type = self.parse_food(user_message)
            if food_type:
                # Extract time from message
                food_time = self.parse_time_phrase(user_message)
                if not food_time:
                    food_time = datetime.now()
                
                self.pending_foods.append({
                    'type': food_type,
                    'time': food_time
                })
                
                response = f"Noted - you had {food_type.replace('_', ' ')} at {food_time.strftime('%I:%M %p')}. This affects absorption significantly. "
            else:
                response = "I didn't catch the food type clearly. "
        
        if not self.pending_drinks and not self.pending_foods:
            response = "Got it. I'm tracking your scenario. You can tell me about more drinks or food anytime!"
        else:
            response += "Want to add more drinks or food?"
        
        return response

    def get_pending_drinks(self) -> List[Dict]:
        """Get drinks to be added to calculator"""
        drinks = self.pending_drinks.copy()
        self.pending_drinks = []
        return drinks

    def get_pending_foods(self) -> List[Dict]:
        """Get foods to be added to calculator"""
        foods = self.pending_foods.copy()
        self.pending_foods = []
        return foods

    def get_collected_data(self) -> Dict:
        """Return collected profile and scenario data"""
        return self.collected_data.copy()

    def is_profile_complete(self) -> bool:
        """Check if minimum profile data is collected"""
        required = ['sex', 'weight', 'age', 'chronic_drinker', 'start_time']
        return all(self.collected_data.get(field) is not None for field in required)

    def get_next_question(self) -> str:
        """Generate next chatbot question based on collected data (for terminal UI compatibility)"""
        if self.collected_data['sex'] is None:
            return "Welcome to the BAC Simulator! I'll help you understand alcohol metabolism. Let's start with your biological sex (male or female):"

        if self.collected_data['weight'] is None:
            return "What's your weight? (e.g., '180 lbs' or '82 kg')"

        if self.collected_data['height'] is None:
            return "What's your height? (e.g., '6 feet', '5\\'10\"', or '180 cm')"

        if self.collected_data['age'] is None:
            return "How old are you?"

        if self.collected_data['chronic_drinker'] is None:
            return "Do you drink regularly/frequently? (e.g., 'yes, most days' or 'no, rarely')"

        if self.collected_data['start_time'] is None:
            return "When did you start drinking today? (e.g., '7pm', '2 hours ago', or 'now')"

        return "Tell me about your drinks and food. You can say things like: 'I had 2 beers at 7pm, then another at 8pm' or 'I ate pizza at 6pm'"
