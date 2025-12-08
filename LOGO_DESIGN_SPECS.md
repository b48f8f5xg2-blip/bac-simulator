# BAC Simulator Logo & Icon Design Specifications

This document provides specifications for creating the BAC Simulator logo and iOS app icon
using external design tools (Canva, Figma, Adobe Illustrator, etc.).

## Brand Identity

**App Name:** BAC Simulator
**Tagline:** Blood Alcohol Calculator
**Purpose:** Educate users about alcohol metabolism and promote responsible drinking

---

## Color Palette

| Color Name    | Hex Code  | RGB             | Usage                              |
|---------------|-----------|-----------------|-----------------------------------|
| Primary Teal  | `#00BFAE` | (0, 191, 174)   | Main brand color, logo background |
| Dark Teal     | `#004040` | (0, 64, 64)     | Text, secondary elements          |
| Light Neutral | `#BFBEBE` | (191, 190, 190) | Subtle backgrounds                |
| Green Accent  | `#029922` | (2, 153, 34)    | Success states, safe indicators   |
| Dark Slate    | `#4A4A63` | (74, 74, 99)    | Text, borders                     |
| White         | `#FFFFFF` | (255, 255, 255) | Icon elements on colored bg       |

---

## Design Concept: "Shield + Pulse"

### Core Concept
- **Shield Shape**: Represents protection and safety (promoting safe drinking)
- **Pulse/Wave Line**: Represents BAC monitoring and the rise/fall of alcohol levels
- **Modern & Minimal**: Clean lines, no gradients in main icon, Apple guidelines compliant

### Visual Description
```
    ┌─────────────────┐
    │     ╭───────╮   │
    │    ╱         ╲  │
    │   ╱           ╲ │
    │  │   ~~~∿~~~   ││  ← Pulse wave through center
    │   ╲           ╱ │
    │    ╲         ╱  │
    │     ╰───────╯   │
    │     (shield)    │
    └─────────────────┘
```

### Icon Elements
1. **Rounded Square Background** (iOS standard): Primary Teal (#00BFAE)
2. **Shield Silhouette**: White (#FFFFFF) or Dark Teal (#004040)
3. **Pulse Wave**: Stylized sine wave cutting through shield center
4. **Optional**: Small "BAC" text or percentage symbol

---

## Required Sizes (iOS App Icon)

### Export the icon at ALL of these sizes:

| Size (px)    | Use Case                    | Filename              |
|--------------|-----------------------------|-----------------------|
| 1024 × 1024  | App Store                   | `icon-1024.png`       |
| 180 × 180    | iPhone (3x)                 | `icon-180.png`        |
| 167 × 167    | iPad Pro                    | `icon-167.png`        |
| 152 × 152    | iPad                        | `icon-152.png`        |
| 120 × 120    | iPhone (2x), Spotlight (3x) | `icon-120.png`        |
| 80 × 80      | Spotlight (2x)              | `icon-80.png`         |
| 76 × 76      | iPad (1x)                   | `icon-76.png`         |
| 60 × 60      | iPhone Notification (3x)    | `icon-60.png`         |
| 58 × 58      | Settings (3x)               | `icon-58.png`         |
| 40 × 40      | Spotlight (2x), Settings    | `icon-40.png`         |
| 29 × 29      | Settings (1x)               | `icon-29.png`         |
| 20 × 20      | Notification (2x)           | `icon-20.png`         |

### Favicon Sizes (Web)
| Size (px)    | Use Case                    | Filename              |
|--------------|-----------------------------|-----------------------|
| 512 × 512    | PWA                         | `icon-512.png`        |
| 192 × 192    | PWA, Android                | `icon-192.png`        |
| 32 × 32      | Favicon                     | `favicon-32.png`      |
| 16 × 16      | Favicon                     | `favicon-16.png`      |

---

## Logo Variations

### 1. App Icon (Primary)
- Square with rounded corners (iOS applies mask automatically)
- Teal background (#00BFAE)
- White shield with pulse wave
- No text

### 2. Logo Mark (Social/Favicon)
- Same as app icon but may need manual corner radius
- Works on light and dark backgrounds

### 3. Full Logo (Horizontal)
```
[Icon] BAC Simulator
```
- Icon + "BAC Simulator" wordmark
- Font: SF Pro Display Bold (or similar sans-serif)
- Text Color: Dark Teal (#004040) or White (on dark bg)

### 4. Monochrome Versions
- **Light Mode**: All Dark Teal (#004040)
- **Dark Mode**: All White (#FFFFFF)

---

## Design Guidelines

### DO:
- Keep the design simple and recognizable at small sizes
- Use solid colors (no gradients for main icon)
- Ensure high contrast between elements
- Test at 20x20 to verify legibility
- Center the design within the safe area (leave ~10% padding)

### DON'T:
- Add text to the main app icon (except for full logo)
- Use thin lines that disappear at small sizes
- Include alcohol imagery (bottles, glasses) - keep it abstract
- Use more than 3 colors in the icon
- Add drop shadows or 3D effects

---

## Technical Specifications

### File Format
- **PNG**: All sizes, with transparency where needed
- **SVG**: Master file for scalability
- **ICO**: Windows favicon (optional)

### Color Mode
- sRGB color space
- 8-bit color depth
- No transparency for iOS icons (solid background required)

### Safe Area
iOS automatically applies corner radius. Design within safe area:
- Corner radius is applied automatically
- Keep important elements 10% away from edges
- Test with Apple's App Icon template

---

## Implementation in Canva/Figma

### Canva Steps:
1. Create new design: 1024 × 1024 px
2. Set background: #00BFAE
3. Add shapes: Rounded rectangle → modify to shield shape
4. Add line: Use curve tool for pulse wave
5. Group and export at all required sizes

### Figma Steps:
1. Create frame: 1024 × 1024
2. Add rounded rectangle background
3. Use pen tool for shield path
4. Add wave using pen/curve
5. Create component, use variants for sizes
6. Export using Asset Export plugin

---

## File Delivery

Place all exported files in:
```
/bac-simulator-web/public/
├── icon-1024.png
├── icon-512.png
├── icon-192.png
├── icon-180.png
├── icon-167.png
├── icon-152.png
├── icon-120.png
├── icon-80.png
├── icon-76.png
├── icon-60.png
├── icon-58.png
├── icon-40.png
├── icon-29.png
├── icon-20.png
├── favicon-32.png
├── favicon-16.png
├── favicon.ico
├── logo.svg          (Master vector)
├── logo-full.svg     (Icon + wordmark)
└── logo-mono.svg     (Single color version)
```

---

## Reference Examples

Similar app icons for inspiration (style, not copy):
- Apple Health app (clean, minimal shield)
- Headspace (simple, friendly)
- Calm (soothing colors, minimal design)

---

## Contact

For questions about these specifications, refer to the main project documentation
or the design system in `/bac-simulator-web/tailwind.config.ts`.
