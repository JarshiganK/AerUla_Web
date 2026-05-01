# AerUla Design System

Design guidance for AerUla's web experience. Keep the UI simple, professional, fast, and culturally warm.

## Design Direction

AerUla should combine:

- Cultural discovery inspired by editorial museum and archive experiences.
- Clean product clarity inspired by modern SaaS interfaces.
- Lightweight simulation-first interaction for mobile and desktop.

Do not copy any reference website directly. Use references only for design principles: clarity, spacing, hierarchy, strong content presentation, and polished interaction.

## Core Principles

- Simple first: every screen should have one clear purpose.
- Professional: use consistent spacing, typography, color, and button hierarchy.
- Cultural: visual choices should support Sri Lankan heritage without becoming decorative clutter.
- Fast: avoid heavy assets, excessive animation, and unnecessary JavaScript.
- Accessible: readable contrast, semantic HTML, visible focus states, and keyboard-friendly controls.
- Mobile first: design must work well on phones before desktop polish.

## Visual Style

### Personality

- Warm
- Trustworthy
- Educational
- Calm
- Premium but approachable

### Layout

- Use generous whitespace.
- Keep page sections full-width with constrained inner content.
- Avoid nested cards.
- Use cards only for repeated items, dashboard summaries, products, hut previews, and compact content groups.
- Prefer clean editorial sections over busy decorative layouts.

### Border Radius

- Default radius: `8px`
- Buttons and pills: `999px`
- Avoid overly rounded cards unless used for small badges or pills.

## Color System

Use a restrained palette. Do not let the interface become dominated by one hue.

### Core Colors

- Ink: `#111827`
- Muted text: `#5f6673`
- Paper: `#fffdf8`
- Warm background: `#f6efe3`
- Line: `#e7e3db`
- Heritage green: `#2f6f4f`
- Gold accent: `#c8923b`
- Deep blue accent: `#365b87`

### Usage

- Ink for primary text and dark buttons.
- Muted text for descriptions and secondary labels.
- Paper and warm background for page surfaces.
- Heritage green for cultural/learning state and positive progress.
- Gold for badges, achievements, and small highlights.
- Deep blue for secondary accents and informational states.

## Typography

Use system fonts unless a brand font is intentionally added later.

```css
font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
```

### Type Scale

- Hero title: `clamp(2.5rem, 6vw, 5.25rem)`
- Page heading: `clamp(2rem, 4vw, 3.5rem)`
- Section heading: `1.75rem` to `2.5rem`
- Card heading: `1.1rem` to `1.25rem`
- Body text: `1rem`
- Small labels: `0.78rem` to `0.875rem`

### Rules

- Keep letter spacing normal except small uppercase labels.
- Do not scale all text with viewport width.
- Use short headings and clear body copy.
- Avoid long paragraphs inside cards.

## Components

### Navigation

- Sticky top navigation is acceptable.
- Use simple links: Home, Virtual Village, Marketplace, Dashboard.
- Use one clear primary nav action: `Enter village`.
- Keep the logo compact and readable.

### Buttons

- Primary: dark filled button.
- Secondary: light or outlined button.
- Destructive actions should be rare and clearly labeled.
- Button text must be action-oriented.

Examples:

- `Enter Virtual Village`
- `Continue Journey`
- `Complete Hut`
- `Add to Cart`
- `Book Experience`

### Cards

Use cards for:

- Hut previews
- Product tiles
- Dashboard summaries
- Badge/passport items
- Booking rows or compact summaries

Card rules:

- One idea per card.
- Clear heading.
- Short description.
- One primary action when needed.
- Avoid decorative-only icons.

### Forms

- Use clear labels.
- Show validation errors near the field.
- Keep forms short.
- Use helper text only where it prevents mistakes.
- Never rely on placeholder text as the only label.

### Badges and Status

Use badges for:

- Completed
- Available
- Locked
- Pending approval
- Approved
- Cancelled

Status colors must be consistent across dashboards, hut pages, marketplace, and admin screens.

## Page Patterns

### Home Page

Purpose: explain AerUla quickly and guide users into the virtual village.

Required elements:

- Strong hero headline.
- Short value statement.
- Primary action to enter the village.
- Secondary action to browse marketplace.
- Lightweight visual preview of the virtual village.
- Three-step explanation: Discover, Interact, Connect.

### Virtual Village

Purpose: let users choose cultural huts and understand progress.

Required elements:

- Clear map or grid of huts.
- States: locked, available, completed.
- Progress indicator.
- Mobile-friendly hut selection.
- No heavy 3D in MVP.

### Hut Experience

Purpose: teach, simulate, quiz, and convert.

Required elements:

- Story section.
- Media section.
- Mini simulation.
- Quiz.
- Badge/progress result.
- Related bookings and products.

### Cultural Passport

Purpose: show achievement and next steps.

Required elements:

- Completed huts.
- Earned badges.
- Scores or completion quality.
- Recommended next hut.
- Future certificate/share action placeholder if needed.

### Marketplace

Purpose: connect cultural learning to host products.

Required elements:

- Product grid.
- Hut/category filtering.
- Product detail page.
- Add-to-cart action.
- Clear stock and approval state.

## Simulation UX

- Simulations must be quick to understand.
- Use clear instructions but keep them short.
- Provide immediate feedback.
- Make success/failure states understandable.
- Save progress only after server validation.
- Support touch, mouse, and keyboard where practical.
- Avoid continuous animation unless it directly improves the interaction.

## Accessibility

Minimum requirements:

- Semantic headings.
- Form labels.
- Alt text for meaningful images.
- Visible keyboard focus.
- Sufficient contrast.
- Buttons for actions, links for navigation.
- Do not communicate state with color alone.

## Performance

- Optimize images before using them.
- Lazy-load below-the-fold media.
- Keep JavaScript small and page-specific.
- Avoid loading simulation code on pages that do not need it.
- Use SVG/CSS for simple visuals.
- Use Canvas only when it provides real interaction value.
- Watch database query count on dashboards, passport, marketplace, and village pages.

## Frontend Deployment Direction

The planned production frontend is Vercel.

If a separate frontend is created:

- Prefer Next.js or React only when the project is ready for a separate frontend.
- Keep components small and reusable.
- Use environment-specific API URLs.
- Never expose backend secrets in client-side environment variables.
- Use preview deployments for review.
- Test critical user flows before production promotion.

## Do Not Do

- Do not copy Google Arts & Culture or Stripe directly.
- Do not add decorative complexity without product value.
- Do not introduce heavy 3D/VR/AR for the MVP.
- Do not create large generic component systems before repeated use exists.
- Do not ship rough placeholder UI for user-facing pages unless scaffolding is explicitly requested.
- Do not sacrifice performance for visual effects.
