'use client';

import { useMemo } from 'react';
import { TimelinePoint } from '@/lib/types';
import { Card, CardHeader, CardTitle, CardContent } from './ui';

interface TimelineChartProps {
  timeline: TimelinePoint[];
  currentBAC?: number;
  showLegalLimit?: boolean;
  showEnhancedDUILimit?: boolean;
  height?: number;
}

export function TimelineChart({
  timeline,
  currentBAC,
  showLegalLimit = true,
  showEnhancedDUILimit = true,
  height = 220,
}: TimelineChartProps) {
  const padding = { top: 20, right: 20, bottom: 40, left: 50 };
  const width = 400; // Will be responsive

  const chartWidth = width - padding.left - padding.right;
  const chartHeight = height - padding.top - padding.bottom;

  // Calculate chart bounds
  const { maxBAC, minTime, maxTime, points, legalLimitY, enhancedDUIY } = useMemo(() => {
    if (timeline.length === 0) {
      return {
        maxBAC: 0.1,
        minTime: new Date(),
        maxTime: new Date(Date.now() + 6 * 60 * 60 * 1000),
        points: '',
        legalLimitY: chartHeight,
        enhancedDUIY: chartHeight,
      };
    }

    const bacValues = timeline.map(p => p.bac);
    const maxBAC = Math.max(0.1, ...bacValues, 0.08, 0.15) * 1.1; // Add 10% headroom
    const minTime = timeline[0].time;
    const maxTime = timeline[timeline.length - 1].time;

    const timeRange = maxTime.getTime() - minTime.getTime();

    // Generate SVG path points
    const points = timeline
      .map(point => {
        const x = ((point.time.getTime() - minTime.getTime()) / timeRange) * chartWidth;
        const y = chartHeight - (point.bac / maxBAC) * chartHeight;
        return `${x},${y}`;
      })
      .join(' ');

    const legalLimitY = chartHeight - (0.08 / maxBAC) * chartHeight;
    const enhancedDUIY = chartHeight - (0.15 / maxBAC) * chartHeight;

    return { maxBAC, minTime, maxTime, points, legalLimitY, enhancedDUIY };
  }, [timeline, chartHeight, chartWidth]);

  // Generate time labels
  const timeLabels = useMemo(() => {
    const labels: { x: number; label: string }[] = [];
    const timeRange = maxTime.getTime() - minTime.getTime();
    const hourCount = timeRange / (60 * 60 * 1000);
    const interval = hourCount <= 3 ? 1 : hourCount <= 6 ? 2 : 3;

    for (let i = 0; i <= Math.ceil(hourCount); i += interval) {
      const time = new Date(minTime.getTime() + i * 60 * 60 * 1000);
      const x = (i * 60 * 60 * 1000 / timeRange) * chartWidth;
      labels.push({
        x: Math.min(x, chartWidth),
        label: time.toLocaleTimeString('en-US', { hour: 'numeric', hour12: true }),
      });
    }

    return labels;
  }, [minTime, maxTime, chartWidth]);

  // Generate BAC labels
  const bacLabels = useMemo(() => {
    const labels: { y: number; label: string }[] = [];
    const step = maxBAC <= 0.1 ? 0.02 : maxBAC <= 0.2 ? 0.05 : 0.1;

    for (let bac = 0; bac <= maxBAC; bac += step) {
      const y = chartHeight - (bac / maxBAC) * chartHeight;
      labels.push({ y, label: bac.toFixed(2) });
    }

    return labels;
  }, [maxBAC, chartHeight]);

  const hasData = timeline.length > 0 && timeline.some(p => p.bac > 0);

  return (
    <Card>
      <CardHeader>
        <CardTitle>BAC Timeline</CardTitle>
        <p className="text-sm text-neutral-600 mt-1">6-hour projection</p>
      </CardHeader>
      <CardContent>
        <div className="relative w-full" style={{ height }}>
          <svg
            viewBox={`0 0 ${width} ${height}`}
            className="w-full h-full"
            preserveAspectRatio="xMidYMid meet"
          >
            <g transform={`translate(${padding.left}, ${padding.top})`}>
              {/* Grid lines */}
              {bacLabels.map(({ y }, i) => (
                <line
                  key={`grid-${i}`}
                  x1={0}
                  y1={y}
                  x2={chartWidth}
                  y2={y}
                  stroke="#E5E7EB"
                  strokeWidth={1}
                />
              ))}

              {/* Legal limit line (0.08%) */}
              {showLegalLimit && legalLimitY < chartHeight && (
                <>
                  <line
                    x1={0}
                    y1={legalLimitY}
                    x2={chartWidth}
                    y2={legalLimitY}
                    stroke="#EF4444"
                    strokeWidth={2}
                    strokeDasharray="6,4"
                  />
                  <text
                    x={chartWidth - 5}
                    y={legalLimitY - 5}
                    fill="#EF4444"
                    fontSize={10}
                    textAnchor="end"
                  >
                    Legal Limit (0.08%)
                  </text>
                </>
              )}

              {/* Enhanced DUI line (0.15%) */}
              {showEnhancedDUILimit && enhancedDUIY < chartHeight && (
                <>
                  <line
                    x1={0}
                    y1={enhancedDUIY}
                    x2={chartWidth}
                    y2={enhancedDUIY}
                    stroke="#991B1B"
                    strokeWidth={2}
                    strokeDasharray="6,4"
                  />
                  <text
                    x={chartWidth - 5}
                    y={enhancedDUIY - 5}
                    fill="#991B1B"
                    fontSize={10}
                    textAnchor="end"
                  >
                    Enhanced DUI (0.15%)
                  </text>
                </>
              )}

              {/* BAC curve */}
              {hasData && (
                <>
                  {/* Area fill */}
                  <polygon
                    points={`0,${chartHeight} ${points} ${chartWidth},${chartHeight}`}
                    fill="url(#bacGradient)"
                    opacity={0.3}
                  />
                  {/* Line */}
                  <polyline
                    points={points}
                    fill="none"
                    stroke="#00BFAE"
                    strokeWidth={3}
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </>
              )}

              {/* Current time indicator */}
              {hasData && currentBAC !== undefined && (
                <circle
                  cx={0}
                  cy={chartHeight - (currentBAC / maxBAC) * chartHeight}
                  r={6}
                  fill="#00BFAE"
                  stroke="white"
                  strokeWidth={2}
                />
              )}

              {/* Y-axis labels (BAC) */}
              {bacLabels.map(({ y, label }, i) => (
                <text
                  key={`bac-${i}`}
                  x={-10}
                  y={y + 4}
                  fill="#6F6F77"
                  fontSize={11}
                  textAnchor="end"
                >
                  {label}
                </text>
              ))}

              {/* X-axis labels (Time) */}
              {timeLabels.map(({ x, label }, i) => (
                <text
                  key={`time-${i}`}
                  x={x}
                  y={chartHeight + 20}
                  fill="#6F6F77"
                  fontSize={11}
                  textAnchor="middle"
                >
                  {label}
                </text>
              ))}

              {/* No data message */}
              {!hasData && (
                <text
                  x={chartWidth / 2}
                  y={chartHeight / 2}
                  fill="#9CA3AF"
                  fontSize={14}
                  textAnchor="middle"
                >
                  Add drinks to see timeline
                </text>
              )}
            </g>

            {/* Gradient definition */}
            <defs>
              <linearGradient id="bacGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#00BFAE" stopOpacity={0.4} />
                <stop offset="100%" stopColor="#00BFAE" stopOpacity={0.05} />
              </linearGradient>
            </defs>
          </svg>
        </div>

        {/* Legend */}
        <div className="flex items-center justify-center gap-6 mt-4 text-xs text-slate-600">
          <div className="flex items-center gap-2">
            <div className="w-4 h-1 bg-primary-500 rounded" />
            <span>Your BAC</span>
          </div>
          {showLegalLimit && (
            <div className="flex items-center gap-2">
              <div className="w-4 h-0.5 bg-bac-danger" style={{ borderTop: '2px dashed' }} />
              <span>Legal Limit</span>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
