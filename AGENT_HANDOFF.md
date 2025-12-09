# BAC Simulator - Agent Handoff & Coordination Protocol

**Version**: 1.0
**Date**: December 9, 2025
**Purpose**: Enable seamless context transfer between AI agents across sessions

---

## Quick Start for New Agents

### Essential Reading Order

1. **Start here**: Read this file (5 min)
2. **Project overview**: Read `PROJECT_CONTEXT.md` (20 min)
3. **Technical guidelines**: Read `CLAUDE.md` (10 min)
4. **Code inspection**: Review key files listed below (10 min)
5. **Implementation**: Begin task

### Fastest Path to Productivity

```bash
# 1. Understand the project structure
ls -la /Users/collinbird/Projects/My-Project-Hub/projects/bac-simulator/

# 2. Check current git status
cd /Users/collinbird/Projects/My-Project-Hub/projects/bac-simulator/
git status

# 3. Review recent changes
git log --oneline -5

# 4. Test current state
open BAC_Simulator.app  # or run web app

# 5. Read documentation
cat CLAUDE.md
cat PROJECT_CONTEXT.md
```

---

## Critical Context Checklist

Before beginning ANY work on this project, verify:

- [ ] **Color System Understood**: 7 core colors (Primary Teal #00BFAE, etc.)
- [ ] **Algorithm Known**: Widmark equation with food absorption modeling
- [ ] **Architecture Clear**: 3-column layout across both platforms
- [ ] **Dual Implementation**: Python desktop + TypeScript web
- [ ] **Design System**: Single source of truth for colors/layout
- [ ] **Constants Synced**: Same values in both Python and TypeScript
- [ ] **Testing Method**: Manual scenario-based testing (no automated tests)

**Verification**:
- Run: `python3 BAC_Simulator.app/Contents/Resources/gui.py`
- See: 3-column layout with header and footer
- Test: Add profile + drinks + food, verify BAC calculation
- Web: `cd bac-simulator-web && npm run dev`, verify same layout

---

## Agent Role Matrix

### Testing Agent Tasks

**Responsibility**: Identify bugs, document issues, verify fixes

**Workflow**:
1. Test both apps with standard scenarios
2. Document any bugs or inconsistencies
3. Note pattern of failures (e.g., "colors not matching")
4. Provide detailed reproduction steps
5. Suggest fixes based on observations

**Success Criteria**:
- Both apps run without crashes
- Calculations match expected values
- Visual design consistent between platforms
- All BAC statuses display correctly
- Color system applied uniformly

**Key Test Scenarios**:
- Empty stomach + 2 beers
- Full meal + 1 drink
- Multiple drinks over 3 hours
- Verify peak BAC calculation
- Verify timeline accuracy
- Test color transitions at thresholds

### Implementation Agent Tasks

**Responsibility**: Write code, fix bugs, implement features

**Workflow**:
1. Review bug report from testing agent
2. Analyze code to understand issue
3. Design fix (maintain parity across platforms)
4. Implement in one platform, then mirror to other
5. Test and commit with clear message

**Success Criteria**:
- Code compiles/runs without errors
- Fixes address root cause (not just symptoms)
- Both platforms updated in parallel
- Commit message references what was fixed
- Code follows existing style conventions

**Code Change Pattern**:
```
1. Modify web app (TypeScript first)
   - Update component or lib file
   - Test with `npm run build`
   - Verify `npm run lint` passes

2. Mirror to desktop app (Python second)
   - Apply same logic
   - Maintain color system consistency
   - Test with `python3 gui.py`

3. Commit
   - Message: "Fix: [description]" + "Fixes #X"
   - Mention both platforms if changes in both
```

### Design/Architecture Agent Tasks

**Responsibility**: Plan features, ensure consistency, manage technical debt

**Workflow**:
1. Review feature request or architectural issue
2. Analyze impact on both platforms
3. Design consistent solution
4. Document in CLAUDE.md if guidelines change
5. Create implementation plan for other agents

**Success Criteria**:
- Design preserves 3-column layout
- Changes consistent across both platforms
- No new external dependencies
- Maintains educational focus
- Follows existing patterns

**Key Principles**:
- Design system is single source of truth
- Algorithm logic stays synchronized
- Code duplication acceptable (platform-specific)
- Platform-specific optimizations allowed (SVG vs Canvas)

### Verification Agent Tasks

**Responsibility**: Validate fixes, ensure quality, run comprehensive tests

**Workflow**:
1. Review implementation against requirements
2. Run comprehensive test suite
3. Verify both platforms work identically
4. Check edge cases and boundary conditions
5. Document any remaining issues

**Success Criteria**:
- No regressions (new bugs introduced)
- Calculation accuracy maintained
- Visual consistency across platforms
- Performance acceptable
- Edge cases handled gracefully

---

## Design System Reference (Quick)

### Colors

```
Primary Teal:        #00BFAE  (buttons, highlights)
Dark Teal:           #004040  (header, dark bg)
Light Neutral:       #BFBEBE  (cards, borders)
Green Accent:        #029922  (success, safe BAC)
Dark Slate:          #4A4A63  (text, body)
Neutral Background:  #F3F4F6  (app bg)
White:               #FFFFFF  (cards, light text)

BAC Safe:            #029922
BAC Caution:         #F59E0B
BAC Warning:         #F97316
BAC Danger:          #EF4444
BAC Critical:        #991B1B
```

### Layout

```
[Header - Dark Teal #004040]
[Logo B] [Title] [Reset Button]

[3-Column Content]
[Profile + Log] [BAC + Timeline] [Chat]

[Footer - Disclaimer]
```

### Font Sizes

- Large BAC: 72px bold
- Titles: 16-18px bold
- Body text: 13px regular
- Small text: 10-11px

---

## Common Handoff Scenarios

### Scenario 1: "Fix Visual Bug"

**Previous Agent**: Testing agent reports color mismatch in BAC display

**Handoff Document**:
```
BUG: BAC display shows yellow (#F59E0B) but should show teal (#00BFAE)

REPRODUCTION:
1. Add 2 beers on empty stomach
2. Wait 30 minutes
3. Observe BAC around 0.06%
4. Expected: Green accent color #029922
5. Actual: Wrong color displayed

LOCATION: BACDisplay.tsx (web) and gui.py (desktop)

LIKELY CAUSE: Color constant mismatch between platforms

PRIORITY: High (visual inconsistency)
```

**Implementation Agent**:
1. Check `tailwind.config.ts` for color definition
2. Verify `IMPAIRMENT_LEVELS` in `lib/types.ts`
3. Check desktop `gui.py` color mapping
4. Ensure all three match
5. Test and commit

### Scenario 2: "Port Web Feature to Desktop"

**Previous Agent**: Feature implemented successfully on web app

**Handoff Document**:
```
FEATURE: Chronic drinker toggle added to ProfileForm

CHANGES MADE:
- Modified ProfileForm.tsx to include checkbox
- Updated useBACCalculator to apply 0.05 adjustment to Widmark ratio
- Tested with male/female profiles

NEED: Same feature in desktop app

FILES TO MODIFY:
- gui.py: Add checkbox to profile card
- bac_calculator.py: Add chronic_drinker logic
```

**Implementation Agent**:
1. Read web implementation in ProfileForm.tsx
2. Understand logic change in bac_calculator.ts
3. Create equivalent in Python
4. Test with same scenarios
5. Commit with note referencing web version

### Scenario 3: "Fix Algorithm Bug"

**Previous Agent**: Testing agent found BAC calculation error

**Handoff Document**:
```
BUG: Peak BAC calculation doesn't account for food absorption properly

TEST CASE: 2 beers + full meal
- Expected peak: 0.12 * (1 - 0.45) = 0.066%
- Actual peak: 0.12%

ROOT CAUSE: Food absorption factor not being applied in peak calculation

ALGORITHM REFERENCE:
Peak BAC = (A × 5.14) / (W × r) * (1 - food_factor)

FILES TO FIX:
- bac_calculator.ts (web)
- bac_calculator.py (desktop)
```

**Implementation Agent**:
1. Review Widmark equation in bac-calculator.ts
2. Find peak calculation function
3. Add food absorption factor multiplication
4. Mirror fix to Python
5. Test with multiple food types
6. Commit with clear message

---

## State of the Project (Current)

### Latest Commit
```
fd59f62 - Complete redesign of desktop GUI to match web app
```

### Current Status
- Both applications fully functional
- Desktop and web apps have visual parity
- Algorithm synchronized across platforms
- All core features implemented
- Test suite (manual) completed successfully

### Known Working Features
- User profile input (sex, weight, height, age)
- Drink selection with alcohol content
- Food selection with absorption modeling
- Real-time BAC calculation
- 6-hour timeline projection
- Color-coded status indicators
- Chat interface with natural language parsing
- Consumption history logging

### No Known Critical Bugs
- All core calculations verified
- Visual design consistent
- Both platforms stable
- Color system implemented
- Layout responsive

---

## Platform-Specific Details

### Web App

**Path**: `/Users/collinbird/Projects/My-Project-Hub/projects/bac-simulator/bac-simulator-web/`

**Key Files**:
- `app/page.tsx` - Main page
- `lib/bac-calculator.ts` - Calculation engine (ALWAYS SYNC WITH PYTHON)
- `lib/types.ts` - Data types + constants (SINGLE SOURCE OF TRUTH)
- `components/BACDisplay.tsx` - BAC display logic
- `components/TimelineChart.tsx` - Chart rendering
- `tailwind.config.ts` - Design system (TRUTH FOR COLORS)

**Commands**:
```bash
cd bac-simulator-web

npm install       # First time setup
npm run dev       # Development server (localhost:3000)
npm run build     # Production build
npm run lint      # Check TypeScript
npm run start     # Serve production build

# Open in browser: http://localhost:3000
```

**Testing**:
```bash
npm run build     # Verify TypeScript compiles
npm run lint      # Check for errors
# Manual test in browser
```

### Desktop App

**Path**: `/Users/collinbird/Projects/My-Project-Hub/projects/bac-simulator/BAC_Simulator.app/`

**Key Files**:
- `Contents/Resources/gui.py` - Main GUI (ALWAYS MATCH WEB LAYOUT)
- `Contents/Resources/bac_calculator.py` - Calculation engine (ALWAYS SYNC WITH TYPESCRIPT)
- `Contents/Resources/chatbot.py` - NLP parsing
- `Contents/MacOS/BAC_Simulator` - Launcher script

**Commands**:
```bash
# Run as app
open /Users/collinbird/Projects/My-Project-Hub/projects/bac-simulator/BAC_Simulator.app

# Run directly
python3 /Users/collinbird/Projects/My-Project-Hub/projects/bac-simulator/BAC_Simulator.app/Contents/Resources/gui.py

# Check Python syntax
python3 -m py_compile BAC_Simulator.app/Contents/Resources/gui.py
```

**Testing**:
```bash
python3 -m py_compile gui.py  # Syntax check
# Manual test: Run app, test scenarios
```

---

## Quality Checklist for Commits

Before committing any changes:

- [ ] **Both platforms tested**: Web and desktop app run without crashes
- [ ] **Calculations match**: Same inputs produce same BAC values
- [ ] **Visual consistency**: Design system colors applied correctly
- [ ] **No regressions**: All previous features still work
- [ ] **Code follows style**: Matches existing code in file
- [ ] **Constants synchronized**: Same values in Python + TypeScript
- [ ] **Commit message clear**: Describes what changed and why
- [ ] **No debug code**: No console.logs, print statements left
- [ ] **No unused imports**: Clean import statements
- [ ] **Colors use constants**: Not hardcoded hex values

**Commit Message Template**:
```
[Type]: [Brief description]

[Longer explanation if needed]

[Platform notes]:
- Web: [changes to TypeScript/React]
- Desktop: [changes to Python/Tkinter]

Fixes #[issue] if applicable
```

---

## Debugging Workflow

### Issue: "Colors not matching between web and desktop"

**Debug Steps**:
1. Check `tailwind.config.ts` for color definition
2. Check `gui.py` color dictionary
3. Compare hex values (should be identical)
4. Check component/widget using the color
5. Verify color is being applied (not overridden)

### Issue: "BAC calculation differs between platforms"

**Debug Steps**:
1. Use identical test inputs (profile + drinks + food)
2. Check Widmark ratio logic in both
3. Verify food absorption factor is applied
4. Check elimination rate constant (0.015)
5. Trace calculation step-by-step on paper
6. Compare intermediate values

### Issue: "Layout doesn't match between platforms"

**Debug Steps**:
1. Check column widths in both apps
2. Verify padding/margins match
3. Check font sizes (should be proportional)
4. Verify responsive behavior
5. Compare screenshots side-by-side

---

## Performance Notes

### Update Rate: 2 Seconds

Both platforms recalculate BAC every 2 seconds:
- **Why 2s**: Balances responsiveness with CPU efficiency
- **Change only if**: Performance issues or UX feedback
- **Implementation**: `useEffect` interval (web) or `after()` (desktop)

### No Optimization Needed If:
- App responds immediately to user input
- No lag when scrolling or updating
- CPU usage < 10% at idle

### Optimize If:
- Calculation takes > 100ms
- Excessive re-renders (web)
- Canvas redraws lag (desktop)

---

## Important Constraints

1. **No external dependencies**: Desktop app uses only stdlib
2. **No external APIs**: All computation is local
3. **Algorithm fidelity**: Must match Widmark equation exactly
4. **Design system**: Colors are standardized, not changeable per component
5. **Educational focus**: Calculations accurate, warnings clear
6. **Both platforms**: Changes usually need parity

---

## Session Handoff Protocol

### At End of Session, Future Agent Should:

1. **Document state**:
   - What's working
   - What's not working
   - What was attempted
   - What needs next

2. **Update this file** with:
   - New known issues
   - New patterns discovered
   - Lessons learned
   - Next recommended tasks

3. **Commit changes**:
   - Include summary in commit message
   - Reference any related issues

4. **Update git status**:
   - Leave repository in clean state
   - All files committed or documented

### Example Handoff at End of Session

**Previous Agent's Final Note**:
```
SESSION SUMMARY (Dec 9, 2025)

COMPLETED:
✓ Desktop GUI redesigned to match web app
✓ 3-column layout implemented
✓ Color system verified
✓ Font hierarchy implemented
✓ All core features tested and working

IN PROGRESS:
- None currently

NEXT STEPS:
1. Add animation when drinks added
2. Implement data persistence (save/load)
3. Add comparison mode for different scenarios
4. Create unit test suite

NOTES:
- Tkinter color rendering requires hex values, not color names
- Canvas coordinates have (0,0) at top-left, not bottom-left
- React re-renders can be optimized with useMemo if performance needed
- Python version pinned to 3.9+ for compatibility

ISSUES DISCOVERED:
- Tkinter on macOS can have DPI scaling issues (minor)
- No critical bugs remaining

TIME SPENT: 4 hours
```

---

## Quick Reference: Common Commands

```bash
# Web App
cd /Users/collinbird/Projects/My-Project-Hub/projects/bac-simulator/bac-simulator-web/
npm run dev              # Start dev server
npm run build            # Build for production
npm run lint             # Check TypeScript
npm run start            # Serve production

# Desktop App
cd /Users/collinbird/Projects/My-Project-Hub/projects/bac-simulator/
python3 BAC_Simulator.app/Contents/Resources/gui.py  # Run
python3 -m py_compile BAC_Simulator.app/Contents/Resources/gui.py  # Check syntax

# Git
git status               # Check what changed
git log --oneline        # See recent commits
git diff                 # See changes in detail
git add .               # Stage all changes
git commit -m "message" # Commit with message
git push                # Push to remote (if needed)

# View files
cat CLAUDE.md            # Project guidelines
cat PROJECT_CONTEXT.md   # Comprehensive context
cat AGENT_HANDOFF.md     # This file
```

---

## Contact/Context References

**Project Location**:
`/Users/collinbird/Projects/My-Project-Hub/projects/bac-simulator/`

**Main Documentation**:
- `CLAUDE.md` - Guidelines and architecture
- `PROJECT_CONTEXT.md` - Comprehensive project knowledge
- `AGENT_HANDOFF.md` - This file (agent coordination)

**Key Files**:
- Web: `/bac-simulator-web/lib/bac-calculator.ts`
- Desktop: `/BAC_Simulator.app/Contents/Resources/bac_calculator.py`
- Types: `/bac-simulator-web/lib/types.ts`
- Design: `/bac-simulator-web/tailwind.config.ts`

---

## Version History

| Version | Date       | Changes |
|---------|-----------|---------|
| 1.0     | Dec 9, 2025 | Initial comprehensive handoff document |

---

**This document is designed for rapid agent onboarding. Start with the checklist, read PROJECT_CONTEXT.md, then begin work. Reference this file during implementation for patterns and protocols.**
