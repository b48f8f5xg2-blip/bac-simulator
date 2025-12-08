"""
BAC Calculation Engine - Widmark Equation with Food Absorption Model
Scientifically accurate blood alcohol content simulator
"""
import math
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

class BACCalculator:
    """
    Core BAC calculation engine using modified Widmark equation:
    BAC = [(A × 5.14) / (W × r)] - (0.015 × H)
    """

    # Widmark distribution ratios
    WIDMARK_RATIOS = {
        'male': 0.73,
        'female': 0.66
    }

    # Elimination rate: % BAC per hour (15 mg/100mL per hour = ~0.015%)
    ELIMINATION_RATE = 0.015  # %/hour

    # Food gastric emptying times (minutes) - half-life of stomach content
    FOOD_GASTRIC_TIMES = {
        'empty_stomach': 0,
        'water': 15,
        'light_snack': 60,
        'light_meal': 90,
        'moderate_meal': 120,
        'full_meal': 150,
        'high_fat_meal': 180
    }

    # Food absorption impact (% reduction in peak BAC)
    FOOD_ABSORPTION_IMPACT = {
        'empty_stomach': 0,      # 0% reduction
        'water': 0.05,           # 5% reduction
        'light_snack': 0.20,     # 20% reduction
        'light_meal': 0.30,      # 30% reduction
        'moderate_meal': 0.40,   # 40% reduction
        'full_meal': 0.45,       # 45% reduction
        'high_fat_meal': 0.60    # 60% reduction
    }

    # Standard drink sizes and alcohol content
    STANDARD_DRINKS = {
        'beer_light': {'oz': 12, 'alcohol_percent': 4.2},
        'beer_regular': {'oz': 12, 'alcohol_percent': 5.0},
        'beer_ipa': {'oz': 12, 'alcohol_percent': 6.5},
        'beer_stout': {'oz': 12, 'alcohol_percent': 7.0},
        'wine_light': {'oz': 5, 'alcohol_percent': 11.0},
        'wine_red': {'oz': 5, 'alcohol_percent': 13.5},
        'wine_fortified': {'oz': 3, 'alcohol_percent': 20.0},
        'spirits': {'oz': 1.5, 'alcohol_percent': 40.0},
        'mixed_drink': {'oz': 1.5, 'alcohol_percent': 40.0},
    }

    def __init__(self):
        self.drinks_timeline = []  # List of {time, drink_type, size_oz, alcohol_percent}
        self.food_timeline = []    # List of {time, food_type}
        self.profile = {
            'sex': 'male',
            'weight_lbs': 180,
            'height_inches': 70,
            'age': 30,
            'chronic_drinker': False,
            'medications': []
        }
        self.start_time = datetime.now()

    def set_profile(self, sex: str, weight_lbs: float, age: int = 30,
                   chronic_drinker: bool = False):
        """Set user profile for BAC calculations"""
        self.profile = {
            'sex': sex.lower(),
            'weight_lbs': float(weight_lbs),
            'age': int(age),
            'chronic_drinker': chronic_drinker,
            'medications': []
        }

    def add_food(self, time: datetime, food_type: str):
        """Add food consumed to timeline"""
        food_type = food_type.lower()
        if food_type not in self.FOOD_GASTRIC_TIMES:
            food_type = 'light_meal'  # Default
        self.food_timeline.append({'time': time, 'type': food_type})
        self.food_timeline.sort(key=lambda x: x['time'])

    def add_drink(self, time: datetime, drink_type: str, size_oz: float = None,
                 alcohol_percent: float = None, quantity: int = 1):
        """Add drink(s) consumed to timeline"""
        drink_type_lower = drink_type.lower()

        if drink_type_lower in self.STANDARD_DRINKS:
            std_drink = self.STANDARD_DRINKS[drink_type_lower]
            size_oz = size_oz or std_drink['oz']
            alcohol_percent = alcohol_percent or std_drink['alcohol_percent']
        else:
            size_oz = size_oz or 12
            alcohol_percent = alcohol_percent or 5.0

        for i in range(quantity):
            drink_time = time + timedelta(minutes=i*30)  # Spread drinks 30 min apart
            self.drinks_timeline.append({
                'time': drink_time,
                'type': drink_type,
                'size_oz': float(size_oz),
                'alcohol_percent': float(alcohol_percent)
            })

        self.drinks_timeline.sort(key=lambda x: x['time'])

    def get_most_recent_food(self, reference_time: datetime) -> Tuple[str, float]:
        """
        Get the most recent food before the reference time and minutes elapsed.
        Returns (food_type, minutes_since_eaten)
        """
        recent_foods = [f for f in self.food_timeline if f['time'] <= reference_time]

        if not recent_foods:
            return 'empty_stomach', float('inf')

        latest_food = recent_foods[-1]
        minutes_elapsed = (reference_time - latest_food['time']).total_seconds() / 60
        return latest_food['type'], minutes_elapsed

    def calculate_absorption_factor(self, drink_time: datetime, target_time: datetime = None) -> float:
        """
        Calculate absorption factor (0-1, where 1 = fully absorbed) for a drink.
        Based on food state at drink time and time elapsed since drinking.

        Args:
            drink_time: When the drink was consumed
            target_time: Time at which to calculate absorption (default: now)
        """
        if target_time is None:
            target_time = datetime.now()

        # Time elapsed since drink was consumed (in minutes)
        minutes_since_drink = max(0, (target_time - drink_time).total_seconds() / 60)

        # Get food state at time of drink
        food_type, minutes_since_food = self.get_most_recent_food(drink_time)
        gastric_half_time = self.FOOD_GASTRIC_TIMES.get(food_type, 90)

        if gastric_half_time == 0:  # Empty stomach
            # Fast absorption: ~80% in 30 min, ~95% in 60 min
            # Ensure minimum 10% immediate absorption
            absorption = 0.10 + 0.90 * (1.0 - math.exp(-minutes_since_drink / 20))
            return min(1.0, absorption)
        else:
            # Food delays absorption
            # Calculate effective delay based on how full stomach was
            delay_factor = min(1.0, minutes_since_food / gastric_half_time)

            # Adjust absorption rate based on food
            # Full stomach: slower absorption, takes ~90-120 min to absorb fully
            # As stomach empties, absorption speeds up
            effective_absorption_time = minutes_since_drink * (0.5 + 0.5 * delay_factor)

            # Ensure minimum 10% immediate absorption even with food
            absorption = 0.10 + 0.90 * (1.0 - math.exp(-effective_absorption_time / 30))
            return min(1.0, absorption)

    def calculate_bac_at_time(self, target_time: datetime = None) -> float:
        """
        Calculate BAC at a specific time using Widmark equation with food absorption.
        BAC = [(A × 5.14) / (W × r)] - (0.015 × H)
        """
        if target_time is None:
            target_time = datetime.now()

        if target_time < self.start_time:
            return 0.0

        # Get Widmark parameters
        widmark_ratio = self.WIDMARK_RATIOS.get(self.profile['sex'], 0.73)
        body_weight = self.profile['weight_lbs']

        # Account for metabolism variation
        elimination_rate = self.ELIMINATION_RATE
        if self.profile['chronic_drinker']:
            elimination_rate *= 1.2  # 20% faster for chronic drinkers

        # Calculate absorption for each drink
        total_alcohol_absorbed = 0.0

        for drink in self.drinks_timeline:
            if drink['time'] <= target_time:
                # Alcohol in this drink (liquid ounces)
                alcohol_oz = drink['size_oz'] * (drink['alcohol_percent'] / 100)

                # Absorption factor accounts for food effects and time elapsed
                absorption_factor = self.calculate_absorption_factor(drink['time'], target_time)

                # Food reduces peak BAC (applied separately from absorption timing)
                food_type, _ = self.get_most_recent_food(drink['time'])
                peak_reduction = self.FOOD_ABSORPTION_IMPACT.get(food_type, 0.0)

                # Effective alcohol = actual alcohol * how much absorbed * food peak reduction
                # Note: absorption_factor handles WHEN alcohol is absorbed
                # peak_reduction handles HOW MUCH of the peak is reduced
                effective_alcohol_oz = alcohol_oz * absorption_factor * (1 - peak_reduction * 0.5)

                # Add to total
                total_alcohol_absorbed += effective_alcohol_oz

        # Widmark equation: BAC = [(A × 5.14) / (W × r)] - (0.015 × H)
        if total_alcohol_absorbed > 0:
            bac_from_absorption = (total_alcohol_absorbed * 5.14) / (body_weight * widmark_ratio)
        else:
            bac_from_absorption = 0.0

        # Time since first drink
        time_since_first = (target_time - self.start_time).total_seconds() / 3600
        elimination = elimination_rate * max(0, time_since_first)

        bac = max(0.0, bac_from_absorption - elimination)
        return round(bac, 4)

    def get_bac_timeline(self, hours: int = 6, from_now: bool = True) -> List[Tuple[datetime, float]]:
        """
        Generate BAC values for timeline visualization.

        Args:
            hours: Number of hours to project
            from_now: If True, start from current time (future projection).
                      If False, start from drinking start time (full history).
        """
        timeline = []

        if from_now:
            # Future projection from current time
            start = datetime.now()
        else:
            # Full history from when drinking started
            start = self.start_time

        end_time = start + timedelta(hours=hours)

        # Sample every 5 minutes
        current_time = start
        while current_time <= end_time:
            bac = self.calculate_bac_at_time(current_time)
            timeline.append((current_time, bac))
            current_time += timedelta(minutes=5)

        return timeline

    def get_peak_bac(self) -> Tuple[float, datetime]:
        """Find peak BAC and when it occurs"""
        timeline = self.get_bac_timeline(hours=6)
        peak_bac = 0.0
        peak_time = self.start_time

        for time, bac in timeline:
            if bac > peak_bac:
                peak_bac = bac
                peak_time = time

        return peak_bac, peak_time

    def get_time_to_sobriety(self, threshold: float = 0.0) -> timedelta:
        """Calculate time until BAC drops below threshold"""
        timeline = self.get_bac_timeline(hours=24)

        for time, bac in timeline:
            if bac <= threshold:
                return time - self.start_time

        return timedelta(hours=24)

    def get_time_to_legal_limit(self) -> timedelta:
        """Calculate time until BAC reaches 0.08% (legal limit)"""
        timeline = self.get_bac_timeline(hours=6)

        for time, bac in timeline:
            if bac >= 0.08:
                return time - self.start_time

        return None

    def get_impairment_level(self, bac: float = None) -> Dict:
        """Get impairment description and legal status for BAC level"""
        if bac is None:
            bac = self.calculate_bac_at_time()

        impairment_levels = [
            {
                'threshold': 0.0,
                'level': 'Sober',
                'description': 'No detectable impairment',
                'color': 'green',
                'fitness_to_drive': 'YES',
                'legal_status': 'LEGAL'
            },
            {
                'threshold': 0.02,
                'level': 'Minimal Impairment',
                'description': 'Slight warmth, mild euphoria, minimal coordination loss',
                'color': 'lightgreen',
                'fitness_to_drive': 'YES',
                'legal_status': 'LEGAL'
            },
            {
                'threshold': 0.05,
                'level': 'Mild Impairment',
                'description': 'Reduced concentration, slower reaction time, slight loss of coordination',
                'color': 'yellow',
                'fitness_to_drive': 'CAUTION',
                'legal_status': 'LEGAL'
            },
            {
                'threshold': 0.08,
                'level': 'Moderate Impairment',
                'description': 'Legal limit reached - DUI threshold for standard drivers',
                'color': 'orange',
                'fitness_to_drive': 'NO',
                'legal_status': 'ILLEGAL - DUI'
            },
            {
                'threshold': 0.15,
                'level': 'Severe Impairment',
                'description': 'Enhanced DUI threshold in Tennessee (7+ day jail for first offense)',
                'color': 'darkorange',
                'fitness_to_drive': 'NO',
                'legal_status': 'ILLEGAL - ENHANCED DUI'
            },
            {
                'threshold': 0.20,
                'level': 'Very Severe Impairment',
                'description': 'Major loss of motor control, risk of blackouts, danger of poisoning',
                'color': 'red',
                'fitness_to_drive': 'NO',
                'legal_status': 'DANGEROUS - MEDICAL RISK'
            },
            {
                'threshold': 0.30,
                'level': 'Extreme Intoxication',
                'description': 'Severe loss of consciousness, risk of death, medical emergency',
                'color': 'darkred',
                'fitness_to_drive': 'NO',
                'legal_status': 'LIFE-THREATENING'
            }
        ]

        # Find appropriate level
        for level in reversed(impairment_levels):
            if bac >= level['threshold']:
                return level

        return impairment_levels[0]

    def clear_scenario(self):
        """Reset all data for new scenario"""
        self.drinks_timeline = []
        self.food_timeline = []
        self.start_time = datetime.now()
