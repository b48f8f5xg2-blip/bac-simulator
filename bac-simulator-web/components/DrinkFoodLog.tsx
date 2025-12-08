'use client';

import { Drink, Food, DRINK_DISPLAY_NAMES, FOOD_DISPLAY_NAMES } from '@/lib/types';
import { Card, CardHeader, CardTitle, CardContent, Button } from './ui';

interface DrinkFoodLogProps {
  drinks: Drink[];
  foods: Food[];
  onRemoveDrink?: (id: string) => void;
  onRemoveFood?: (id: string) => void;
}

export function DrinkFoodLog({ drinks, foods, onRemoveDrink, onRemoveFood }: DrinkFoodLogProps) {
  const allItems = [
    ...drinks.map(d => ({ ...d, itemType: 'drink' as const })),
    ...foods.map(f => ({ ...f, itemType: 'food' as const })),
  ].sort((a, b) => b.time.getTime() - a.time.getTime());

  const drinkIcons: Record<string, string> = {
    beer_light: '🍺',
    beer_regular: '🍺',
    beer_ipa: '🍺',
    beer_stout: '🍺',
    wine_light: '🍷',
    wine_red: '🍷',
    wine_fortified: '🍷',
    spirits: '🥃',
    mixed_drink: '🍸',
  };

  const foodIcons: Record<string, string> = {
    empty_stomach: '🚫',
    water: '💧',
    light_snack: '🥨',
    light_meal: '🥗',
    moderate_meal: '🍽️',
    full_meal: '🍱',
    high_fat_meal: '🍔',
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Consumption Log</CardTitle>
        <p className="text-sm text-neutral-600 mt-1">
          {drinks.length} drink{drinks.length !== 1 ? 's' : ''}, {foods.length} food item{foods.length !== 1 ? 's' : ''}
        </p>
      </CardHeader>
      <CardContent>
        {allItems.length === 0 ? (
          <div className="text-center py-8 text-neutral-500">
            <p>No items logged yet</p>
            <p className="text-sm mt-1">Add drinks or food using the chat</p>
          </div>
        ) : (
          <div className="space-y-2 max-h-[300px] overflow-y-auto">
            {allItems.map(item => (
              <div
                key={item.id}
                className="flex items-center justify-between p-3 bg-neutral-50 rounded-lg"
              >
                <div className="flex items-center gap-3">
                  <span className="text-xl">
                    {item.itemType === 'drink'
                      ? drinkIcons[item.type] || '🍹'
                      : foodIcons[item.type] || '🍽️'}
                  </span>
                  <div>
                    <p className="font-medium text-slate-800">
                      {item.itemType === 'drink'
                        ? DRINK_DISPLAY_NAMES[item.type as keyof typeof DRINK_DISPLAY_NAMES]
                        : FOOD_DISPLAY_NAMES[item.type as keyof typeof FOOD_DISPLAY_NAMES]}
                    </p>
                    <p className="text-xs text-neutral-600">
                      {item.time.toLocaleTimeString('en-US', {
                        hour: 'numeric',
                        minute: '2-digit',
                        hour12: true,
                      })}
                      {item.itemType === 'drink' && 'sizeOz' in item && (
                        <span className="ml-2">
                          · {item.sizeOz}oz · {item.alcoholPercent}%
                        </span>
                      )}
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => {
                    if (item.itemType === 'drink') {
                      onRemoveDrink?.(item.id);
                    } else {
                      onRemoveFood?.(item.id);
                    }
                  }}
                  className="p-1 hover:bg-neutral-200 rounded-full transition-colors"
                  aria-label="Remove"
                >
                  <svg className="w-4 h-4 text-neutral-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
