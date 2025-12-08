# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BAC Simulator is a multi-platform educational blood alcohol content (BAC) calculator. It uses the modified Widmark equation with food absorption modeling to simulate alcohol metabolism.

**Two Applications:**
1. **Desktop App** (macOS) - Python/Tkinter native application
2. **Web App** - Modern Next.js 15 + React 19 + TypeScript application

## Color Palette (Design System)

| Color         | Hex       | Usage                              |
|---------------|-----------|-----------------------------------|
| Primary Teal  | `#00BFAE` | Main brand, buttons, active states |
| Dark Teal     | `#004040` | App bar, dark surfaces, navigation |
| Light Neutral | `#BFBEBE` | Cards, secondary surfaces          |
| Green Accent  | `#029922` | Success states, safe BAC           |
| Dark Slate    | `#4A4A63` | Text, borders                      |

### BAC Status Colors
- Safe (0.00-0.05%): `#029922` (green)
- Caution (0.05-0.08%): `#F59E0B` (yellow)
- Warning (0.08-0.15%): `#F97316` (orange)
- Danger (0.15-0.20%): `#EF4444` (red)
- Critical (0.20%+): `#991B1B` (dark red)

---

## Desktop Application (macOS)

### Running the Desktop App

```bash
# Launch the .app bundle
open BAC_Simulator.app

# Or run directly via Python
python3 BAC_Simulator.app/Contents/MacOS/BAC_Simulator
```

### Desktop Architecture

```
BAC_Simulator.app/Contents/
├── MacOS/BAC_Simulator    # Entry point (GUI mode, falls back to terminal)
├── Resources/
│   ├── bac_calculator.py  # Core BAC calculation engine (Widmark equation)
│   ├── chatbot.py         # Natural language parsing
│   ├── gui.py             # Tkinter-based GUI
│   └── terminal_ui.py     # Terminal fallback interface
└── Info.plist             # macOS bundle configuration
```

---

## Web Application (Next.js)

### Running the Web App

```bash
cd bac-simulator-web

# Install dependencies
npm install

# Development server
npm run dev

# Production build
npm run build

# Serve static export
npm run start
# Or serve the /out directory with any static file server
```

### Web Architecture

```
bac-simulator-web/
├── app/
│   ├── layout.tsx        # Root layout with ToastProvider
│   ├── page.tsx          # Main application page
│   └── globals.css       # Design tokens + Tailwind base
├── components/
│   ├── ui/               # Base UI components
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   ├── Card.tsx
│   │   └── Toast.tsx
│   ├── ProfileForm.tsx   # User profile input form
│   ├── BACDisplay.tsx    # BAC number + status display
│   ├── TimelineChart.tsx # SVG-based BAC timeline
│   ├── ChatInterface.tsx # Conversational drink/food input
│   └── DrinkFoodLog.tsx  # Consumption history list
├── lib/
│   ├── types.ts          # TypeScript interfaces & constants
│   ├── bac-calculator.ts # Core calculation engine (ported)
│   └── chatbot-parser.ts # NLP parsing functions (ported)
├── hooks/
│   └── useBACCalculator.ts
├── tailwind.config.ts    # Design system colors & tokens
├── next.config.js        # Static export configuration
└── package.json
```

### Component Responsibilities

- **BACCalculator** (`lib/bac-calculator.ts`): TypeScript port of Widmark equation with food absorption
- **ChatbotParser** (`lib/chatbot-parser.ts`): Parses natural language for drinks/food/profile
- **ProfileForm**: Collects sex, weight, height, age, chronic drinker status
- **BACDisplay**: Shows current BAC with color-coded status, fitness to drive, peak BAC
- **TimelineChart**: 6-hour BAC projection with legal limit lines
- **ChatInterface**: Conversational input with quick action buttons

### Tech Stack

- Next.js 15 + React 19
- TypeScript (strict mode)
- Tailwind CSS
- No external charting libraries (custom SVG)

---

## Core Algorithm (Both Apps)

### Widmark Equation
```
BAC = [(A × 5.14) / (W × r)] - (0.015 × H)
```
Where:
- A = alcohol consumed (fluid ounces of pure alcohol)
- W = body weight (lbs)
- r = Widmark ratio (male=0.73, female=0.66)
- H = hours since drinking started
- 0.015 = elimination rate (%/hour)

### Key Constants

| Constant              | Value   | Notes                           |
|-----------------------|---------|--------------------------------|
| Male Widmark ratio    | 0.73    | Distribution coefficient       |
| Female Widmark ratio  | 0.66    | Distribution coefficient       |
| Elimination rate      | 0.015%/hr | ~15 mg/100mL per hour       |
| DUI threshold         | 0.08%   | Standard legal limit           |
| Enhanced DUI          | 0.15%   | Aggravated DUI threshold       |

### Food Absorption Impact

| Food Type        | Gastric Time | Peak Reduction |
|------------------|--------------|----------------|
| Empty stomach    | 0 min        | 0%             |
| Water/liquids    | 15 min       | 5%             |
| Light snack      | 60 min       | 20%            |
| Light meal       | 90 min       | 30%            |
| Moderate meal    | 120 min      | 40%            |
| Full meal        | 150 min      | 45%            |
| High-fat meal    | 180 min      | 60%            |

---

## Development Guidelines

### Desktop App (Python)
- Python 3.9+ standard library only
- No external dependencies required
- Tkinter for GUI (optional)

### Web App (TypeScript)
- Use existing design system colors from `tailwind.config.ts`
- Components should be "use client" for interactivity
- Prefer editing existing files over creating new ones
- Run `npm run build` to verify TypeScript before committing

### Testing
- Web app: `npm run lint` for linting
- Both: Manual testing with various scenarios
  - Empty stomach + multiple drinks
  - Full meal + drinks (delayed absorption)
  - Peak BAC projection accuracy
  - Time to sobriety calculation

---

## Files Reference

### Recently Fixed (Desktop App)
- `chatbot.py`: Added `process_message()` method
- `bac_calculator.py`: Fixed absorption factor at t=0, removed double food penalty, fixed timeline projection
- `gui.py`: Fixed canvas rendering, changed update rate to 2s

### Logo Design
See `LOGO_DESIGN_SPECS.md` for icon/logo creation guidelines.
