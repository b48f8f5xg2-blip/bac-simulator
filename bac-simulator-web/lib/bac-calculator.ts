/**
 * BAC Calculation Engine - Widmark Equation with Food Absorption Model
 * TypeScript port of scientifically accurate blood alcohol content simulator
 *
 * BAC Formula: BAC = [(A × 5.14) / (W × r)] - (0.015 × H)
 * Where: A = alcohol consumed (oz), W = weight (lbs), r = Widmark ratio, H = hours
 */

import {
  UserProfile,
  Drink,
  Food,
  DrinkType,
  FoodType,
  BACResult,
  ImpairmentLevel,
  TimelinePoint,
  BACPeak,
  STANDARD_DRINKS,
  FOOD_GASTRIC_TIMES,
  FOOD_ABSORPTION_IMPACT,
  WIDMARK_RATIOS,
  IMPAIRMENT_LEVELS,
} from './types';

// Elimination rate: % BAC per hour (15 mg/100mL per hour ≈ 0.015%)
const ELIMINATION_RATE = 0.015;

export class BACCalculator {
  private drinks: Drink[] = [];
  private foods: Food[] = [];
  private profile: UserProfile;
  private startTime: Date;

  constructor(profile?: Partial<UserProfile>) {
    this.profile = {
      sex: 'male',
      weightLbs: 180,
      heightInches: 70,
      age: 30,
      chronicDrinker: false,
      ...profile,
    };
    this.startTime = new Date();
  }

  /**
   * Set user profile for BAC calculations
   */
  setProfile(profile: Partial<UserProfile>): void {
    this.profile = { ...this.profile, ...profile };
  }

  /**
   * Get current profile
   */
  getProfile(): UserProfile {
    return { ...this.profile };
  }

  /**
   * Add food consumed to timeline
   */
  addFood(time: Date, type: FoodType): string {
    const id = `food_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    this.foods.push({ id, time, type });
    this.foods.sort((a, b) => a.time.getTime() - b.time.getTime());
    return id;
  }

  /**
   * Add drink(s) consumed to timeline
   */
  addDrink(
    time: Date,
    type: DrinkType,
    sizeOz?: number,
    alcoholPercent?: number,
    quantity: number = 1
  ): string[] {
    const stdDrink = STANDARD_DRINKS[type];
    const finalSizeOz = sizeOz ?? stdDrink.oz;
    const finalAlcoholPercent = alcoholPercent ?? stdDrink.alcoholPercent;
    const ids: string[] = [];

    for (let i = 0; i < quantity; i++) {
      // Spread multiple drinks 30 minutes apart
      const drinkTime = new Date(time.getTime() + i * 30 * 60 * 1000);
      const id = `drink_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

      this.drinks.push({
        id,
        time: drinkTime,
        type,
        sizeOz: finalSizeOz,
        alcoholPercent: finalAlcoholPercent,
      });
      ids.push(id);
    }

    this.drinks.sort((a, b) => a.time.getTime() - b.time.getTime());

    // Update start time if this is earlier
    if (this.drinks.length > 0) {
      const earliestDrink = this.drinks[0].time;
      if (earliestDrink < this.startTime) {
        this.startTime = earliestDrink;
      }
    }

    return ids;
  }

  /**
   * Remove a drink by ID
   */
  removeDrink(id: string): boolean {
    const index = this.drinks.findIndex(d => d.id === id);
    if (index !== -1) {
      this.drinks.splice(index, 1);
      return true;
    }
    return false;
  }

  /**
   * Remove food by ID
   */
  removeFood(id: string): boolean {
    const index = this.foods.findIndex(f => f.id === id);
    if (index !== -1) {
      this.foods.splice(index, 1);
      return true;
    }
    return false;
  }

  /**
   * Get all drinks
   */
  getDrinks(): Drink[] {
    return [...this.drinks];
  }

  /**
   * Get all foods
   */
  getFoods(): Food[] {
    return [...this.foods];
  }

  /**
   * Get the most recent food before the reference time
   * @returns [foodType, minutesSinceEaten]
   */
  private getMostRecentFood(referenceTime: Date): [FoodType, number] {
    const recentFoods = this.foods.filter(f => f.time <= referenceTime);

    if (recentFoods.length === 0) {
      return ['empty_stomach', Infinity];
    }

    const latestFood = recentFoods[recentFoods.length - 1];
    const minutesElapsed = (referenceTime.getTime() - latestFood.time.getTime()) / (60 * 1000);
    return [latestFood.type, minutesElapsed];
  }

  /**
   * Calculate absorption factor (0-1, where 1 = fully absorbed) for a drink.
   * Based on food state at drink time and time elapsed since drinking.
   */
  private calculateAbsorptionFactor(drinkTime: Date, targetTime: Date = new Date()): number {
    // Time elapsed since drink was consumed (in minutes)
    const minutesSinceDrink = Math.max(0, (targetTime.getTime() - drinkTime.getTime()) / (60 * 1000));

    // Get food state at time of drink
    const [foodType, minutesSinceFood] = this.getMostRecentFood(drinkTime);
    const gastricHalfTime = FOOD_GASTRIC_TIMES[foodType] ?? 90;

    if (gastricHalfTime === 0) {
      // Empty stomach - fast absorption: ~80% in 30 min, ~95% in 60 min
      // Ensure minimum 10% immediate absorption
      const absorption = 0.10 + 0.90 * (1.0 - Math.exp(-minutesSinceDrink / 20));
      return Math.min(1.0, absorption);
    } else {
      // Food delays absorption
      const delayFactor = Math.min(1.0, minutesSinceFood / gastricHalfTime);

      // Adjust absorption rate based on food
      const effectiveAbsorptionTime = minutesSinceDrink * (0.5 + 0.5 * delayFactor);

      // Ensure minimum 10% immediate absorption even with food
      const absorption = 0.10 + 0.90 * (1.0 - Math.exp(-effectiveAbsorptionTime / 30));
      return Math.min(1.0, absorption);
    }
  }

  /**
   * Calculate BAC at a specific time using Widmark equation with food absorption.
   * BAC = [(A × 5.14) / (W × r)] - (0.015 × H)
   */
  calculateBACAtTime(targetTime: Date = new Date()): number {
    if (targetTime < this.startTime) {
      return 0.0;
    }

    // Get Widmark parameters
    const widmarkRatio = WIDMARK_RATIOS[this.profile.sex];
    const bodyWeight = this.profile.weightLbs;

    // Account for metabolism variation
    let eliminationRate = ELIMINATION_RATE;
    if (this.profile.chronicDrinker) {
      eliminationRate *= 1.2; // 20% faster for chronic drinkers
    }

    // Calculate absorption for each drink
    let totalAlcoholAbsorbed = 0.0;

    for (const drink of this.drinks) {
      if (drink.time <= targetTime) {
        // Alcohol in this drink (liquid ounces)
        const alcoholOz = drink.sizeOz * (drink.alcoholPercent / 100);

        // Absorption factor accounts for food effects and time elapsed
        const absorptionFactor = this.calculateAbsorptionFactor(drink.time, targetTime);

        // Food reduces peak BAC (applied separately from absorption timing)
        const [foodType] = this.getMostRecentFood(drink.time);
        const peakReduction = FOOD_ABSORPTION_IMPACT[foodType] ?? 0.0;

        // Effective alcohol = actual alcohol * how much absorbed * food peak reduction
        const effectiveAlcoholOz = alcoholOz * absorptionFactor * (1 - peakReduction * 0.5);

        totalAlcoholAbsorbed += effectiveAlcoholOz;
      }
    }

    // Widmark equation: BAC = [(A × 5.14) / (W × r)] - (0.015 × H)
    let bacFromAbsorption = 0.0;
    if (totalAlcoholAbsorbed > 0) {
      bacFromAbsorption = (totalAlcoholAbsorbed * 5.14) / (bodyWeight * widmarkRatio);
    }

    // Time since first drink (hours)
    const timeSinceFirst = (targetTime.getTime() - this.startTime.getTime()) / (3600 * 1000);
    const elimination = eliminationRate * Math.max(0, timeSinceFirst);

    const bac = Math.max(0.0, bacFromAbsorption - elimination);
    return Math.round(bac * 10000) / 10000; // Round to 4 decimal places
  }

  /**
   * Get current BAC
   */
  getCurrentBAC(): number {
    return this.calculateBACAtTime(new Date());
  }

  /**
   * Generate BAC values for timeline visualization
   * @param hours Number of hours to project
   * @param fromNow If true, start from current time (future projection)
   */
  getBACTimeline(hours: number = 6, fromNow: boolean = true): TimelinePoint[] {
    const timeline: TimelinePoint[] = [];

    const start = fromNow ? new Date() : this.startTime;
    const endTime = new Date(start.getTime() + hours * 60 * 60 * 1000);

    // Sample every 5 minutes
    let currentTime = new Date(start);
    while (currentTime <= endTime) {
      const bac = this.calculateBACAtTime(currentTime);
      timeline.push({ time: new Date(currentTime), bac });
      currentTime = new Date(currentTime.getTime() + 5 * 60 * 1000);
    }

    return timeline;
  }

  /**
   * Find peak BAC and when it occurs
   */
  getPeakBAC(): BACPeak {
    const timeline = this.getBACTimeline(6, false);
    let peakBac = 0.0;
    let peakTime = this.startTime;

    for (const point of timeline) {
      if (point.bac > peakBac) {
        peakBac = point.bac;
        peakTime = point.time;
      }
    }

    return { bac: peakBac, time: peakTime };
  }

  /**
   * Calculate time until BAC drops below threshold
   * @param threshold BAC threshold (default: 0.0 for complete sobriety)
   * @returns Minutes until threshold reached, or null if already below
   */
  getTimeToSobriety(threshold: number = 0.0): number | null {
    const timeline = this.getBACTimeline(24, true);
    const now = new Date();

    for (const point of timeline) {
      if (point.bac <= threshold) {
        return Math.round((point.time.getTime() - now.getTime()) / (60 * 1000));
      }
    }

    return null; // More than 24 hours
  }

  /**
   * Calculate time until BAC reaches legal limit (0.08%)
   * @returns Minutes until legal limit reached, or null if won't reach
   */
  getTimeToLegalLimit(): number | null {
    const timeline = this.getBACTimeline(6, true);
    const now = new Date();

    for (const point of timeline) {
      if (point.bac >= 0.08) {
        return Math.round((point.time.getTime() - now.getTime()) / (60 * 1000));
      }
    }

    return null; // Won't reach legal limit
  }

  /**
   * Get time when BAC will drop below legal limit
   * @returns Date when safe to drive, or null if already legal
   */
  getTimeWhenLegal(): Date | null {
    const currentBAC = this.getCurrentBAC();
    if (currentBAC < 0.08) {
      return null; // Already legal
    }

    const timeline = this.getBACTimeline(24, true);
    for (const point of timeline) {
      if (point.bac < 0.08) {
        return point.time;
      }
    }

    return null;
  }

  /**
   * Get impairment description and legal status for BAC level
   */
  getImpairmentLevel(bac?: number): ImpairmentLevel {
    const currentBac = bac ?? this.getCurrentBAC();

    // Find appropriate level (iterate in reverse to find highest matching threshold)
    for (let i = IMPAIRMENT_LEVELS.length - 1; i >= 0; i--) {
      if (currentBac >= IMPAIRMENT_LEVELS[i].threshold) {
        return IMPAIRMENT_LEVELS[i];
      }
    }

    return IMPAIRMENT_LEVELS[0];
  }

  /**
   * Get full BAC result with impairment level
   */
  getBACResult(): BACResult {
    const bac = this.getCurrentBAC();
    return {
      bac,
      impairmentLevel: this.getImpairmentLevel(bac),
      timestamp: new Date(),
    };
  }

  /**
   * Reset all data for new scenario
   */
  clearScenario(): void {
    this.drinks = [];
    this.foods = [];
    this.startTime = new Date();
  }

  /**
   * Check if there are any drinks logged
   */
  hasDrinks(): boolean {
    return this.drinks.length > 0;
  }

  /**
   * Get start time of drinking session
   */
  getStartTime(): Date {
    return new Date(this.startTime);
  }
}

/**
 * Create a new BAC calculator instance
 */
export function createBACCalculator(profile?: Partial<UserProfile>): BACCalculator {
  return new BACCalculator(profile);
}

/**
 * Format BAC as percentage string
 */
export function formatBAC(bac: number): string {
  return `${(bac * 100).toFixed(2)}%`;
}

/**
 * Format BAC as decimal string (e.g., "0.08")
 */
export function formatBACDecimal(bac: number): string {
  return bac.toFixed(3);
}

/**
 * Format time duration in minutes to human-readable string
 */
export function formatDuration(minutes: number | null): string {
  if (minutes === null) return 'N/A';
  if (minutes < 60) return `${Math.round(minutes)} min`;

  const hours = Math.floor(minutes / 60);
  const mins = Math.round(minutes % 60);

  if (mins === 0) return `${hours}h`;
  return `${hours}h ${mins}m`;
}

/**
 * Calculate standard drinks equivalent
 * One standard drink = 0.6 oz of pure alcohol
 */
export function calculateStandardDrinks(sizeOz: number, alcoholPercent: number): number {
  const pureAlcoholOz = sizeOz * (alcoholPercent / 100);
  return Math.round((pureAlcoholOz / 0.6) * 10) / 10;
}
