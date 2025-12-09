# BAC Simulator - API & Interface Reference

**Version**: 1.0
**Date**: December 9, 2025
**Purpose**: Complete reference for all public interfaces, types, and functions

---

## TypeScript API Reference (Web App)

### Core Types (`lib/types.ts`)

#### UserProfile
```typescript
interface UserProfile {
  sex: 'male' | 'female';
  weightLbs: number;
  heightInches: number;
  age: number;
  chronicDrinker: boolean;
}
```

**Example**:
```typescript
const profile: UserProfile = {
  sex: 'male',
  weightLbs: 180,
  heightInches: 72,
  age: 28,
  chronicDrinker: false
};
```

#### Drink
```typescript
interface Drink {
  id: string;
  time: Date;
  type: DrinkType;
  sizeOz: number;
  alcoholPercent: number;
}

type DrinkType =
  | 'beer_light'      // 12 oz, 4.2%
  | 'beer_regular'    // 12 oz, 5.0%
  | 'beer_ipa'        // 12 oz, 6.5%
  | 'beer_stout'      // 12 oz, 7.0%
  | 'wine_light'      // 5 oz, 11.0%
  | 'wine_red'        // 5 oz, 13.5%
  | 'wine_fortified'  // 3 oz, 20.0%
  | 'spirits'         // 1.5 oz, 40.0%
  | 'mixed_drink';    // 1.5 oz, 40.0%
```

**Example**:
```typescript
const drink: Drink = {
  id: 'drink_001',
  time: new Date('2025-12-09T20:30:00'),
  type: 'beer_regular',
  sizeOz: 12,
  alcoholPercent: 5.0
};
```

#### Food
```typescript
interface Food {
  id: string;
  time: Date;
  type: FoodType;
}

type FoodType =
  | 'empty_stomach'   // 0 min delay, 0% reduction
  | 'water'           // 15 min delay, 5% reduction
  | 'light_snack'     // 60 min delay, 20% reduction
  | 'light_meal'      // 90 min delay, 30% reduction
  | 'moderate_meal'   // 120 min delay, 40% reduction
  | 'full_meal'       // 150 min delay, 45% reduction
  | 'high_fat_meal';  // 180 min delay, 60% reduction
```

**Example**:
```typescript
const food: Food = {
  id: 'food_001',
  time: new Date('2025-12-09T20:00:00'),
  type: 'full_meal'
};
```

#### BACResult
```typescript
interface BACResult {
  bac: number;                      // Current BAC percentage (0.0-0.4)
  impairmentLevel: ImpairmentLevel;
  timestamp: Date;
}

interface ImpairmentLevel {
  threshold: number;                // BAC threshold for this level
  level: string;                    // "Sober", "Mild Impairment", etc.
  description: string;              // Clinical description
  color: BACStatusColor;            // UI color: 'safe'|'caution'|etc.
  fitnessToDriver: 'YES'|'CAUTION'|'NO';
  legalStatus: string;              // "LEGAL", "DUI", "ENHANCED DUI", etc.
}

type BACStatusColor = 'safe' | 'caution' | 'warning' | 'danger' | 'critical';
```

**Example**:
```typescript
const result: BACResult = {
  bac: 0.065,
  impairmentLevel: {
    threshold: 0.05,
    level: 'Mild Impairment',
    description: 'Reduced concentration, slower reaction time',
    color: 'caution',
    fitnessToDriver: 'CAUTION',
    legalStatus: 'LEGAL'
  },
  timestamp: new Date()
};
```

#### TimelinePoint
```typescript
interface TimelinePoint {
  time: Date;
  bac: number;  // BAC at this time (0-6 hours from first drink)
}

interface BACPeak {
  bac: number;
  time: Date;
}
```

**Example**:
```typescript
const timeline: TimelinePoint[] = [
  { time: new Date('2025-12-09T20:30:00'), bac: 0.0 },
  { time: new Date('2025-12-09T20:35:00'), bac: 0.04 },
  { time: new Date('2025-12-09T20:40:00'), bac: 0.06 },
  // ... continues for 6 hours
];
```

### Constants (`lib/types.ts`)

#### Standard Drinks
```typescript
export const STANDARD_DRINKS: Record<DrinkType, StandardDrink> = {
  beer_light: { oz: 12, alcoholPercent: 4.2 },
  beer_regular: { oz: 12, alcoholPercent: 5.0 },
  beer_ipa: { oz: 12, alcoholPercent: 6.5 },
  beer_stout: { oz: 12, alcoholPercent: 7.0 },
  wine_light: { oz: 5, alcoholPercent: 11.0 },
  wine_red: { oz: 5, alcoholPercent: 13.5 },
  wine_fortified: { oz: 3, alcoholPercent: 20.0 },
  spirits: { oz: 1.5, alcoholPercent: 40.0 },
  mixed_drink: { oz: 1.5, alcoholPercent: 40.0 },
};
```

#### Widmark Ratios
```typescript
export const WIDMARK_RATIOS = {
  male: 0.73,
  female: 0.66,
} as const;
```

#### Food Gastric Times (minutes)
```typescript
export const FOOD_GASTRIC_TIMES: Record<FoodType, number> = {
  empty_stomach: 0,
  water: 15,
  light_snack: 60,
  light_meal: 90,
  moderate_meal: 120,
  full_meal: 150,
  high_fat_meal: 180,
};
```

#### Food Absorption Impact (fraction of peak reduction)
```typescript
export const FOOD_ABSORPTION_IMPACT: Record<FoodType, number> = {
  empty_stomach: 0,     // No reduction
  water: 0.05,          // 5% reduction
  light_snack: 0.20,    // 20% reduction
  light_meal: 0.30,     // 30% reduction
  moderate_meal: 0.40,  // 40% reduction
  full_meal: 0.45,      // 45% reduction
  high_fat_meal: 0.60,  // 60% reduction
};
```

#### Impairment Levels
```typescript
export const IMPAIRMENT_LEVELS: ImpairmentLevel[] = [
  {
    threshold: 0.0,
    level: 'Sober',
    description: 'No detectable impairment',
    color: 'safe',
    fitnessToDriver: 'YES',
    legalStatus: 'LEGAL',
  },
  {
    threshold: 0.02,
    level: 'Minimal Impairment',
    description: 'Slight warmth, mild euphoria',
    color: 'safe',
    fitnessToDriver: 'YES',
    legalStatus: 'LEGAL',
  },
  {
    threshold: 0.05,
    level: 'Mild Impairment',
    description: 'Reduced concentration, slower reaction time',
    color: 'caution',
    fitnessToDriver: 'CAUTION',
    legalStatus: 'LEGAL',
  },
  {
    threshold: 0.08,
    level: 'Moderate Impairment',
    description: 'Legal limit reached - DUI threshold',
    color: 'warning',
    fitnessToDriver: 'NO',
    legalStatus: 'ILLEGAL - DUI',
  },
  {
    threshold: 0.15,
    level: 'Severe Impairment',
    description: 'Enhanced DUI threshold (7+ day jail)',
    color: 'danger',
    fitnessToDriver: 'NO',
    legalStatus: 'ILLEGAL - ENHANCED DUI',
  },
  {
    threshold: 0.20,
    level: 'Very Severe Impairment',
    description: 'Major loss of motor control, danger of poisoning',
    color: 'danger',
    fitnessToDriver: 'NO',
    legalStatus: 'DANGEROUS - MEDICAL RISK',
  },
  {
    threshold: 0.30,
    level: 'Extreme Intoxication',
    description: 'Risk of death, medical emergency',
    color: 'critical',
    fitnessToDriver: 'NO',
    legalStatus: 'LIFE-THREATENING',
  },
];
```

### Calculation Functions (`lib/bac-calculator.ts`)

#### calculateBAC
```typescript
export function calculateBAC(
  drinks: Drink[],
  profile: UserProfile,
  currentTime: Date
): number {
  // Returns: Current BAC percentage
  // Formula: Peak BAC - (0.015 × hours elapsed)
  // Where Peak = (A × 5.14) / (W × r) × (1 - food_factor)
}

// Example usage
const drinks: Drink[] = [
  { id: '1', time: new Date('2025-12-09T20:30:00'),
    type: 'beer_regular', sizeOz: 12, alcoholPercent: 5.0 }
];
const profile: UserProfile = {
  sex: 'male',
  weightLbs: 180,
  heightInches: 72,
  age: 28,
  chronicDrinker: false
};
const currentTime = new Date('2025-12-09T21:30:00');

const bac = calculateBAC(drinks, profile, currentTime);
// Returns: approximately 0.04
```

#### calculateTimeline
```typescript
export function calculateTimeline(
  drinks: Drink[],
  food: Food[],
  profile: UserProfile,
  startTime: Date,
  hours: number = 6
): TimelinePoint[] {
  // Returns: Array of time points with BAC values
  // Default: 6 hours forward from startTime
  // Interval: Every 5 minutes (60 points for 5 hours)
}

// Example usage
const timeline = calculateTimeline(
  drinks,
  [{ id: '1', time: new Date('2025-12-09T20:00:00'), type: 'full_meal' }],
  profile,
  new Date('2025-12-09T20:30:00'),
  6
);
// Returns: 72 TimelinePoint objects spanning 6 hours
```

#### calculatePeakBAC
```typescript
export function calculatePeakBAC(
  drinks: Drink[],
  food: Food[],
  profile: UserProfile
): BACPeak {
  // Returns: { bac: number, time: Date }
  // Accounts for food absorption delays
  // Finds the maximum BAC and when it occurs
}

// Example usage
const peak = calculatePeakBAC(drinks, [food], profile);
// Returns: { bac: 0.065, time: Date }
```

#### getImpairmentLevel
```typescript
export function getImpairmentLevel(bac: number): ImpairmentLevel {
  // Returns: Appropriate impairment level for given BAC
  // Matches against IMPAIRMENT_LEVELS thresholds
  // Returns highest threshold ≤ bac
}

// Example usage
const level = getImpairmentLevel(0.065);
// Returns: {
//   threshold: 0.05,
//   level: 'Mild Impairment',
//   color: 'caution',
//   ...
// }
```

### Hook API (`hooks/useBACCalculator.ts`)

#### useBACCalculator
```typescript
interface UseBACCalculatorReturn {
  profile: UserProfile;
  setProfile: (profile: UserProfile) => void;
  drinks: Drink[];
  addDrink: (type: DrinkType, time?: Date) => void;
  removeDrink: (id: string) => void;
  food: Food[];
  addFood: (type: FoodType, time?: Date) => void;
  removeFood: (id: string) => void;
  currentBAC: number;
  timeline: TimelinePoint[];
  peakBAC: BACPeak;
  impairmentLevel: ImpairmentLevel;
  reset: () => void;
}

export function useBACCalculator(): UseBACCalculatorReturn {
  // Main calculation hook - manages all state
  // Updates BAC every 2 seconds
  // Recalculates timeline on any change
}

// Example usage in component
const {
  profile,
  setProfile,
  drinks,
  addDrink,
  currentBAC,
  timeline,
  impairmentLevel,
  reset
} = useBACCalculator();

return (
  <div>
    <BACDisplay bac={currentBAC} impairment={impairmentLevel} />
    <TimelineChart timeline={timeline} />
  </div>
);
```

### Chatbot Parser API (`lib/chatbot-parser.ts`)

#### parseDrinkMessage
```typescript
export function parseDrinkMessage(message: string): {
  found: boolean;
  type?: DrinkType;
  quantity?: number;
  confidence: number;
} {
  // Recognizes drink types in natural language
  // Examples: "two beers", "glass of wine", "shot of whiskey"
  // Returns: Matched drink type and quantity
}

// Example usage
const result = parseDrinkMessage("I had a beer");
// Returns: { found: true, type: 'beer_regular', quantity: 1, confidence: 0.95 }
```

#### parseFoodMessage
```typescript
export function parseFoodMessage(message: string): {
  found: boolean;
  type?: FoodType;
  confidence: number;
} {
  // Recognizes food types in natural language
  // Examples: "light meal", "full dinner", "just water"
  // Returns: Matched food type
}

// Example usage
const result = parseFoodMessage("I ate a full meal");
// Returns: { found: true, type: 'full_meal', confidence: 0.92 }
```

#### parseProfileMessage
```typescript
export function parseProfileMessage(message: string): {
  sex?: 'male' | 'female';
  weight?: number;
  height?: number;
  age?: number;
} {
  // Extracts profile information from natural language
  // Examples: "I'm a 180 pound male", "5'10\" female"
  // Returns: Extracted profile fields
}

// Example usage
const result = parseProfileMessage("I'm a 180 pound 6 foot tall male, 28 years old");
// Returns: { sex: 'male', weight: 180, height: 72, age: 28 }
```

---

## Python API Reference (Desktop App)

### BACCalculator Class (`bac_calculator.py`)

#### Constructor
```python
class BACCalculator:
    def __init__(self, profile: dict):
        self.profile = profile  # {'sex': 'male'|'female', 'weight_lbs': int, ...}
        self.drinks = []
        self.food = []
        self.start_time = None
```

#### Core Methods

```python
def add_drink(self, drink_type: str, time: datetime) -> None:
    """Add a drink to the consumption list"""
    # drink_type: 'beer_light', 'beer_regular', 'wine_red', 'spirits', etc.
    # time: datetime when drink was consumed

def add_food(self, food_type: str, time: datetime) -> None:
    """Add food to the consumption list"""
    # food_type: 'empty_stomach', 'light_meal', 'full_meal', etc.
    # time: datetime when food was consumed

def calculate_bac(self, hours_elapsed: float) -> float:
    """Calculate current BAC given hours elapsed"""
    # Returns: BAC as decimal (0.0 to 0.4)
    # Formula: Peak BAC - (0.015 × hours_elapsed)

def calculate_peak_bac(self) -> dict:
    """Calculate peak BAC and when it occurs"""
    # Returns: {'bac': float, 'hours': float, 'time': datetime}

def calculate_timeline(self, hours: int = 6) -> list:
    """Generate 6-hour BAC projection"""
    # Returns: List of {'time': datetime, 'bac': float}
    # Interval: Every 5 minutes

def get_impairment_level(self, bac: float) -> dict:
    """Get impairment classification for BAC"""
    # Returns: {
    #   'level': str,
    #   'description': str,
    #   'color': str,
    #   'fitness_to_drive': str,
    #   'legal_status': str
    # }

def reset(self) -> None:
    """Clear all drinks and food, reset calculator"""
```

#### Example Usage
```python
profile = {
    'sex': 'male',
    'weight_lbs': 180,
    'height_inches': 72,
    'age': 28,
    'chronic_drinker': False
}

calc = BACCalculator(profile)

# Add drinks
calc.add_drink('beer_regular', datetime.now())
calc.add_drink('beer_regular', datetime.now() + timedelta(minutes=30))

# Add food
calc.add_food('full_meal', datetime.now() - timedelta(minutes=30))

# Calculate current BAC
bac = calc.calculate_bac(hours_elapsed=1.0)
print(f"Current BAC: {bac:.3f}%")

# Get peak
peak = calc.calculate_peak_bac()
print(f"Peak BAC: {peak['bac']:.3f}% at {peak['hours']:.1f} hours")

# Get timeline
timeline = calc.calculate_timeline(hours=6)
for point in timeline[:6]:  # First 30 minutes
    print(f"{point['time']}: {point['bac']:.3f}%")

# Get impairment
level = calc.get_impairment_level(bac)
print(f"Status: {level['level']}")
print(f"Fitness to drive: {level['fitness_to_drive']}")
```

### Chatbot Class (`chatbot.py`)

```python
class Chatbot:
    def process_message(self, message: str) -> dict:
        """Process user message and extract information"""
        # Returns: {
        #   'drinks': [{'type': str, 'quantity': int}],
        #   'food': [{'type': str}],
        #   'profile_updates': {...},
        #   'response': str,  # Conversational response
        #   'action': str     # 'add_drink'|'add_food'|'update_profile'|etc.
        # }

    def parse_drink(self, message: str) -> dict:
        """Extract drink information"""
        # Returns: {'type': str, 'quantity': int, 'confidence': float}

    def parse_food(self, message: str) -> dict:
        """Extract food information"""
        # Returns: {'type': str, 'confidence': float}

    def parse_profile(self, message: str) -> dict:
        """Extract profile updates"""
        # Returns: {'sex': str, 'weight': int, 'height': int, 'age': int}
```

#### Example Usage
```python
chatbot = Chatbot()

response = chatbot.process_message("I just had two beers")
print(response['action'])  # 'add_drink'
print(response['drinks'])  # [{'type': 'beer_regular', 'quantity': 2}]

response = chatbot.process_message("I ate a big dinner")
print(response['action'])  # 'add_food'
print(response['food'])    # [{'type': 'full_meal'}]
```

### GUI Class (`gui.py`)

#### Main Methods
```python
class BACSimulatorGUI:
    def __init__(self, root, calculator, chatbot):
        """Initialize GUI with calculator and chatbot"""

    def setup_ui(self) -> None:
        """Create main UI layout (3 columns)"""

    def update_display(self) -> None:
        """Update all UI elements with current data"""
        # Called every 2 seconds

    def add_drink_to_list(self, drink_type: str) -> None:
        """Add drink and update display"""

    def add_food_to_list(self, food_type: str) -> None:
        """Add food and update display"""

    def reset_scenario(self) -> None:
        """Clear all drinks/food, reset profile"""

    def send_chat_message(self, message: str) -> None:
        """Process chat input through chatbot"""
```

#### Example of Extending GUI
```python
# To add a new drink button in gui.py:
btn = tk.Button(
    button_frame,
    text="IPA",
    command=lambda: self.add_drink_to_list('beer_ipa'),
    bg=self.colors['primary'],
    fg=self.colors['white'],
    font=self.fonts['body_small']
)
btn.pack(side=tk.LEFT, padx=5)
```

---

## Design System Constants

### Colors (Both Platforms)

```python
# Python (gui.py)
colors = {
    'primary': '#00BFAE',
    'primary_dark': '#004040',
    'neutral': '#BFBEBE',
    'accent': '#029922',
    'slate': '#4A4A63',
    'bac_safe': '#029922',
    'bac_caution': '#F59E0B',
    'bac_warning': '#F97316',
    'bac_danger': '#EF4444',
    'bac_critical': '#991B1B',
}
```

```typescript
// TypeScript (tailwind.config.ts)
colors: {
  primary: '#00BFAE',
  secondary: '#004040',
  neutral: '#BFBEBE',
  accent: '#029922',
  slate: '#4A4A63',
  bac: {
    safe: '#029922',
    caution: '#F59E0B',
    warning: '#F97316',
    danger: '#EF4444',
    critical: '#991B1B',
  }
}
```

### Algorithm Constants

```python
# Python
WIDMARK_RATIOS = {'male': 0.73, 'female': 0.66}
ELIMINATION_RATE = 0.015  # %/hour
DUI_THRESHOLD = 0.08
ENHANCED_DUI_THRESHOLD = 0.15

FOOD_GASTRIC_TIMES = {
    'empty_stomach': 0,
    'water': 15,
    'light_snack': 60,
    'light_meal': 90,
    'moderate_meal': 120,
    'full_meal': 150,
    'high_fat_meal': 180,
}

FOOD_ABSORPTION_IMPACT = {
    'empty_stomach': 0.0,
    'water': 0.05,
    'light_snack': 0.20,
    'light_meal': 0.30,
    'moderate_meal': 0.40,
    'full_meal': 0.45,
    'high_fat_meal': 0.60,
}
```

```typescript
// TypeScript (same values in lib/types.ts)
export const WIDMARK_RATIOS = {
  male: 0.73,
  female: 0.66,
} as const;

const ELIMINATION_RATE = 0.015;
const DUI_THRESHOLD = 0.08;
const ENHANCED_DUI_THRESHOLD = 0.15;
```

---

## Usage Patterns & Examples

### Pattern 1: Calculate BAC for a Scenario

**TypeScript (Web)**:
```typescript
import { calculateBAC, getImpairmentLevel } from '@/lib/bac-calculator';

const profile: UserProfile = {
  sex: 'male',
  weightLbs: 180,
  heightInches: 72,
  age: 28,
  chronicDrinker: false
};

const drinks: Drink[] = [
  {
    id: '1',
    time: new Date('2025-12-09T20:30:00'),
    type: 'beer_regular',
    sizeOz: 12,
    alcoholPercent: 5.0
  }
];

const currentTime = new Date('2025-12-09T21:00:00');
const bac = calculateBAC(drinks, profile, currentTime);
const level = getImpairmentLevel(bac);

console.log(`BAC: ${bac.toFixed(3)}%`);
console.log(`Status: ${level.level}`);
console.log(`Safe to drive: ${level.fitnessToDriver === 'YES' ? 'Yes' : 'No'}`);
```

**Python (Desktop)**:
```python
from bac_calculator import BACCalculator
from datetime import datetime, timedelta

profile = {
    'sex': 'male',
    'weight_lbs': 180,
    'height_inches': 72,
    'age': 28,
    'chronic_drinker': False
}

calc = BACCalculator(profile)
calc.add_drink('beer_regular', datetime.now() - timedelta(minutes=30))

bac = calc.calculate_bac(hours_elapsed=0.5)
level = calc.get_impairment_level(bac)

print(f"BAC: {bac:.3f}%")
print(f"Status: {level['level']}")
print(f"Safe to drive: {'Yes' if level['fitness_to_drive'] == 'YES' else 'No'}")
```

### Pattern 2: Generate Timeline for Display

**TypeScript (Web)**:
```typescript
const timeline = calculateTimeline(drinks, food, profile, startTime, 6);

// Use in chart component
<TimelineChart
  timeline={timeline}
  currentBAC={currentBAC}
  peak={peakBAC}
/>
```

**Python (Desktop)**:
```python
timeline = calc.calculate_timeline(hours=6)

# Draw on canvas
for point in timeline:
    # Convert to pixel coordinates
    x = point['hours'] * pixels_per_hour
    y = height - (point['bac'] * pixels_per_unit)
    canvas.create_oval(x-2, y-2, x+2, y+2, fill='teal')
```

### Pattern 3: Process User Input

**TypeScript (Web)**:
```typescript
const handleChatMessage = (message: string) => {
  const drinkResult = parseDrinkMessage(message);
  if (drinkResult.found) {
    const drinkType = drinkResult.type as DrinkType;
    addDrink(drinkType, new Date());
  }

  const foodResult = parseFoodMessage(message);
  if (foodResult.found) {
    const foodType = foodResult.type as FoodType;
    addFood(foodType, new Date());
  }
};
```

**Python (Desktop)**:
```python
message = chat_input.get()
result = chatbot.process_message(message)

if result['action'] == 'add_drink':
    for drink in result['drinks']:
        calc.add_drink(drink['type'], datetime.now())

if result['action'] == 'add_food':
    for food in result['food']:
        calc.add_food(food['type'], datetime.now())

gui.update_display()
```

---

## Error Handling

### TypeScript Error Cases

```typescript
// Invalid BAC (should never occur with valid inputs)
if (bac < 0) {
  return 0; // Cannot have negative BAC
}

if (bac > 0.5) {
  // Medical emergency warning
  return criticalImpairmentLevel;
}

// Invalid profile
if (profile.weightLbs < 50 || profile.weightLbs > 500) {
  throw new Error('Invalid weight');
}

if (profile.heightInches < 36 || profile.heightInches > 108) {
  throw new Error('Invalid height');
}
```

### Python Error Cases

```python
# Validation in BACCalculator
if self.profile['weight_lbs'] < 50:
    raise ValueError("Weight must be at least 50 lbs")

if bac < 0:
    return 0

if bac > 0.5:
    # Critical state
    return self.impairment_levels[-1]  # Extreme intoxication
```

---

## Performance Considerations

### Update Rate: 2 Seconds

Both platforms recalculate every 2 seconds:
- Smooth visual updates
- Reasonable CPU usage
- Responsive to user input

### Avoid These in Calculations

1. **Floating-point comparisons**: Use thresholds (e.g., `bac > 0.075` not `bac == 0.08`)
2. **Unnecessary recalculations**: Cache results when possible
3. **Excessive timeline points**: 72 points (5-minute intervals) is sufficient

### Optimize These if Needed

1. **Memoization**: Cache timeline calculation if inputs haven't changed
2. **Lazy rendering**: Only update visible elements
3. **Batch updates**: Update all UI at once, not incrementally

---

## Testing Checklist

Before deploying changes, verify with these test cases:

```
Test Case 1: Empty Stomach, 2 Beers
- Profile: 180 lb male
- Input: 2 beers at t=0
- Expected Peak: ~0.105%
- Expected Time to Sober: ~7 hours

Test Case 2: Full Meal + 1 Drink
- Profile: 140 lb female
- Food: Full meal at t=-30 min
- Input: 1 beer at t=0
- Expected Peak: ~0.03% (45% reduction)
- Expected Peak Time: ~1.5 hours (delayed)

Test Case 3: DUI Threshold
- Profile: 160 lb
- Input: 3 beers over 1 hour
- Expected: Cross 0.08% threshold
- Verify: Color changes to warning

Test Case 4: Timeline Accuracy
- Verify: 6-hour projection
- Verify: Elimination rate correct
- Verify: Peak timing accurate
- Verify: Color transitions at thresholds
```

---

## Version History

| Version | Date       | Changes |
|---------|-----------|---------|
| 1.0     | Dec 9, 2025 | Initial API reference |

---

**This reference document is machine-readable and should be kept in sync with actual implementation changes.**
