'use client';

import { useState, useCallback, useEffect } from 'react';
import { UserProfile, DrinkType, FoodType, Drink, Food, BACResult, TimelinePoint, BACPeak } from '@/lib/types';
import { BACCalculator, createBACCalculator } from '@/lib/bac-calculator';

export interface UseBACCalculatorReturn {
  // Current state
  profile: UserProfile;
  drinks: Drink[];
  foods: Food[];
  bacResult: BACResult;
  timeline: TimelinePoint[];
  peak: BACPeak;
  timeToSobriety: number | null;
  timeWhenLegal: Date | null;

  // Actions
  setProfile: (profile: Partial<UserProfile>) => void;
  addDrink: (time: Date, type: DrinkType, quantity?: number, alcoholPercent?: number) => void;
  addFood: (time: Date, type: FoodType) => void;
  removeDrink: (id: string) => void;
  removeFood: (id: string) => void;
  clearScenario: () => void;
}

export function useBACCalculator(
  initialProfile?: Partial<UserProfile>,
  updateInterval: number = 2000
): UseBACCalculatorReturn {
  const [calculator] = useState(() => createBACCalculator(initialProfile));
  const [, forceUpdate] = useState({});

  // Force re-render to get latest state from calculator
  const refresh = useCallback(() => forceUpdate({}), []);

  // Auto-update BAC values
  useEffect(() => {
    const interval = setInterval(refresh, updateInterval);
    return () => clearInterval(interval);
  }, [refresh, updateInterval]);

  // Actions
  const setProfile = useCallback((profile: Partial<UserProfile>) => {
    calculator.setProfile(profile);
    refresh();
  }, [calculator, refresh]);

  const addDrink = useCallback((
    time: Date,
    type: DrinkType,
    quantity: number = 1,
    alcoholPercent?: number
  ) => {
    calculator.addDrink(time, type, undefined, alcoholPercent, quantity);
    refresh();
  }, [calculator, refresh]);

  const addFood = useCallback((time: Date, type: FoodType) => {
    calculator.addFood(time, type);
    refresh();
  }, [calculator, refresh]);

  const removeDrink = useCallback((id: string) => {
    calculator.removeDrink(id);
    refresh();
  }, [calculator, refresh]);

  const removeFood = useCallback((id: string) => {
    calculator.removeFood(id);
    refresh();
  }, [calculator, refresh]);

  const clearScenario = useCallback(() => {
    calculator.clearScenario();
    refresh();
  }, [calculator, refresh]);

  return {
    profile: calculator.getProfile(),
    drinks: calculator.getDrinks(),
    foods: calculator.getFoods(),
    bacResult: calculator.getBACResult(),
    timeline: calculator.getBACTimeline(6, true),
    peak: calculator.getPeakBAC(),
    timeToSobriety: calculator.getTimeToSobriety(0),
    timeWhenLegal: calculator.getTimeWhenLegal(),
    setProfile,
    addDrink,
    addFood,
    removeDrink,
    removeFood,
    clearScenario,
  };
}
