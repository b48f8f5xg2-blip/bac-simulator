/**
 * Natural Language Parser for BAC Scenario Building
 * TypeScript port of conversational parsing functions
 */

import { DrinkType, FoodType } from './types';

// ============ Weight Parsing ============

/**
 * Extract weight in lbs from natural language
 * @example "180 lbs" -> 180
 * @example "82 kg" -> 180.81
 */
export function parseWeight(text: string): number | null {
  const patterns = [
    /(\d+(?:\.\d+)?)\s*(?:lbs?|pounds?)/i,
    /(?:weigh|weight)\s+(?:about\s+)?(\d+(?:\.\d+)?)/i,
    /(\d+(?:\.\d+)?)\s*(?:kg|kilos?)/i,
  ];

  for (const pattern of patterns) {
    const match = text.match(pattern);
    if (match) {
      let weight = parseFloat(match[1]);
      // Convert kg to lbs if needed
      if (/kg|kilo/i.test(pattern.source) || /kg|kilo/i.test(text)) {
        weight *= 2.205;
      }
      return Math.round(weight * 10) / 10;
    }
  }

  // Try plain number if no units
  const plainNumber = text.match(/^(\d+(?:\.\d+)?)$/);
  if (plainNumber) {
    const weight = parseFloat(plainNumber[1]);
    // Assume lbs if reasonable range
    if (weight >= 80 && weight <= 400) {
      return weight;
    }
    // Assume kg if smaller
    if (weight >= 35 && weight < 80) {
      return Math.round(weight * 2.205 * 10) / 10;
    }
  }

  return null;
}

// ============ Height Parsing ============

/**
 * Extract height in inches from natural language
 * @example "6'2" -> 74
 * @example "180 cm" -> 70.87
 */
export function parseHeight(text: string): number | null {
  // 6'2" or 6' 2" format
  const feetInchesMatch = text.match(/(\d+)\s*['′]\s*(\d+)?/);
  if (feetInchesMatch) {
    const feet = parseInt(feetInchesMatch[1], 10);
    const inches = feetInchesMatch[2] ? parseInt(feetInchesMatch[2], 10) : 0;
    return feet * 12 + inches;
  }

  // "6 feet 2 inches" or "6 ft 2 in"
  const feetWordsMatch = text.match(/(\d+)\s*(?:feet|ft)(?:\s+(\d+)\s*(?:in|inches?))?/i);
  if (feetWordsMatch) {
    const feet = parseInt(feetWordsMatch[1], 10);
    const inches = feetWordsMatch[2] ? parseInt(feetWordsMatch[2], 10) : 0;
    return feet * 12 + inches;
  }

  // "70 inches" or "70 in" (but not "X min ago")
  const inchesMatch = text.match(/(\d+)\s*(?:inches?|in)(?!\s*ago)/i);
  if (inchesMatch) {
    return parseInt(inchesMatch[1], 10);
  }

  // "180 cm"
  const cmMatch = text.match(/(\d+)\s*cm/i);
  if (cmMatch) {
    return Math.round(parseInt(cmMatch[1], 10) / 2.54 * 10) / 10;
  }

  return null;
}

// ============ Sex Parsing ============

/**
 * Extract biological sex from natural language
 */
export function parseSex(text: string): 'male' | 'female' | null {
  const textLower = text.toLowerCase();

  if (/\b(male|man|boy|guy|m)\b/.test(textLower)) {
    return 'male';
  }
  if (/\b(female|woman|girl|gal|f)\b/.test(textLower)) {
    return 'female';
  }

  return null;
}

// ============ Age Parsing ============

/**
 * Extract age from natural language
 * @example "I'm 25 years old" -> 25
 * @example "age is 30" -> 30
 */
export function parseAge(text: string): number | null {
  const patterns = [
    /(?:i'm\s+|i am\s+)?(\d+)\s+(?:years?\s+)?old/i,
    /age\s+(?:is\s+)?(\d+)/i,
    /^(\d+)$/,
  ];

  for (const pattern of patterns) {
    const match = text.match(pattern);
    if (match) {
      const age = parseInt(match[1], 10);
      if (age >= 18 && age <= 120) {
        return age;
      }
    }
  }

  return null;
}

// ============ Time Parsing ============

/**
 * Parse time references like 'now', '7pm', '2 hours ago', etc.
 */
export function parseTimePhrase(text: string): Date | null {
  const textLower = text.toLowerCase();
  const now = new Date();

  // Handle "now" or "just now"
  if (/\b(now|just now|right now)\b/.test(textLower)) {
    return now;
  }

  // Handle relative times like "X hours ago"
  const hoursAgoMatch = text.match(/(\d+)\s*(?:hours?|hrs?)\s*ago/i);
  if (hoursAgoMatch) {
    const hours = parseInt(hoursAgoMatch[1], 10);
    return new Date(now.getTime() - hours * 60 * 60 * 1000);
  }

  // Handle "X minutes ago"
  const minutesAgoMatch = text.match(/(\d+)\s*(?:minutes?|mins?)\s*ago/i);
  if (minutesAgoMatch) {
    const minutes = parseInt(minutesAgoMatch[1], 10);
    return new Date(now.getTime() - minutes * 60 * 1000);
  }

  // Handle time like "7pm", "7:30pm", "19:30"
  const timeMatch = text.match(/(\d{1,2}):?(\d{2})?\s*(am|pm)?/i);
  if (timeMatch) {
    let hour = parseInt(timeMatch[1], 10);
    const minute = timeMatch[2] ? parseInt(timeMatch[2], 10) : 0;
    const meridiem = timeMatch[3]?.toLowerCase();

    // Adjust for AM/PM
    if (meridiem === 'pm' && hour < 12) {
      hour += 12;
    } else if (meridiem === 'am' && hour === 12) {
      hour = 0;
    }

    const parsedTime = new Date(now);
    parsedTime.setHours(hour, minute, 0, 0);

    // If time is in future, assume it was yesterday
    if (parsedTime > now) {
      parsedTime.setDate(parsedTime.getDate() - 1);
    }

    return parsedTime;
  }

  return null;
}

// ============ Drink Parsing ============

interface ParsedDrink {
  type: DrinkType;
  quantity: number;
  alcoholPercent: number | null;
}

const DRINK_PATTERNS: Record<DrinkType, string[]> = {
  beer_light: ['light beer', 'lite beer', 'bud light', 'corona light', 'miller lite', 'coors light'],
  beer_regular: ['beer', 'regular beer', 'domestic beer', 'pbr', 'budweiser', 'heineken'],
  beer_ipa: ['ipa', 'india pale ale', 'craft beer'],
  beer_stout: ['stout', 'guinness', 'porter'],
  wine_light: ['white wine', 'chardonnay', 'pinot grigio', 'sauvignon blanc', 'rose', 'rosé'],
  wine_red: ['red wine', 'cabernet', 'merlot', 'pinot noir', 'shiraz'],
  wine_fortified: ['port', 'sherry', 'fortified wine', 'vermouth'],
  spirits: ['whiskey', 'whisky', 'vodka', 'rum', 'gin', 'tequila', 'bourbon', 'scotch', 'liquor', 'shot'],
  mixed_drink: ['cocktail', 'mixed drink', 'margarita', 'cosmopolitan', 'martini', 'mojito', 'daiquiri'],
};

/**
 * Parse drink information from natural language
 */
export function parseDrink(text: string): ParsedDrink | null {
  const textLower = text.toLowerCase();

  // Find drink type
  let detectedType: DrinkType | null = null;

  for (const [drinkType, terms] of Object.entries(DRINK_PATTERNS)) {
    for (const term of terms) {
      if (textLower.includes(term)) {
        detectedType = drinkType as DrinkType;
        break;
      }
    }
    if (detectedType) break;
  }

  // Default to beer if 'drink' mentioned but no specific type
  if (!detectedType && /\b(drink|drank|had|having)\b/i.test(textLower)) {
    // Check if wine is mentioned
    if (/\bwine\b/i.test(textLower)) {
      detectedType = 'wine_light';
    } else {
      detectedType = 'beer_regular';
    }
  }

  if (!detectedType) {
    return null;
  }

  // Extract quantity
  let quantity = 1;
  const qtyMatch = text.match(/(\d+)\s*(?:beers?|glasses?|shots?|drinks?|cocktails?)/i);
  if (qtyMatch) {
    quantity = parseInt(qtyMatch[1], 10);
  }

  // Also check for "a couple" or "a few"
  if (/\b(a couple|couple of)\b/i.test(textLower)) {
    quantity = 2;
  } else if (/\b(a few|few)\b/i.test(textLower)) {
    quantity = 3;
  }

  // Extract alcohol percent if specified
  let alcoholPercent: number | null = null;
  const alcMatch = text.match(/(\d+(?:\.\d+)?)\s*%/);
  if (alcMatch) {
    alcoholPercent = parseFloat(alcMatch[1]);
  }

  return {
    type: detectedType,
    quantity,
    alcoholPercent,
  };
}

// ============ Food Parsing ============

const FOOD_PATTERNS: Record<FoodType, string[]> = {
  empty_stomach: ['empty stomach', "haven't eaten", "didn't eat", 'no food', 'nothing', 'fasting'],
  water: ['water', 'juice', 'soda', 'clear liquid', 'coffee', 'tea'],
  light_snack: ['snack', 'crackers', 'toast', 'chips', 'nuts', 'candy', 'pretzels', 'popcorn'],
  light_meal: ['soup', 'salad', 'sandwich', 'light meal', 'wrap', 'yogurt'],
  moderate_meal: ['meal', 'dinner', 'lunch', 'breakfast', 'pasta', 'rice', 'chicken'],
  full_meal: ['full meal', 'big meal', 'large meal', 'buffet', 'feast'],
  high_fat_meal: ['pizza', 'burger', 'fries', 'fatty', 'greasy', 'fast food', 'high-fat', 'steak', 'bacon', 'wings'],
};

/**
 * Parse food type from natural language
 */
export function parseFood(text: string): FoodType | null {
  const textLower = text.toLowerCase();

  for (const [foodType, terms] of Object.entries(FOOD_PATTERNS)) {
    for (const term of terms) {
      if (textLower.includes(term)) {
        return foodType as FoodType;
      }
    }
  }

  // If mentions "ate" but we didn't match, default to light meal
  if (/\b(ate|eaten|had food|had a meal)\b/i.test(textLower)) {
    return 'light_meal';
  }

  return null;
}

// ============ Chronic Drinker Parsing ============

/**
 * Determine if user drinks regularly
 */
export function parseChronicDrinker(text: string): boolean | null {
  const textLower = text.toLowerCase();

  // Positive indicators
  if (/\b(yes|regularly|every day|daily|frequently|often|heavy drinker|most days|quite often)\b/i.test(textLower)) {
    return true;
  }

  // Negative indicators
  if (/\b(no|nope|rarely|never|first time|not really|occasionally|sometimes|not often)\b/i.test(textLower)) {
    return false;
  }

  return null;
}

// ============ Full Message Processing ============

export interface ParsedMessage {
  drinks: Array<{
    type: DrinkType;
    quantity: number;
    alcoholPercent: number | null;
    time: Date;
  }>;
  foods: Array<{
    type: FoodType;
    time: Date;
  }>;
  profileUpdates: {
    sex?: 'male' | 'female';
    weight?: number;
    height?: number;
    age?: number;
    chronicDrinker?: boolean;
  };
}

/**
 * Process a complete message and extract all relevant data
 */
export function parseMessage(text: string): ParsedMessage {
  const result: ParsedMessage = {
    drinks: [],
    foods: [],
    profileUpdates: {},
  };

  // Parse profile data
  const sex = parseSex(text);
  if (sex) result.profileUpdates.sex = sex;

  const weight = parseWeight(text);
  if (weight) result.profileUpdates.weight = weight;

  const height = parseHeight(text);
  if (height) result.profileUpdates.height = height;

  const age = parseAge(text);
  if (age) result.profileUpdates.age = age;

  const chronicDrinker = parseChronicDrinker(text);
  if (chronicDrinker !== null) result.profileUpdates.chronicDrinker = chronicDrinker;

  // Parse time (will be used for drinks/food)
  const time = parseTimePhrase(text) ?? new Date();

  // Parse drink
  const drink = parseDrink(text);
  if (drink) {
    result.drinks.push({
      ...drink,
      time,
    });
  }

  // Parse food
  const food = parseFood(text);
  if (food) {
    result.foods.push({
      type: food,
      time,
    });
  }

  return result;
}

// ============ Response Generation ============

/**
 * Generate a conversational response based on parsed input
 */
export function generateResponse(parsed: ParsedMessage): string {
  const parts: string[] = [];

  // Acknowledge drinks
  if (parsed.drinks.length > 0) {
    const drink = parsed.drinks[0];
    const drinkName = drink.type.replace(/_/g, ' ');
    const timeStr = formatTime(drink.time);
    if (drink.quantity > 1) {
      parts.push(`Got it! Added ${drink.quantity} ${drinkName}s at ${timeStr}.`);
    } else {
      parts.push(`Got it! Added ${drinkName} at ${timeStr}.`);
    }
  }

  // Acknowledge food
  if (parsed.foods.length > 0) {
    const food = parsed.foods[0];
    const foodName = food.type.replace(/_/g, ' ');
    const timeStr = formatTime(food.time);
    parts.push(`Noted ${foodName} at ${timeStr}. This affects alcohol absorption.`);
  }

  // If nothing was parsed
  if (parts.length === 0) {
    return "I didn't quite catch that. Try telling me about drinks (e.g., '2 beers at 7pm') or food (e.g., 'had pizza for dinner').";
  }

  return parts.join(' ');
}

/**
 * Format a Date to a readable time string
 */
function formatTime(date: Date): string {
  return date.toLocaleTimeString('en-US', {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true,
  });
}

// ============ Quick Action Helpers ============

export interface QuickAction {
  label: string;
  emoji: string;
  action: () => ParsedMessage;
}

/**
 * Get quick actions for common inputs
 */
export function getQuickActions(): QuickAction[] {
  const now = new Date();

  return [
    {
      label: 'Beer',
      emoji: '🍺',
      action: () => ({
        drinks: [{ type: 'beer_regular', quantity: 1, alcoholPercent: null, time: now }],
        foods: [],
        profileUpdates: {},
      }),
    },
    {
      label: 'Wine',
      emoji: '🍷',
      action: () => ({
        drinks: [{ type: 'wine_light', quantity: 1, alcoholPercent: null, time: now }],
        foods: [],
        profileUpdates: {},
      }),
    },
    {
      label: 'Shot',
      emoji: '🥃',
      action: () => ({
        drinks: [{ type: 'spirits', quantity: 1, alcoholPercent: null, time: now }],
        foods: [],
        profileUpdates: {},
      }),
    },
    {
      label: 'Food',
      emoji: '🍔',
      action: () => ({
        drinks: [],
        foods: [{ type: 'moderate_meal', time: now }],
        profileUpdates: {},
      }),
    },
  ];
}
