# AerUla Design System

Design guidance for AerUla's web experience. AerUla is an AI-powered digital cultural village for exploring authentic Sri Lankan traditions. The design should feel premium, calm, trustworthy, and culturally warm.

## Brand Direction

AerUla visually combines Sri Lankan/Jaffna cultural warmth with modern digital-product clarity. It should feel:

- **Cultural**: Rooted in authentic Sri Lankan heritage without becoming a tourist poster.
- **Premium**: Clean, spacious, and intentional. Nothing cheap or cluttered.
- **Calm**: Warm tones, readable typography, generous whitespace.
- **Trustworthy**: Professional, consistent, and clear.
- **Modern**: Digital-first, responsive, fast.
- **Simple**: One idea per screen; clear user paths.

### Visual Inspiration (Principles Only)

- Google Arts & Culture: cultural, visual, educational, story-driven.
- Stripe: clean, premium, spacious, product-focused.

### Style to Avoid

- Overcrowded layouts.
- Too many colors.
- Tourist-poster clutter.
- Cheap-looking gradients.
- Heavy 3D before MVP.
- Too many animations.
- Overly playful game UI.

## Design Direction

AerUla should combine:

- **Image-led cultural discovery** inspired by editorial museum and archive experiences.
- **Clean product clarity** inspired by modern SaaS interfaces.
- **Lightweight simulation-first interaction** for mobile and desktop.
- **Short supporting text** with real cultural imagery carrying most of the page.

Do not copy any reference website directly. Use references only for design principles: clarity, spacing, hierarchy, strong content presentation, and polished interaction.

## Core Principles

- Simple first: every screen should have one clear purpose.
- Professional: use consistent spacing, typography, color, and button hierarchy.
- Cultural: visual choices should support Sri Lankan heritage without becoming decorative clutter.
- Relevant: hut, product, and simulation images must directly match the culture or object being presented.
- Fast: avoid heavy assets, excessive animation, and unnecessary JavaScript.
- Accessible: readable contrast, semantic HTML, visible focus states, and keyboard-friendly controls.
- Mobile first: design must work well on phones before desktop polish.

## Color System

### Brand Palette

Use this refined heritage-inspired palette:

- **Heritage Blue** (Primary Brand): `#083B8A` — Deep, trustworthy, cultural.
- **Deep Navy** (Dark Accent): `#061A40` — High contrast for text and strong elements.
- **Clay Sand** (Warm Accent): `#D9A86C` — Warm, earthy, cultural warmth.
- **Warm Ivory** (Background): `#FAF7F0` — Soft, readable, professional.
- **Palmyrah Green** (Secondary): `#2E7D5B` — Growth, learning, progress.
- **Sunset Gold** (Highlight): `#F2B84B` — Badges, achievements, warmth.

### Functional Colors

- **Charcoal Text**: `#1F2933` — Primary text, maximum contrast.
- **Muted Gray**: `#6B7280` — Secondary text, descriptions, metadata.
- **Border Gray**: `#E5E7EB` — Subtle borders, dividers, cards.
- **Success Green**: `#16A34A` — Positive states, validation.
- **Error Red**: `#DC2626` — Errors, warnings, destructive actions.
- **Off-White**: `#FFFFFF` — Cards, button backgrounds, paper surfaces.

### Usage

- **Heritage Blue** for primary buttons, links, and brand identity.
- **Deep Navy** for headings, navigation, and dark accents.
- **Clay Sand** for cultural warmth, background accents, and section dividers.
- **Palmyrah Green** for learning states, progress, and badges earned.
- **Sunset Gold** for achievement badges, highlights, and cultural items.
- **Charcoal** for all body text and primary content.
- **Muted Gray** for secondary labels, metadata, and descriptions.
- **Border Gray** for subtle dividers, card borders, and form fields.

Do not let the interface become dominated by one hue. Use Heritage Blue sparingly for navigation and primary actions. Let Warm Ivory dominate as the background. Use Clay Sand and Palmyrah Green as intentional accents.

## Typography

Use system fonts unless a brand font is intentionally added later.

```css
font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
```

### Type Scale

- Hero title: `clamp(2.5rem, 6vw, 5.25rem)` — Landing page, emotional, main call to action.
- Page heading: `clamp(2rem, 4vw, 3.5rem)` — Section headers, main page titles.
- Section heading: `1.75rem` to `2.5rem` — Sub-sections, card groups.
- Card heading: `1.1rem` to `1.25rem` — Individual card titles, hut names.
- Body text: `1rem` — Standard reading, descriptions, content.
- Small labels: `0.78rem` to `0.875rem` — Metadata, badges, helper text.

### Rules

- Keep letter spacing normal except small uppercase labels.
- Do not scale all text with viewport width.
- Use short headings and clear body copy.
- Avoid long paragraphs inside cards.
- Prioritize readability over visual drama.

## UI Language and Tone

AerUla's voice is welcoming, clear, and culturally respectful. Use short, action-oriented language.

### Recommended Actions and Labels

- "Explore the Village"
- "Enter the Hut"
- "Start Your Journey"
- "Continue Learning"
- "Ask the AI Guide"
- "Unlock Your Badge"
- "View Your Passport"
- "Browse Products"
- "Book a Real Experience"
- "Meet Local Hosts"
- "Share Your Story"

### Tone Examples

**Landing page hero:**
> Explore Sri Lanka beyond the surface.

**Supporting headline:**
> Discover authentic traditions through interactive cultural huts, guided by AI, and connect with real local experiences.

**Hut invitation:**
> Learn pottery from a master craftsperson. Shape clay, understand the tradition, earn your badge.

**Marketplace section:**
> Meet local artisans. Support authentic cultural products.

**AI Guide prompt:**
> What would you like to know about this tradition?

**Badge earned:**
> You've earned the Potter's Badge. Add it to your cultural passport.

### Tone Principles

- Respectful of Sri Lankan culture; not exoticizing or stereotyping.
- Educational without being condescending.
- Warm and inviting, not corporate.
- Action-oriented and clear.
- Celebrate learner progress and achievement.

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
- Short description only when the image and title are not enough.
- One primary action when needed.
- Avoid decorative-only icons.
- Include a relevant image for hut, product, booking, and simulation preview cards whenever available.

### Images

- Use images as first-class content, not decoration.
- Every hut must have a relevant image, alt text, and source credit.
- Product imagery should match the associated hut or product material.
- Simulation screens should show a real reference image next to the interactive SVG/HTML/Canvas surface.
- Avoid generic filler photos, unrelated craft photos, and images from the wrong cultural context when a closer Sri Lankan or Jaffna reference exists.
- Keep text short around image grids; use captions and action labels instead of long paragraphs.

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
- Large cultural photo stack plus lightweight visual preview of the virtual village.
- Three-step explanation: Discover, Interact, Connect.
- Gallery of relevant hut images.

### Virtual Village

Purpose: let users choose cultural huts and understand progress.

Required elements:

- Clear map or grid of huts.
- Image preview for the selected hut.
- States: locked, available, completed.
- Progress indicator.
- Mobile-friendly hut selection.
- No heavy 3D in MVP.

### Hut Experience

Purpose: teach, simulate, quiz, and convert.

Required elements:

- Story section.
- Media section.
- Mini simulation with a real reference image beside the interactive surface.
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
- Product or hut reference images on every product card.
- Hut/category filtering.
- Product detail page.
- Add-to-cart action.
- Clear stock and approval state.

## Simulation UX

- Simulations must be quick to understand.
- Use clear instructions but keep them short.
- Provide immediate feedback.
- Pair each simulation with a visible reference photo and a small interactive surface.
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
