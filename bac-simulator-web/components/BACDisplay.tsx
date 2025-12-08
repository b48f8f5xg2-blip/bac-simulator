'use client';

import { BACResult, BACStatusColor, BACPeak } from '@/lib/types';
import { formatBAC, formatDuration } from '@/lib/bac-calculator';
import { Card } from './ui';

interface BACDisplayProps {
  result: BACResult;
  peak?: BACPeak | null;
  timeToSobriety?: number | null;
  timeWhenLegal?: Date | null;
}

export function BACDisplay({ result, peak, timeToSobriety, timeWhenLegal }: BACDisplayProps) {
  const { bac, impairmentLevel } = result;

  const colorClasses: Record<BACStatusColor, string> = {
    safe: 'text-bac-safe',
    caution: 'text-bac-caution',
    warning: 'text-bac-warning',
    danger: 'text-bac-danger',
    critical: 'text-bac-critical',
  };

  const bgColorClasses: Record<BACStatusColor, string> = {
    safe: 'bg-accent-50',
    caution: 'bg-yellow-50',
    warning: 'bg-orange-50',
    danger: 'bg-red-50',
    critical: 'bg-red-100',
  };

  const badgeColorClasses: Record<BACStatusColor, string> = {
    safe: 'bg-accent-100 text-accent-800',
    caution: 'bg-yellow-100 text-yellow-800',
    warning: 'bg-orange-100 text-orange-800',
    danger: 'bg-red-100 text-red-800',
    critical: 'bg-red-200 text-red-900',
  };

  return (
    <Card padding="lg" className={bgColorClasses[impairmentLevel.color]}>
      <div className="text-center">
        {/* BAC Number */}
        <div className="mb-4">
          <div className={`bac-display ${colorClasses[impairmentLevel.color]}`}>
            {bac.toFixed(3)}
          </div>
          <div className="text-sm text-slate-600 mt-1">Blood Alcohol Content (%)</div>
        </div>

        {/* Status Badge */}
        <div className={`inline-flex items-center px-4 py-2 rounded-full text-sm font-semibold ${badgeColorClasses[impairmentLevel.color]}`}>
          {impairmentLevel.level}
        </div>

        {/* Description */}
        <p className="text-slate-600 mt-4 text-sm">
          {impairmentLevel.description}
        </p>

        {/* Fitness to Drive */}
        <div className="mt-6 pt-4 border-t border-neutral-200">
          <div className="flex items-center justify-center gap-2">
            <DriveIcon fitness={impairmentLevel.fitnessToDriver} />
            <span className={`font-semibold ${
              impairmentLevel.fitnessToDriver === 'YES' ? 'text-accent-600' :
              impairmentLevel.fitnessToDriver === 'CAUTION' ? 'text-bac-caution' : 'text-bac-danger'
            }`}>
              {impairmentLevel.fitnessToDriver === 'YES' && 'Safe to Drive'}
              {impairmentLevel.fitnessToDriver === 'CAUTION' && 'Caution Advised'}
              {impairmentLevel.fitnessToDriver === 'NO' && 'Do Not Drive'}
            </span>
          </div>
          <div className="text-xs text-slate-500 mt-1">
            Legal Status: {impairmentLevel.legalStatus}
          </div>
        </div>

        {/* Additional Info */}
        <div className="mt-6 grid grid-cols-2 gap-4 text-left">
          {peak && peak.bac > 0 && (
            <div className="bg-white/60 rounded-lg p-3">
              <div className="text-xs text-slate-500 uppercase tracking-wide">Peak BAC</div>
              <div className="text-lg font-bold text-slate-800">{peak.bac.toFixed(3)}</div>
              <div className="text-xs text-slate-600">
                {formatTimeDistance(peak.time)}
              </div>
            </div>
          )}

          {timeToSobriety !== null && timeToSobriety !== undefined && timeToSobriety > 0 && (
            <div className="bg-white/60 rounded-lg p-3">
              <div className="text-xs text-slate-500 uppercase tracking-wide">Time to Sober</div>
              <div className="text-lg font-bold text-slate-800">{formatDuration(timeToSobriety)}</div>
              <div className="text-xs text-slate-600">To reach 0.00%</div>
            </div>
          )}

          {timeWhenLegal && (
            <div className="bg-white/60 rounded-lg p-3 col-span-2">
              <div className="text-xs text-slate-500 uppercase tracking-wide">Legal to Drive At</div>
              <div className="text-lg font-bold text-slate-800">
                {timeWhenLegal.toLocaleTimeString('en-US', {
                  hour: 'numeric',
                  minute: '2-digit',
                  hour12: true,
                })}
              </div>
              <div className="text-xs text-slate-600">When BAC drops below 0.08%</div>
            </div>
          )}
        </div>
      </div>
    </Card>
  );
}

function DriveIcon({ fitness }: { fitness: 'YES' | 'CAUTION' | 'NO' }) {
  if (fitness === 'YES') {
    return (
      <svg className="w-6 h-6 text-accent-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    );
  }

  if (fitness === 'CAUTION') {
    return (
      <svg className="w-6 h-6 text-bac-caution" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
      </svg>
    );
  }

  return (
    <svg className="w-6 h-6 text-bac-danger" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
    </svg>
  );
}

function formatTimeDistance(date: Date): string {
  const now = new Date();
  const diff = date.getTime() - now.getTime();

  if (diff < 0) {
    // Past
    const minutes = Math.abs(diff) / (60 * 1000);
    if (minutes < 60) {
      return `${Math.round(minutes)} min ago`;
    }
    const hours = minutes / 60;
    return `${Math.round(hours * 10) / 10}h ago`;
  } else {
    // Future
    const minutes = diff / (60 * 1000);
    if (minutes < 60) {
      return `in ${Math.round(minutes)} min`;
    }
    const hours = minutes / 60;
    return `in ${Math.round(hours * 10) / 10}h`;
  }
}
