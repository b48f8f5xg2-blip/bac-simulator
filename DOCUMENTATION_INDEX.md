# BAC Simulator - Documentation Index

**Date**: December 9, 2025
**Status**: Complete and Current
**Total Documentation**: 72 KB across 6 files

---

## Overview

This directory contains comprehensive documentation for the BAC Simulator project. The documentation has been structured specifically for rapid agent onboarding, knowledge preservation, and seamless multi-session development.

---

## Documentation Map

### 1. **PROJECT_CONTEXT.md** (34 KB) - START HERE
**Purpose**: Comprehensive project knowledge base

**Contents**:
- Executive summary and project overview
- Current state (commit fd59f62, status as of Dec 9, 2025)
- Design system specification (colors, layout, typography)
- Core algorithm explanation (Widmark equation, food absorption)
- Platform implementations (desktop Python + web TypeScript)
- Development patterns and workflow
- Technical decisions with rationale
- Performance characteristics
- Deployment and distribution
- File reference guide
- Quick reference for common tasks

**Best For**:
- Understanding overall project architecture
- Learning about design decisions
- Reference during implementation
- Onboarding new team members
- Understanding dual-platform considerations

**Read Time**: 25-30 minutes

**Key Sections**:
- "Architecture & Design System" - Visual and layout specs
- "Core Algorithm: Widmark Equation" - Mathematical foundation
- "Platform Implementations" - Detailed tech stack
- "File Reference Guide" - Where to find things

---

### 2. **AGENT_HANDOFF.md** (16 KB) - FOR AGENT COORDINATION
**Purpose**: Multi-agent development protocol and context transfer

**Contents**:
- Quick start checklist (5 minutes to productivity)
- Essential reading order
- Critical context checklist (verify understanding)
- Agent role matrix:
  - Testing agent responsibilities
  - Implementation agent workflow
  - Design/architecture agent tasks
  - Verification agent procedures
- Design system quick reference
- Common handoff scenarios with templates
- Debugging workflow for common issues
- Quality checklist before committing
- Session handoff protocol
- Command reference

**Best For**:
- New agents starting work on project
- Understanding role-specific responsibilities
- Knowing what to verify before committing
- Common problem diagnosis
- Context transfer between sessions

**Read Time**: 15-20 minutes

**Critical Sections**:
- "Quick Start for New Agents" - First steps
- "Agent Role Matrix" - What your role is
- "Quality Checklist for Commits" - Before pushing
- "Common Handoff Scenarios" - Pattern examples

---

### 3. **API_REFERENCE.md** (22 KB) - TECHNICAL REFERENCE
**Purpose**: Complete interface documentation with examples

**Contents**:
- TypeScript API reference:
  - All type definitions with examples
  - Calculation functions with signatures
  - Hook API documentation
  - Chatbot parser functions
- Python API reference:
  - BACCalculator class methods
  - Chatbot class methods
  - GUI class extension points
- Design system constants
- Algorithm constants (both platforms)
- Usage patterns with complete examples
- Error handling guide
- Performance considerations
- Testing checklist

**Best For**:
- Writing code that integrates with existing system
- Understanding available functions and types
- Copy-paste examples for common tasks
- Knowing what parameters functions expect
- Error handling requirements

**Read Time**: 20-25 minutes

**Critical Sections**:
- "TypeScript API Reference" - Web development
- "Python API Reference" - Desktop development
- "Usage Patterns & Examples" - Working code
- "Testing Checklist" - Verification steps

---

### 4. **CLAUDE.md** (6.3 KB) - PROJECT GUIDELINES
**Purpose**: Project-specific development guidelines (in codebase)

**Contents**:
- Project overview
- Color palette specification
- Desktop application structure
- Web application architecture
- Core algorithm (Widmark equation)
- Key constants table
- Food absorption impact reference
- Development guidelines
- File reference

**Best For**:
- Quick reference during coding
- Understanding color values
- Architecture overview
- Finding which file to edit

**Read Time**: 5-10 minutes

**When to Use**:
- Every coding session start
- Color values reference
- Architecture questions
- File location questions

---

### 5. **LOGO_DESIGN_SPECS.md** (6.6 KB) - DESIGN SPECIFICATIONS
**Purpose**: Logo and icon design guidelines

**Contents**:
- Logo design specifications
- Icon guidelines
- Color application rules
- Typography usage
- Deployment specifications

**Best For**:
- Visual design decisions
- Icon creation guidelines
- Logo specifications

**Read Time**: 10 minutes

---

### 6. **UPDATE_SUMMARY.md** (6.3 KB) - RECENT CHANGES
**Purpose**: Summary of recent work (maintained from previous session)

**Contents**:
- Recent updates and fixes
- Known working features
- Potential issues noted

**Best For**:
- Understanding what changed recently
- What was attempted
- What still needs work

**Read Time**: 5 minutes

---

## Reading Order by Role

### For Testing Agents
1. **AGENT_HANDOFF.md** - Understand testing responsibilities
2. **PROJECT_CONTEXT.md** - "Current State" section
3. **API_REFERENCE.md** - "Testing Checklist"
4. Start testing with scenarios from API_REFERENCE

**Time**: ~30 minutes

### For Implementation Agents
1. **AGENT_HANDOFF.md** - Understand role and workflow
2. **PROJECT_CONTEXT.md** - "Platform Implementations"
3. **API_REFERENCE.md** - Function signatures and examples
4. **CLAUDE.md** - Quick reference
5. Review relevant source files
6. Begin implementation

**Time**: ~45 minutes

### For Design/Architecture Agents
1. **PROJECT_CONTEXT.md** - Full document
2. **CLAUDE.md** - Guidelines
3. **LOGO_DESIGN_SPECS.md** - Visual specifications
4. Review recent commits
5. Plan changes with cross-platform consideration

**Time**: ~40 minutes

### For Verification Agents
1. **AGENT_HANDOFF.md** - Verification responsibilities
2. **API_REFERENCE.md** - Testing checklist
3. **PROJECT_CONTEXT.md** - Current state
4. Run test scenarios
5. Verify both platforms

**Time**: ~35 minutes

---

## Quick Navigation

### By Topic

#### Colors & Design
- **PROJECT_CONTEXT.md** → "Architecture & Design System"
- **CLAUDE.md** → "Color Palette"
- **API_REFERENCE.md** → "Design System Constants"

#### Algorithm & Calculation
- **PROJECT_CONTEXT.md** → "Core Algorithm: Widmark Equation"
- **CLAUDE.md** → "Core Algorithm"
- **API_REFERENCE.md** → "Calculation Functions"

#### File Locations
- **PROJECT_CONTEXT.md** → "File Reference Guide"
- **CLAUDE.md** → "Files Reference"
- **AGENT_HANDOFF.md** → "Platform-Specific Details"

#### Development Workflow
- **AGENT_HANDOFF.md** → "Agent Role Matrix"
- **PROJECT_CONTEXT.md** → "Development Workflow & Patterns"
- **API_REFERENCE.md** → "Usage Patterns & Examples"

#### Deployment
- **PROJECT_CONTEXT.md** → "Deployment & Distribution"
- **AGENT_HANDOFF.md** → "Commands Reference"

#### Testing
- **AGENT_HANDOFF.md** → "Common Handoff Scenarios"
- **API_REFERENCE.md** → "Testing Checklist"
- **PROJECT_CONTEXT.md** → "Testing Methodology"

---

## Key Information at a Glance

### Project Status
- **Current Commit**: fd59f62 (Complete redesign of desktop GUI to match web app)
- **Status**: Feature complete, both apps fully functional
- **Last Updated**: December 9, 2025
- **Known Bugs**: None critical

### Platform Details

#### Web App
- **Technology**: Next.js 15 + React 19 + TypeScript
- **Path**: `bac-simulator-web/`
- **Key File**: `lib/bac-calculator.ts`
- **Start**: `npm run dev` (localhost:3000)

#### Desktop App
- **Technology**: Python 3.9+ + Tkinter
- **Path**: `BAC_Simulator.app/`
- **Key File**: `Contents/Resources/gui.py`
- **Start**: `open BAC_Simulator.app` or `python3 gui.py`

### Core Algorithm
- **Name**: Modified Widmark Equation
- **Formula**: `Peak BAC = (A × 5.14) / (W × r) × (1 - food_factor)`
- **Elimination**: 0.015%/hour
- **Legal Threshold**: 0.08% (DUI)
- **Male Ratio**: 0.73 | **Female Ratio**: 0.66

### Colors (Always Use These Hex Values)
- Primary: `#00BFAE` | Secondary: `#004040` | Neutral: `#BFBEBE`
- Accent: `#029922` | Slate: `#4A4A63`
- Safe: `#029922` | Caution: `#F59E0B` | Warning: `#F97316`
- Danger: `#EF4444` | Critical: `#991B1B`

### Important Constants
- Update Rate: 2 seconds
- Timeline: 6 hours forward
- Food Types: 7 (empty stomach to high-fat meal)
- Drink Types: 9 (light beer to spirits)
- Impairment Levels: 7 (sober to extreme intoxication)

---

## Update Protocol

### When Documentation Changes
1. Update relevant markdown files
2. Update related source files in sync
3. Update CLAUDE.md if guidelines change
4. Commit with clear message referencing which docs changed
5. Update version number at end of each documentation file

### When Code Changes
1. Review if documentation needs updating
2. Check PROJECT_CONTEXT.md current state section
3. Update API_REFERENCE.md if interfaces change
4. Note changes in git commit message

### When Architecture Changes
1. Update PROJECT_CONTEXT.md architecture sections
2. Update AGENT_HANDOFF.md patterns
3. Update CLAUDE.md guidelines
4. Create new documentation if needed

---

## File Statistics

| File | Size | Lines | Purpose |
|------|------|-------|---------|
| PROJECT_CONTEXT.md | 34 KB | 850+ | Comprehensive knowledge base |
| AGENT_HANDOFF.md | 16 KB | 450+ | Multi-agent coordination |
| API_REFERENCE.md | 22 KB | 700+ | Technical interface reference |
| CLAUDE.md | 6.3 KB | 200 | Project guidelines (checked in) |
| LOGO_DESIGN_SPECS.md | 6.6 KB | 200 | Design specifications |
| UPDATE_SUMMARY.md | 6.3 KB | 200 | Recent changes log |
| **Total** | **91 KB** | **2,600+** | Complete documentation |

---

## Maintenance Schedule

### Weekly
- Review PROJECT_CONTEXT.md current state
- Update if any major changes
- Verify all links are valid

### Per Commit
- Update relevant documentation
- Include doc changes in commit message
- Verify consistency between files

### Per Major Feature
- Update PROJECT_CONTEXT.md architecture
- Update API_REFERENCE.md if interfaces changed
- Update AGENT_HANDOFF.md if patterns changed

---

## Success Criteria for Documentation

This documentation achieves the following goals:

✓ **Rapid Onboarding** (< 1 hour to productivity)
✓ **Knowledge Preservation** (complete without source reading)
✓ **Context Transfer** (seamless between sessions)
✓ **API Clarity** (examples for common tasks)
✓ **Pattern Recognition** (successful workflows documented)
✓ **Consistency** (design system and algorithm synced)
✓ **Troubleshooting** (debugging workflow included)
✓ **Quality Assurance** (checklists before commit)

---

## Feedback & Improvements

If you find gaps in documentation:
1. Note what's missing
2. Note where you looked (which file)
3. Document what you learned
4. Suggest addition to relevant file
5. Update documentation accordingly

This living documentation improves with each session.

---

## Version History

| Version | Date | Created By | Changes |
|---------|------|-----------|---------|
| 1.0 | Dec 9, 2025 | Claude (AG) | Initial comprehensive documentation |

---

## Quick Links to Key Sections

**Getting Started**:
1. AGENT_HANDOFF.md - "Quick Start for New Agents"
2. PROJECT_CONTEXT.md - "Executive Summary"
3. CLAUDE.md - "Project Overview"

**Development**:
1. API_REFERENCE.md - "Usage Patterns & Examples"
2. PROJECT_CONTEXT.md - "Development Workflow & Patterns"
3. AGENT_HANDOFF.md - "Quality Checklist for Commits"

**Reference**:
1. API_REFERENCE.md - "TypeScript API Reference" / "Python API Reference"
2. PROJECT_CONTEXT.md - "File Reference Guide"
3. CLAUDE.md - "Color Palette"

**Debugging**:
1. AGENT_HANDOFF.md - "Debugging Workflow"
2. PROJECT_CONTEXT.md - "Technical Decisions & Rationale"
3. API_REFERENCE.md - "Error Handling"

---

**Last Updated**: December 9, 2025
**Maintainer**: AI Development Team
**Status**: Complete and Current
**Next Review**: After major feature addition or significant changes

This documentation enables BAC Simulator to maintain consistency, quality, and clarity across all development activities. Use it, update it, and help it grow!
