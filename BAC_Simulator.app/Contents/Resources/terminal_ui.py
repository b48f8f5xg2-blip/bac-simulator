"""
BAC Simulator - Terminal-Based Interactive Interface
Works on any Python without Tkinter dependency
Perfect for Rosetta/Apple Silicon compatibility issues
"""
import os
import sys
import time
from datetime import datetime, timedelta
from typing import Optional

class TerminalUI:
    """Text-based interactive interface for BAC Simulator"""

    def __init__(self, calculator, chatbot):
        self.calculator = calculator
        self.chatbot = chatbot
        self.width = 80
        self.drinks_added = False
        self.foods_added = False

    def print_header(self):
        """Print application header"""
        print("\n" + "=" * self.width)
        print("BAC SIMULATOR - Blood Alcohol Content Calculator".center(self.width))
        print("Educational Tool for Understanding Alcohol Metabolism".center(self.width))
        print("=" * self.width)
        print()

    def print_footer(self):
        """Print disclaimer footer"""
        print("\n" + "-" * self.width)
        print("⚠️  EDUCATIONAL USE ONLY - Do not use for legal/medical decisions")
        print("When in doubt about driving, call a taxi/Uber/Lyft. Do NOT drive.")
        print("-" * self.width + "\n")

    def print_divider(self):
        """Print visual divider"""
        print("-" * self.width)

    def print_bac_display(self):
        """Print current BAC with formatting"""
        current_bac = self.calculator.calculate_bac_at_time()
        impairment = self.calculator.get_impairment_level(current_bac)

        # Status color codes (text representation)
        status_colors = {
            'green': '✅',
            'lightgreen': '🟢',
            'yellow': '🟡',
            'orange': '🟠',
            'darkorange': '🟠',
            'red': '🔴',
            'darkred': '⛔',
        }
        color_symbol = status_colors.get(impairment['color'], '⚪')

        print()
        print(f"{color_symbol} CURRENT BAC: {current_bac:.4f}%")
        print(f"  Status: {impairment['level']}")
        print(f"  Description: {impairment['description']}")
        print(f"  FITNESS TO DRIVE: {impairment['fitness_to_drive']}")
        print(f"  LEGAL STATUS: {impairment['legal_status']}")
        print()

    def print_timeline_summary(self):
        """Print timeline information"""
        self.print_divider()
        print("TIMELINE & PROJECTIONS:")
        self.print_divider()

        peak_bac, peak_time = self.calculator.get_peak_bac()
        time_to_sober = self.calculator.get_time_to_sobriety()
        current_bac = self.calculator.calculate_bac_at_time()

        elapsed_since_start = (datetime.now() - self.calculator.start_time).total_seconds() / 3600

        print(f"\n  Peak BAC: {peak_bac:.4f}% at {peak_time.strftime('%I:%M %p')}")
        print(f"  Time until sober: {self._format_timedelta(time_to_sober)}")
        print(f"  Hours elapsed since start: {elapsed_since_start:.1f} hours")

        # Legal limit information
        if current_bac >= 0.15:
            print(f"\n  ⚠️  CRITICAL: You are at ENHANCED DUI level (0.15%+)")
            print(f"     Tennessee enhanced DUI penalty: 7+ days jail")
        elif current_bac >= 0.08:
            print(f"\n  ⚠️  WARNING: You are at DUI level (0.08%+)")
            print(f"     Illegal to drive in all US states")
        elif current_bac > 0.00:
            print(f"\n  ✓ Below legal limit (0.08%) but impaired")
            print(f"  ✓ Sober in approximately {self._format_timedelta(time_to_sober)}")

        print()

    def print_drinks_and_food(self):
        """Print consumed drinks and food"""
        if not self.calculator.drinks_timeline and not self.calculator.food_timeline:
            return

        self.print_divider()
        print("CONSUMPTION HISTORY:")
        self.print_divider()

        # Food timeline
        if self.calculator.food_timeline:
            print("\n🍽️  FOOD CONSUMED:")
            for food in self.calculator.food_timeline:
                time_str = food['time'].strftime('%I:%M %p')
                food_name = food['type'].replace('_', ' ').title()
                print(f"     • {time_str} - {food_name}")

        # Drinks timeline
        if self.calculator.drinks_timeline:
            print("\n🍺 DRINKS CONSUMED:")
            for i, drink in enumerate(self.calculator.drinks_timeline, 1):
                time_str = drink['time'].strftime('%I:%M %p')
                drink_name = drink['type'].replace('_', ' ').title()
                alcohol_content = drink['size_oz'] * drink['alcohol_percent'] / 100
                print(f"     {i}. {time_str} - {drink['size_oz']:.0f}oz {drink_name} ({drink['alcohol_percent']:.1f}%) [{alcohol_content:.2f}oz alcohol]")

        print()

    def _format_timedelta(self, td: timedelta) -> str:
        """Format timedelta as readable string"""
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        if hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"

    def print_profile(self):
        """Print user profile"""
        data = self.chatbot.get_collected_data()
        if not all([data['sex'], data['weight'], data['age']]):
            return

        self.print_divider()
        print("YOUR PROFILE:")
        self.print_divider()
        print(f"  Sex: {data['sex'].title()}")
        print(f"  Weight: {data['weight']:.0f} lbs")
        if data['height']:
            feet = int(data['height'] // 12)
            inches = int(data['height'] % 12)
            print(f"  Height: {feet}'{inches}\"")
        print(f"  Age: {data['age']} years")
        drinks_freq = "Regular drinker" if data['chronic_drinker'] else "Occasional drinker"
        print(f"  Drinking Frequency: {drinks_freq}")
        if data['start_time']:
            print(f"  Drinking started: {data['start_time'].strftime('%I:%M %p')}")
        print()

    def run_chatbot_loop(self):
        """Run interactive chatbot loop"""
        print("\n" + "=" * self.width)
        print("Let's build your BAC scenario through conversation".center(self.width))
        print("=" * self.width + "\n")

        # Chatbot conversation loop
        while not self.chatbot.is_profile_complete():
            # Get and display bot question
            question = self.chatbot.get_next_question()
            print(f"\n🤖 Bot: {question}")

            # Get user input
            user_input = input("You: ").strip()
            if not user_input:
                continue

            # Process message
            response = self.chatbot.process_message(user_input)
            print(f"🤖 Bot: {response}")

            # Small delay for readability
            time.sleep(0.5)

        # Update calculator with profile data
        self._update_calculator_from_chatbot()

        # Now allow free-form drink/food entry
        print("\n" + "=" * self.width)
        print("Scenario Builder - Log Your Drinks & Food".center(self.width))
        print("=" * self.width)
        print("\nExamples:")
        print("  • I had a beer at 7pm")
        print("  • I drank 2 beers, 12 oz each")
        print("  • I ate pizza at 6pm")
        print("  • I just had another drink")
        print("\nType 'done' when finished, 'show' to see current BAC, or 'help' for more options.\n")

        while True:
            user_input = input("You: ").strip().lower()

            if not user_input:
                continue

            if user_input == 'done':
                break

            if user_input == 'help':
                self._print_help()
                continue

            if user_input == 'show':
                self.print_bac_display()
                self.print_timeline_summary()
                self.print_drinks_and_food()
                continue

            if user_input == 'profile':
                self.print_profile()
                continue

            if user_input == 'clear':
                self.calculator.clear_scenario()
                print("\n✓ Scenario cleared. Starting over...\n")
                continue

            # Process drink/food input
            user_input_original = user_input

            # Check for drinks
            drink_type, quantity, alc_percent = self.chatbot.parse_drink(user_input)
            if drink_type:
                time_phrase = self.chatbot.parse_time_phrase(user_input)
                drink_time = time_phrase if time_phrase else datetime.now()

                self.calculator.add_drink(drink_time, drink_type, quantity=quantity or 1,
                                        alcohol_percent=alc_percent)
                print(f"✓ Added {quantity or 1} {drink_type.replace('_', ' ')}(s) at {drink_time.strftime('%I:%M %p')}")
                self.drinks_added = True
                continue

            # Check for food
            food_type = self.chatbot.parse_food(user_input)
            if food_type:
                time_phrase = self.chatbot.parse_time_phrase(user_input)
                food_time = time_phrase if time_phrase else datetime.now()

                self.calculator.add_food(food_time, food_type)
                print(f"✓ Added {food_type.replace('_', ' ')} at {food_time.strftime('%I:%M %p')}")
                self.foods_added = True
                continue

            # If nothing matched
            print("I didn't understand. Try: 'I had a beer' or 'I ate pizza at 6pm'")

    def _update_calculator_from_chatbot(self):
        """Update calculator with chatbot profile data"""
        data = self.chatbot.get_collected_data()
        if data['sex'] and data['weight'] and data['age']:
            self.calculator.set_profile(
                sex=data['sex'],
                weight_lbs=data['weight'],
                age=data['age'],
                chronic_drinker=data['chronic_drinker'] or False
            )
            if data['start_time']:
                self.calculator.start_time = data['start_time']

    def _print_help(self):
        """Print help information"""
        print("""
COMMANDS:
  done      - Finish entering drinks/food and show results
  show      - Display current BAC and timeline
  profile   - Show your user profile
  clear     - Reset scenario and start over
  help      - Show this help message

DRINK EXAMPLES:
  I had a beer at 7pm
  2 beers, 12 oz each
  I drank whiskey (40%)
  Cocktail at 8pm
  Just had another beer

FOOD EXAMPLES:
  Pizza at 6pm
  Light meal at noon
  I ate a burger
  Had soup earlier

FOOD TYPES (by absorption delay):
  • empty stomach     (no delay)
  • water/clear liquid (minimal delay)
  • light snack       (60 min delay)
  • light meal        (90 min delay)
  • moderate meal     (120 min delay)
  • full meal         (150 min delay)
  • high-fat meal     (180 min delay)
""")

    def show_final_results(self):
        """Display final BAC calculations and results"""
        print("\n" + "=" * self.width)
        print("FINAL BAC CALCULATION RESULTS".center(self.width))
        print("=" * self.width)

        self.print_bac_display()
        self.print_profile()
        self.print_drinks_and_food()
        self.print_timeline_summary()
        self._print_calculation_details()
        self.print_footer()

    def _print_calculation_details(self):
        """Print detailed calculation breakdown"""
        self.print_divider()
        print("CALCULATION DETAILS (Widmark Equation):")
        self.print_divider()

        profile = self.calculator.profile
        widmark_ratio = self.calculator.WIDMARK_RATIOS.get(profile['sex'], 0.73)

        print(f"\nWIDMARK FORMULA: BAC = [(A × 5.14) / (W × r)] - (0.015 × H)")
        print(f"\nVariables:")
        print(f"  A (Alcohol consumed): {len(self.calculator.drinks_timeline)} drinks")
        print(f"  W (Body weight): {profile['weight_lbs']:.0f} lbs")
        print(f"  r (Distribution ratio): {widmark_ratio} ({profile['sex']})")
        print(f"  H (Hours elapsed): ~{(datetime.now() - self.calculator.start_time).total_seconds() / 3600:.1f} hours")
        print(f"  Elimination rate: 0.015% per hour")

        # Calculate total alcohol
        total_alcohol_oz = sum(
            d['size_oz'] * (d['alcohol_percent'] / 100)
            for d in self.calculator.drinks_timeline
        )
        print(f"\nTotal alcohol consumed: {total_alcohol_oz:.2f} liquid ounces")

        # Food impact
        if self.calculator.food_timeline:
            print(f"\nFood impact on absorption:")
            for food in self.calculator.food_timeline:
                impact = self.calculator.FOOD_ABSORPTION_IMPACT.get(food['type'], 0.3)
                peak_reduction = impact * 100
                print(f"  • {food['type'].replace('_', ' ').title()}: {peak_reduction:.0f}% peak BAC reduction")

        print()

    def run(self):
        """Main application loop"""
        try:
            self.print_header()

            # Run chatbot conversation
            self.run_chatbot_loop()

            # Show results
            if self.drinks_added or self.foods_added:
                self.show_final_results()
            else:
                print("\nNo drinks or food added. Showing profile and calculator ready.")
                self.print_profile()
                print("Ready to add drinks and food. Run again and enter your consumption data.")
                self.print_footer()

        except KeyboardInterrupt:
            print("\n\n✓ BAC Simulator closed. Goodbye!")
            self.print_footer()
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            self.print_footer()
            sys.exit(1)
