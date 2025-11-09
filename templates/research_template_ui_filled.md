# UI Best Practices Research Template (Improved)

Instruction for AI: produce a practical, evidence‑backed UI best practices guide tailored to this project and stack.

---

## Project Context
- Project: tr808-synth
- Description: Web application that emulates the classic Roland TR-808 drum machine using the Web Audio API. Provides a 16-step sequencer grid, playback controls, and visual step highlighting for drum pattern creation.
- Tech stack: TypeScript/Vanilla JavaScript, Web Audio API, CSS, HTML
- Domain: audio-synthesis, music production, drum machine
- Year: 2025

## Task
Create a comprehensive UI best‑practices guide for tr808-synth that is:
1) Current — relevant to 2025; mark deprecated/outdated UI patterns.
2) Specific — tailored to TypeScript/Vanilla JS + Web Audio API and music production domain.
3) Practical — include concrete CSS/HTML/JS code examples, design system tokens, UI component patterns.
4) Complete — cover design system, user experience, accessibility, responsive design, and visual design.

## Output Structure (Markdown)
### 1. TL;DR (≤10 bullets)
- **Design System**: CSS custom properties for consistent styling; use HSL colors for easy theming
- **Dark Theme Default**: Music apps use dark themes to reduce eye strain during long sessions
- **Grid-First**: 16-step sequencer as core UI element; step buttons need clear visual states
- **Responsive**: Desktop-first with tablet optimization; 1024px+ optimal width
- **Audio-Visual Sync**: Visual feedback must align precisely with audio timing
- **Performance**: 60fps animation for step highlighting; avoid layout thrashing during playback
- **Accessibility**: Focus states, keyboard navigation (arrow keys, spacebar for play/stop)
- **Visual Feedback**: Clear active/current step indicators with accent color glow
- **Theming**: CSS variables for easy light/dark mode switching
- **Component Pattern**: Custom sequencer grid, transport controls, instrument labels

### 2. Landscape — What's new in 2025 UI
For TypeScript/Vanilla JS:
- CSS Container Queries mature for responsive components
- CSS `@layer` for better cascade management
- Improved CSS nesting support (no need for preprocessors)
- `:has()` selector for better parent styling based on children state
- Subgrid for aligned layouts (limited support, use with fallbacks)

### 3. UI Architecture Patterns (2–4 for audio-synthesis with TypeScript/Vanilla JS)
Pattern A — [Vanilla JS Components with CSS Custom Properties] (MVP)
- When to use; Steps; Pros/Cons; Optional later features

**When**: Small application (<20 components), maximum performance, no build complexity.
**Steps**:
1. Create custom elements with classes (e.g., `SequencerGrid`, `TransportControls`)
2. Use CSS custom properties for theming and design consistency
3. Event delegation for grid interactions
4. CSS animations for visual feedback
**Pros**: Fast, small bundle, no framework overhead, direct DOM control
**Cons**: More manual code, no virtual DOM, less component lifecycle management
**Later**: Component libraries if complexity grows

Pattern B — [Modular Component Architecture] (Scale-up)
- When to use; Migration from A

**When**: UI complexity grows beyond 20-30 components, team collaboration required.
**How**: ES6 modules with clear interfaces; composition patterns; state management abstraction.
**Migrate from A**: Gradually introduce modules, maintain CSS custom properties approach.

### 4. Priority 1 — [Design System/Visual Design]
**Why** → Ensures consistent, professional appearance that feels like premium VST instrument; reduces visual clutter that interferes with music creation.
**Scope** → In: Color palette, typography, spacing, shadows, radii, visual states; Out: Animations, interactions (covered separately).
**Decisions**
- Use dark theme as default: `#1a1a1a` background, `#2a2a2a` panels, `#ff6b35` accent (TR-808 orange)
- Spacing system: `4px` base unit; `var(--space-xs: 4px, --space-sm: 8px, --space-md: 16px, --space-lg: 24px)`
- Typography: System sans-serif with clear hierarchy (`--font-size-xs: 11px` to `--font-size-xl: 20px`)
**Implementation outline**
1. Define CSS custom properties in `:root` and `[data-theme="light"]`
2. Create consistent component patterns (buttons, sliders, step indicators)
3. Apply to all UI elements (grid, controls, panels)
**Guardrails & SLOs**
- Consistent spacing using tokens (no hardcoded values); 4.5:1 contrast minimum; all interactive elements ≥44px touch target
**Failure modes → Recovery**
- Inconsistent styling → enforce tokens in code review
- Poor contrast → use contrast checker tools

### 5. Priority 1 — [User Experience/Interaction Design]
**Why** → Ensures intuitive music creation flow; reduces friction between musical ideas and the interface.
**Scope** → In: Sequencer grid interaction, transport controls, keyboard shortcuts; Out: Audio processing (domain concern).
**Decisions**
- Click to toggle steps; visual feedback immediate
- Spacebar for play/stop; arrow keys for navigation; 1-5 for instrument selection
- Visual step highlighting synchronized with audio (≤2ms drift)
- Smooth animations for state changes (≤150ms)
**Implementation**
1. Event delegation on grid container for step toggling
2. Keyboard event listeners for shortcuts
3. Visualizer component synchronized with audio scheduler
**Guardrails & SLOs**
- Keyboard shortcuts documented; consistent interaction patterns; <2ms visual/audio sync drift
**Failure modes**
- Unresponsive steps → optimize rendering, batch updates; desync → align with audio context time

### 6. Priority 2 — [Accessibility]
**Why** → Enables users with disabilities to create music; improves experience for power users with keyboard navigation.
**Scope** → In: Semantic HTML, ARIA labels, keyboard navigation, focus states; Out: Screen reader optimization (P3).
**Decisions**
- Semantic roles (`role="grid"`, `role="gridcell"` for sequencer)
- Proper focus management and keyboard navigation
- ARIA attributes for live regions (`aria-live="polite"` for BPM changes)
- High contrast focus indicators
**Implementation**
1. Add ARIA roles to grid elements
2. Implement keyboard navigation (tab order, arrow keys)
3. Focus-visible polyfill for consistent focus states
4. Screen reader announcements for state changes
**Guardrails & SLOs**
- Passes axe-core accessibility tests; keyboard navigation complete; focus indicators visible
**Failure modes**
- Poor keyboard nav → test with keyboard only; missing ARIA → use accessibility testing tools

### 7. Priority 3 — [Responsive Design]
**Why** → Enables use on multiple device sizes; tablet optimization for studio workflows.
**Scope** → In: Breakpoints, touch targets, layout adaptation; Out: Mobile-specific features.
**Decisions**
- Desktop-first: 1024px+ optimal width; tablet: 768px-1023px adaptation; no mobile optimization (P3)
- Grid columns adapt: 16-step remains fixed width, but rows wrap on narrow screens
- Touch targets: ≥44px minimum for mobile/touch use
**Implementation**
1. CSS Grid for main layout with flexible panels
2. Media queries at 1024px and 768px
3. Touch-friendly button sizes and spacing
**Guardrails & SLOs**
- All functions accessible at 768px width; no horizontal scrolling; touch targets ≥44px
**Failure modes**
- Overcrowded UI → hide non-essential controls; small touch targets → increase spacing

### 8. Design System & Visual Tokens (for TypeScript/Vanilla JS, Web Audio API)
**Color palettes**: 
```css
:root {
  /* Dark Theme */
  --color-bg-primary: #1a1a1a;
  --color-bg-secondary: #2a2a2a;
  --color-bg-tertiary: #333;
  --color-bg-elevated: #3a3a3a;
  --color-text-primary: #fff;
  --color-text-secondary: #aaa;
  --color-accent: #ff6b35; /* TR-808 Orange */
  --color-accent-hover: #ff8555;
  --color-success: #00ff00;
  --color-border: #444;
}
```

**Typography & Spacing**:
- `--font-family: system-ui, sans-serif`
- `--font-size-xs: 11px` to `--font-size-xl: 20px`
- `--space-xs: 4px` to `--space-xl: 32px`
- `--radius-sm: 2px` to `--radius-lg: 8px`

**Component patterns**: Reusable classes for buttons, sliders, step indicators, panels

### 9. Accessibility Best Practices
- **Semantic HTML**: Use proper elements (`<button>`, `<label>`, `<section>`)
- **ARIA roles**: `role="grid"` for sequencer, `role="gridcell"` for individual steps
- **Keyboard navigation**: Tab order, arrow key navigation, spacebar for activation
- **Focus management**: Visible focus indicators, logical tab flow
- **Screen reader support**: Proper labels, live regions for state changes
- **Color contrast**: Minimum 4.5:1 for normal text, 3:1 for large text

### 10. Performance & UX Responsiveness
- **Frame rate**: Maintain 60fps for visual feedback during playback
- **CSS optimization**: Use `transform` and `opacity` for animations; avoid layout thrashing
- **Batch updates**: Group DOM modifications during playback
- **Debounce/resist**: Input handling for sliders and controls
- **Critical CSS**: Inline above-fold styles
- **Interaction latency**: <100ms response to user input

### 11. Code Quality Standards for UI
- **CSS Architecture**: ITCSS/BEM methodology for maintainability
- **Naming convention**: BEM-style (`.component-name__element--modifier`)
- **Selector specificity**: Keep low; use classes primarily
- **CSS custom properties**: For all design tokens (colors, spacing, typography)
- **Component structure**: Clear separation of concerns (HTML structure, CSS styling, JS behavior)

### 12. Responsive & Cross-Platform Considerations
- **Breakpoint strategy**: `768px` (tablet), `1024px` (desktop optimal)
- **Touch vs. mouse**: Same interface but larger touch targets on touch devices
- **Cross-browser**: Support Chrome 90+, Firefox 88+, Safari 14+ (Web Audio API support)
- **Performance**: Optimize for mid-tier laptops during playback

### 13. Reading List (with dates and gists)
- [WebAIM Contrast Checker] (Last updated: 2024-10-15) — tool for verifying color contrast ratios
- [Smashing Magazine - Modern CSS Layouts] (2025-01-08) — guide to CSS Grid and Flexbox
- [MDN - Web Audio API] (2025-01-12) — audio timing and visual sync
- [A11Y Project] (2024-12-20) — accessibility best practices and patterns

### 14. Decision Log (ADR style)
- [ADR-001] **Dark theme default** over light theme because music apps typically use dark themes to reduce eye strain during long studio sessions
- [ADR-002] **CSS custom properties** for theming over CSS-in-JS or build-time variables because of simplicity and performance
- [ADR-003] **Semantic HTML with ARIA** over complex custom components because of accessibility and SEO considerations
- [ADR-004] **Event delegation** for grid instead of individual listeners to reduce memory usage during 16x12 grid interactions

### 15. Anti‑Patterns to Avoid
- **Layout thrashing** during playback → batch DOM updates, use `requestAnimationFrame`
- **Hardcoded values** instead of CSS custom properties → creates inconsistency and maintenance issues
- **Deeply nested selectors** → increases specificity conflicts and maintenance complexity
- **Inline styles** → prevents theming and systematic changes
- **Inconsistent spacing** → use spacing tokens system consistently
- **Insufficient touch targets** → ensure ≥44px for accessibility

### 16. Evidence & Citations
- Web Audio API precise timing: Use `AudioContext.getOutputTimestamp()` for audio-visual sync
- CSS performance: Stick to `transform` and `opacity` for animations (Browser rendering engines optimize these)
- Accessibility: Follow WCAG 2.2 AA guidelines for keyboard navigation and focus management
- Color contrast: Use 4.5:1 minimum for normal text to meet AA compliance

### 17. Verification
- **Self‑check scripts**:
  - Accessibility: Run axe-core browser extension on all UI states
  - Performance: Chrome DevTools Performance tab during playback 
  - Contrast: Use browser dev tools or WebAIM contrast checker
  - Keyboard nav: Navigate entire app with keyboard only
- **Confidence**: 
  - Visual design patterns — **High** (established music app conventions)
  - Accessibility guidelines — **High** (WCAG 2.2 standards)
  - Performance recommendations — **High** (browser best practices)
  - Responsive guidelines — **Medium** (device-specific optimizations may be needed)

## Requirements
1) No chain‑of‑thought. Provide final answers with short, verifiable reasoning.
2) If browsing is needed, state what to check and why; produce a provisional answer with TODOs.
3) Keep it implementable today; prefer defaults that reduce complexity.
4) Include specific CSS custom properties, design tokens, and component examples.

## Additional Context
{{ADDITIONAL_CONTEXT}}

---
Start the research now and produce the UI guide for tr808-synth.