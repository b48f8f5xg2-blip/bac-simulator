import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Primary brand color - Teal
        primary: {
          DEFAULT: '#00BFAE',
          50: '#E6FAF8',
          100: '#B3F0EB',
          200: '#80E6DE',
          300: '#4DD9D0',
          400: '#26CFC4',
          500: '#00BFAE',
          600: '#00A899',
          700: '#008F83',
          800: '#00756C',
          900: '#004D47',
        },
        // Secondary dark - Dark Teal
        secondary: {
          DEFAULT: '#004040',
          50: '#E6EDED',
          100: '#B3CCCC',
          200: '#80ABAB',
          300: '#4D8A8A',
          400: '#266969',
          500: '#004040',
          600: '#003838',
          700: '#002E2E',
          800: '#002424',
          900: '#001616',
        },
        // Neutral - Light Gray
        neutral: {
          DEFAULT: '#BFBEBE',
          50: '#FAFAFA',
          100: '#F5F5F5',
          200: '#EEEEEE',
          300: '#E0E0E0',
          400: '#CFCECE',
          500: '#BFBEBE',
          600: '#9E9E9E',
          700: '#757575',
          800: '#616161',
          900: '#424242',
        },
        // Accent - Green
        accent: {
          DEFAULT: '#029922',
          50: '#E6F5E9',
          100: '#B3E2BE',
          200: '#80CF93',
          300: '#4DBC68',
          400: '#26AC43',
          500: '#029922',
          600: '#02871E',
          700: '#017219',
          800: '#015E15',
          900: '#003E0E',
        },
        // Supporting - Dark Slate
        slate: {
          DEFAULT: '#4A4A63',
          50: '#EDEDF0',
          100: '#C9C9D4',
          200: '#A5A5B8',
          300: '#81819C',
          400: '#656588',
          500: '#4A4A63',
          600: '#414158',
          700: '#36364A',
          800: '#2B2B3B',
          900: '#1C1C27',
        },
        // BAC status colors
        bac: {
          safe: '#029922',
          caution: '#F59E0B',
          warning: '#F97316',
          danger: '#EF4444',
          critical: '#991B1B',
        },
      },
      fontFamily: {
        sans: ['-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Helvetica', 'Arial', 'sans-serif'],
        mono: ['SF Mono', 'Monaco', 'Menlo', 'Consolas', 'monospace'],
      },
      fontSize: {
        'display': ['4.75rem', { lineHeight: '1.1', fontWeight: '700' }],
        'h1': ['3rem', { lineHeight: '1.2', fontWeight: '700' }],
        'h2': ['2rem', { lineHeight: '1.3', fontWeight: '600' }],
        'h3': ['1.5rem', { lineHeight: '1.4', fontWeight: '600' }],
        'body': ['1rem', { lineHeight: '1.6', fontWeight: '400' }],
        'small': ['0.875rem', { lineHeight: '1.5', fontWeight: '400' }],
        'caption': ['0.75rem', { lineHeight: '1.4', fontWeight: '400' }],
      },
      spacing: {
        '18': '4.5rem',
        '22': '5.5rem',
      },
      borderRadius: {
        '2xl': '1rem',
        '3xl': '1.5rem',
      },
      boxShadow: {
        'card': '0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06)',
        'card-hover': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        'button': '0 1px 2px rgba(0, 0, 0, 0.05)',
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'pulse-slow': 'pulse 3s ease-in-out infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
    },
  },
  plugins: [],
}
export default config
