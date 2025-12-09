'use client';

import { useState, useEffect, useCallback } from 'react';
import Image from 'next/image';
import { UserProfile, Drink, Food, DrinkType, FoodType, STANDARD_DRINKS } from '@/lib/types';
import { BACCalculator, createBACCalculator } from '@/lib/bac-calculator';
import { ParsedMessage } from '@/lib/chatbot-parser';
import {
  ProfileForm,
  BACDisplay,
  TimelineChart,
  ChatInterface,
  DrinkFoodLog,
  useToast,
} from '@/components';

export default function Home() {
  const { addToast } = useToast();

  // Calculator state
  const [calculator] = useState(() => createBACCalculator());
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [drinks, setDrinks] = useState<Drink[]>([]);
  const [foods, setFoods] = useState<Food[]>([]);

  // BAC results (updated on interval)
  const [bacResult, setBacResult] = useState(calculator.getBACResult());
  const [timeline, setTimeline] = useState(calculator.getBACTimeline(6, true));
  const [peak, setPeak] = useState(calculator.getPeakBAC());
  const [timeToSobriety, setTimeToSobriety] = useState<number | null>(null);
  const [timeWhenLegal, setTimeWhenLegal] = useState<Date | null>(null);

  // Update BAC results
  const updateResults = useCallback(() => {
    setBacResult(calculator.getBACResult());
    setTimeline(calculator.getBACTimeline(6, true));
    setPeak(calculator.getPeakBAC());
    setTimeToSobriety(calculator.getTimeToSobriety(0));
    setTimeWhenLegal(calculator.getTimeWhenLegal());
    setDrinks(calculator.getDrinks());
    setFoods(calculator.getFoods());
  }, [calculator]);

  // Update every 2 seconds
  useEffect(() => {
    const interval = setInterval(updateResults, 2000);
    return () => clearInterval(interval);
  }, [updateResults]);

  // Handle profile submission
  const handleProfileSubmit = (newProfile: UserProfile) => {
    calculator.setProfile(newProfile);
    setProfile(newProfile);
    addToast('Profile saved!', 'success');
    updateResults();
  };

  // Handle drink added from chat
  const handleDrinkAdded = (drinkData: ParsedMessage['drinks'][0]) => {
    const stdDrink = STANDARD_DRINKS[drinkData.type];
    calculator.addDrink(
      drinkData.time,
      drinkData.type,
      stdDrink.oz,
      drinkData.alcoholPercent ?? stdDrink.alcoholPercent,
      drinkData.quantity
    );
    updateResults();
    addToast(`Added ${drinkData.quantity} ${drinkData.type.replace(/_/g, ' ')}`, 'success');
  };

  // Handle food added from chat
  const handleFoodAdded = (foodData: ParsedMessage['foods'][0]) => {
    calculator.addFood(foodData.time, foodData.type);
    updateResults();
    addToast(`Added ${foodData.type.replace(/_/g, ' ')}`, 'success');
  };

  // Handle drink removal
  const handleRemoveDrink = (id: string) => {
    calculator.removeDrink(id);
    updateResults();
    addToast('Drink removed', 'info');
  };

  // Handle food removal
  const handleRemoveFood = (id: string) => {
    calculator.removeFood(id);
    updateResults();
    addToast('Food removed', 'info');
  };

  // Handle reset
  const handleReset = () => {
    calculator.clearScenario();
    updateResults();
    addToast('Scenario cleared', 'info');
  };

  return (
    <div className="min-h-screen bg-neutral-100">
      {/* Header */}
      <header className="bg-secondary-500 text-white py-4 px-4 shadow-md">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Image
              src="/logo.svg"
              alt="BAC Simulator Logo"
              width={44}
              height={44}
              className="rounded-lg"
              priority
            />
            <div>
              <h1 className="text-xl font-bold">BAC Simulator</h1>
              <p className="text-xs text-primary-200">Blood Alcohol Calculator</p>
            </div>
          </div>
          <button
            onClick={handleReset}
            className="text-sm text-primary-200 hover:text-white transition-colors"
          >
            Reset
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Left Column - Profile & Log */}
          <div className="lg:col-span-4 space-y-6">
            <ProfileForm
              onSubmit={handleProfileSubmit}
              initialProfile={profile ?? undefined}
            />
            <DrinkFoodLog
              drinks={drinks}
              foods={foods}
              onRemoveDrink={handleRemoveDrink}
              onRemoveFood={handleRemoveFood}
            />
          </div>

          {/* Middle Column - BAC Display & Timeline */}
          <div className="lg:col-span-4 space-y-6">
            <BACDisplay
              result={bacResult}
              peak={peak}
              timeToSobriety={timeToSobriety}
              timeWhenLegal={timeWhenLegal}
            />
            <TimelineChart
              timeline={timeline}
              currentBAC={bacResult.bac}
            />
          </div>

          {/* Right Column - Chat */}
          <div className="lg:col-span-4">
            <ChatInterface
              onDrinkAdded={handleDrinkAdded}
              onFoodAdded={handleFoodAdded}
            />
          </div>
        </div>

        {/* Disclaimer */}
        <div className="mt-8 p-4 bg-bac-caution/10 border border-bac-caution/30 rounded-lg">
          <h3 className="font-semibold text-bac-caution mb-2">Important Disclaimer</h3>
          <p className="text-sm text-slate-600">
            This simulator provides estimates only and should not be used to determine if you are fit to drive.
            BAC levels vary significantly based on individual factors not captured here. When in doubt,
            <strong> don&apos;t drive</strong>. Use a designated driver, taxi, or rideshare service.
            <span className="block mt-2 font-medium">
              Legal limits: 0.08% (standard DUI), 0.15% (enhanced DUI in many states)
            </span>
          </p>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-slate-800 text-neutral-400 py-4 px-4 mt-8">
        <div className="max-w-7xl mx-auto text-center text-sm">
          <p>BAC Simulator - For educational purposes only</p>
          <p className="mt-1 text-xs">
            Uses the Widmark equation with food absorption modeling
          </p>
        </div>
      </footer>
    </div>
  );
}
