'use client';

import { useState, FormEvent } from 'react';
import { UserProfile } from '@/lib/types';
import { Button, Input, Card, CardHeader, CardTitle, CardContent } from './ui';

interface ProfileFormProps {
  onSubmit: (profile: UserProfile) => void;
  initialProfile?: Partial<UserProfile>;
}

export function ProfileForm({ onSubmit, initialProfile }: ProfileFormProps) {
  const [formData, setFormData] = useState({
    sex: initialProfile?.sex || 'male',
    weightLbs: initialProfile?.weightLbs?.toString() || '',
    heightFeet: initialProfile?.heightInches ? Math.floor(initialProfile.heightInches / 12).toString() : '',
    heightInches: initialProfile?.heightInches ? (initialProfile.heightInches % 12).toString() : '',
    age: initialProfile?.age?.toString() || '',
    chronicDrinker: initialProfile?.chronicDrinker || false,
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const validate = (): boolean => {
    const newErrors: Record<string, string> = {};

    const weight = parseFloat(formData.weightLbs);
    if (!formData.weightLbs || isNaN(weight)) {
      newErrors.weight = 'Please enter your weight';
    } else if (weight < 80 || weight > 500) {
      newErrors.weight = 'Weight must be between 80-500 lbs';
    }

    const feet = parseInt(formData.heightFeet);
    const inches = parseInt(formData.heightInches || '0');
    if (!formData.heightFeet || isNaN(feet)) {
      newErrors.height = 'Please enter your height';
    } else if (feet < 4 || feet > 8) {
      newErrors.height = 'Height must be between 4-8 feet';
    }

    const age = parseInt(formData.age);
    if (!formData.age || isNaN(age)) {
      newErrors.age = 'Please enter your age';
    } else if (age < 18) {
      newErrors.age = 'You must be 18 or older';
    } else if (age > 120) {
      newErrors.age = 'Please enter a valid age';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();

    if (!validate()) return;

    setIsSubmitting(true);

    const feet = parseInt(formData.heightFeet);
    const inches = parseInt(formData.heightInches || '0');

    const profile: UserProfile = {
      sex: formData.sex as 'male' | 'female',
      weightLbs: parseFloat(formData.weightLbs),
      heightInches: feet * 12 + inches,
      age: parseInt(formData.age),
      chronicDrinker: formData.chronicDrinker,
    };

    onSubmit(profile);
    setIsSubmitting(false);
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Your Profile</CardTitle>
        <p className="text-sm text-neutral-600 mt-1">
          This information helps calculate accurate BAC estimates
        </p>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Sex Selection */}
          <div>
            <label className="block text-sm font-medium text-slate-600 mb-2">Biological Sex</label>
            <div className="flex gap-3">
              <button
                type="button"
                onClick={() => setFormData(prev => ({ ...prev, sex: 'male' }))}
                className={`
                  flex-1 py-3 px-4 rounded-lg border-2 font-medium transition-all
                  ${formData.sex === 'male'
                    ? 'border-primary-500 bg-primary-50 text-primary-700'
                    : 'border-neutral-300 bg-white text-slate-600 hover:border-neutral-400'
                  }
                `}
              >
                Male
              </button>
              <button
                type="button"
                onClick={() => setFormData(prev => ({ ...prev, sex: 'female' }))}
                className={`
                  flex-1 py-3 px-4 rounded-lg border-2 font-medium transition-all
                  ${formData.sex === 'female'
                    ? 'border-primary-500 bg-primary-50 text-primary-700'
                    : 'border-neutral-300 bg-white text-slate-600 hover:border-neutral-400'
                  }
                `}
              >
                Female
              </button>
            </div>
            <p className="text-xs text-neutral-500 mt-1">
              Affects alcohol distribution (Widmark ratio)
            </p>
          </div>

          {/* Weight */}
          <Input
            label="Weight (lbs)"
            type="number"
            placeholder="180"
            value={formData.weightLbs}
            onChange={(e) => setFormData(prev => ({ ...prev, weightLbs: e.target.value }))}
            error={errors.weight}
            helpText="Your body weight in pounds"
            min={80}
            max={500}
          />

          {/* Height */}
          <div>
            <label className="block text-sm font-medium text-slate-600 mb-1.5">Height</label>
            <div className="flex gap-3">
              <div className="flex-1">
                <Input
                  type="number"
                  placeholder="5"
                  value={formData.heightFeet}
                  onChange={(e) => setFormData(prev => ({ ...prev, heightFeet: e.target.value }))}
                  min={4}
                  max={8}
                />
                <span className="text-xs text-neutral-500 mt-1 block">Feet</span>
              </div>
              <div className="flex-1">
                <Input
                  type="number"
                  placeholder="10"
                  value={formData.heightInches}
                  onChange={(e) => setFormData(prev => ({ ...prev, heightInches: e.target.value }))}
                  min={0}
                  max={11}
                />
                <span className="text-xs text-neutral-500 mt-1 block">Inches</span>
              </div>
            </div>
            {errors.height && <p className="text-xs text-bac-danger mt-1">{errors.height}</p>}
          </div>

          {/* Age */}
          <Input
            label="Age"
            type="number"
            placeholder="30"
            value={formData.age}
            onChange={(e) => setFormData(prev => ({ ...prev, age: e.target.value }))}
            error={errors.age}
            min={18}
            max={120}
          />

          {/* Chronic Drinker */}
          <div>
            <label className="flex items-center gap-3 cursor-pointer">
              <div
                className={`
                  relative w-12 h-6 rounded-full transition-colors
                  ${formData.chronicDrinker ? 'bg-primary-500' : 'bg-neutral-300'}
                `}
                onClick={() => setFormData(prev => ({ ...prev, chronicDrinker: !prev.chronicDrinker }))}
              >
                <div
                  className={`
                    absolute top-0.5 w-5 h-5 bg-white rounded-full shadow transition-transform
                    ${formData.chronicDrinker ? 'translate-x-6' : 'translate-x-0.5'}
                  `}
                />
              </div>
              <span className="text-sm font-medium text-slate-600">Regular drinker</span>
            </label>
            <p className="text-xs text-neutral-500 mt-1 ml-15">
              Frequent drinkers metabolize alcohol ~20% faster
            </p>
          </div>

          <Button type="submit" className="w-full" size="lg" isLoading={isSubmitting}>
            Apply Profile
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
