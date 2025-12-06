================================================================================
BAC SIMULATOR - Blood Alcohol Content Calculator
Educational Tool for Understanding Alcohol Metabolism
================================================================================

DESCRIPTION:
The BAC Simulator is a professional, scientifically-accurate desktop application
for understanding how the human body processes alcohol. It uses the modified
Widmark equation and accounts for food consumption, metabolic variations, and
individual factors to provide realistic BAC (Blood Alcohol Content) calculations.

SYSTEM REQUIREMENTS:
- macOS 10.13 or later
- Python 3.9+ (typically pre-installed on modern macOS)
- No additional software required (fully self-contained)

INSTALLATION:
1. Download the BAC_Simulator.app folder
2. Place it on your Desktop or in Applications folder
3. Double-click to launch

USAGE:
1. Launch the application by double-clicking BAC_Simulator.app
2. Follow the conversational chatbot to enter your profile:
   - Biological sex (male/female)
   - Body weight
   - Height
   - Age
   - Drinking frequency
   - Drinking start time

3. Tell the chatbot about your drinks and food:
   - Examples: "I had 2 beers at 7pm" or "I ate pizza at 6pm"
   - The app will parse natural language and track everything

4. View real-time BAC calculations:
   - Current BAC level with color-coded status
   - Impairment assessment
   - Timeline showing BAC over next 6 hours
   - Legal status and fitness to drive
   - Detailed breakdown of drinks, food, and metabolism

FEATURES:
- Widmark Equation: BAC = [(A × 5.14) / (W × r)] - (0.015 × H)
- Food Absorption Modeling: Accounts for food type and gastric emptying
- Metabolic Variations: Gender, age, chronic drinking status, medications
- Real-time Calculation: Updates as you add drinks
- Timeline Visualization: See BAC curve over time
- Legal Threshold Display: Shows DUI risk (0.08% federal limit, 0.15% Tennessee enhanced)
- Impairment Levels: From sober to life-threatening
- Natural Language Input: Conversational interface for ease of use

SCIENTIFIC BASIS:
This simulator uses peer-reviewed research on:
- Modified Widmark equation for BAC calculation
- Gastric emptying and food absorption rates
- Individual metabolic variation (gender, age, body composition)
- Linear alcohol elimination (0.015%/hour on average)
- Tennessee DUI laws (2024 enhanced DUI threshold at 0.15%)

IMPORTANT DISCLAIMER:
⚠️  THIS SIMULATOR PROVIDES EDUCATIONAL ESTIMATES ONLY.
⚠️  DO NOT USE TO DETERMINE FITNESS TO DRIVE OR LEGAL DECISIONS.
⚠️  ACTUAL BAC VARIES SIGNIFICANTLY BY INDIVIDUAL FACTORS.
⚠️  WHEN IN DOUBT, DO NOT DRIVE. CALL A TAXI, RIDESHARE, OR DESIGNATED DRIVER.

This tool is for educational purposes only. It should never be used as a basis
for legal decisions or driving safety decisions. Actual BAC is affected by many
factors not captured in this simulator, including individual enzyme variation,
medication interactions, food composition, and other metabolic factors.

BAC CATEGORIES:
- 0.00-0.02%: Sober / No impairment
- 0.02-0.05%: Minimal impairment / Slight warmth
- 0.05-0.08%: Mild impairment / Reduced concentration (legal to drive)
- 0.08-0.15%: Moderate impairment / DUI threshold (illegal to drive)
- 0.15-0.20%: Severe impairment / Enhanced DUI in Tennessee
- 0.20%+: Very severe impairment / Medical risk / Possible poisoning
- 0.40%+: Life-threatening / Risk of coma/death

TROUBLESHOOTING:

Q: The app won't open
A: Try double-clicking again, or right-click and select "Open"

Q: "Python not found" error
A: macOS requires Python 3.9+. Install from python.org or use Homebrew:
   brew install python3

Q: Can't type in the chatbox
A: Click in the text input field at the bottom of the chatbox before typing

Q: Numbers look weird/cut off
A: The app requires a minimum window size. Try resizing the window larger.

CONTACT & SUPPORT:
For technical issues with the application, report problems with the app
structure or Python environment.

For scientific questions about BAC calculations, consult peer-reviewed
literature on alcohol metabolism and forensic toxicology.

================================================================================
Version: 1.0
Last Updated: November 2024
Educational Use Only - Not for Medical or Legal Decisions
================================================================================
