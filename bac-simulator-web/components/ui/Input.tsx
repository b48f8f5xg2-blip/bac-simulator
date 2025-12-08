'use client';

import { forwardRef, InputHTMLAttributes } from 'react';

export interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helpText?: string;
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className = '', label, error, helpText, id, ...props }, ref) => {
    const inputId = id || label?.toLowerCase().replace(/\s+/g, '-');

    return (
      <div className="w-full">
        {label && (
          <label htmlFor={inputId} className="block text-sm font-medium text-slate-600 mb-1.5">
            {label}
          </label>
        )}
        <input
          ref={ref}
          id={inputId}
          className={`
            w-full px-4 py-3 rounded-lg border bg-white
            text-slate-700 placeholder-neutral-500
            transition-all duration-200
            focus:outline-none focus:ring-2 focus:ring-primary-100
            ${error
              ? 'border-bac-danger focus:border-bac-danger focus:ring-red-100'
              : 'border-neutral-300 focus:border-primary-500'
            }
            ${className}
          `}
          {...props}
        />
        {error && (
          <p className="text-xs text-bac-danger mt-1">{error}</p>
        )}
        {helpText && !error && (
          <p className="text-xs text-neutral-600 mt-1">{helpText}</p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';

export { Input };
