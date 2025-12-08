// User Profile Types
export interface UserProfile {
  sex: 'male' | 'female';
  weightLbs: number;
  heightInches: number;
  age: number;
  chronicDrinker: boolean;
}

// Drink and Food Types
export interface Drink {
  id: string;
  time: Date;
  type: DrinkType;
  sizeOz: number;
  alcoholPercent: number;
}

export interface Food {
  id: string;
  time: Date;
  type: FoodType;
}

export type DrinkType =
  | 'beer_light'
  | 'beer_regular'
  | 'beer_ipa'
  | 'beer_stout'
  | 'wine_light'
  | 'wine_red'
  | 'wine_fortified'
  | 'spirits'
  | 'mixed_drink';

export type FoodType =
  | 'empty_stomach'
  | 'water'
  | 'light_snack'
  | 'light_meal'
  | 'moderate_meal'
  | 'full_meal'
  | 'high_fat_meal';

// BAC Calculation Types
export interface BACResult {
  bac: number;
  impairmentLevel: ImpairmentLevel;
  timestamp: Date;
}

export interface ImpairmentLevel {
  threshold: number;
  level: string;
  description: string;
  color: BACStatusColor;
  fitnessToDriver: 'YES' | 'CAUTION' | 'NO';
  legalStatus: string;
}

export type BACStatusColor = 'safe' | 'caution' | 'warning' | 'danger' | 'critical';

export interface TimelinePoint {
  time: Date;
  bac: number;
}

export interface BACPeak {
  bac: number;
  time: Date;
}

// Standard Drink Definitions
export interface StandardDrink {
  oz: number;
  alcoholPercent: number;
}

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

// Food Gastric Emptying Times (minutes)
export const FOOD_GASTRIC_TIMES: Record<FoodType, number> = {
  empty_stomach: 0,
  water: 15,
  light_snack: 60,
  light_meal: 90,
  moderate_meal: 120,
  full_meal: 150,
  high_fat_meal: 180,
};

// Food Absorption Impact (% reduction in peak BAC)
export const FOOD_ABSORPTION_IMPACT: Record<FoodType, number> = {
  empty_stomach: 0,
  water: 0.05,
  light_snack: 0.20,
  light_meal: 0.30,
  moderate_meal: 0.40,
  full_meal: 0.45,
  high_fat_meal: 0.60,
};

// Widmark Distribution Ratios
export const WIDMARK_RATIOS = {
  male: 0.73,
  female: 0.66,
} as const;

// Impairment Levels
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

// Drink display names
export const DRINK_DISPLAY_NAMES: Record<DrinkType, string> = {
  beer_light: 'Light Beer',
  beer_regular: 'Beer',
  beer_ipa: 'IPA',
  beer_stout: 'Stout',
  wine_light: 'White Wine',
  wine_red: 'Red Wine',
  wine_fortified: 'Fortified Wine',
  spirits: 'Shot/Spirit',
  mixed_drink: 'Mixed Drink',
};

// Food display names
export const FOOD_DISPLAY_NAMES: Record<FoodType, string> = {
  empty_stomach: 'Empty Stomach',
  water: 'Water/Clear Liquid',
  light_snack: 'Light Snack',
  light_meal: 'Light Meal',
  moderate_meal: 'Moderate Meal',
  full_meal: 'Full Meal',
  high_fat_meal: 'High-Fat Meal',
};
