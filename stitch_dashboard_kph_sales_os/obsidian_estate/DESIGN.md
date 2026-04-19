# Design System Specification: High-End Real Estate Sales OS

## 1. Overview & Creative North Star: "The Architectural Ledger"
The objective of this design system is to transcend the "SaaS template" look and move into the realm of high-end editorial precision. We are building **"The Architectural Ledger"**—a space where the brutalist efficiency of real estate development meets the sophisticated, high-contrast clarity of a luxury stock exchange.

To achieve this, we reject the soft, rounded "bubbly" trends of modern web design. We embrace **sharp 0px radii**, **subtle 0.5px hairlines**, and a **monochromatic depth** punctuated by intense "Island Green" and "Stock Market" financial values. The layout is intentionally rigid and high-density, conveying authority and surgical precision for high-stakes sales environments.

---

## 2. Colors & Tonal Depth
This palette is rooted in deep obsidian tones, designed to make financial data and lead names pop with neon-like clarity.

### Primary Palette
- **Background (`surface`):** `#10141a` – The foundation. Deep, dark, and matte.
- **Cards (`surface_container`):** `#1c2026` – Used for primary content blocks.
- **Success (`primary`):** `#74daae` – The "Stock Market" green. Used exclusively for financial growth and positive conversion.
- **Urgent (`error`):** `#ffb4ab` – For overdue tasks and critical alerts.
- **Warmth (`secondary`):** `#e9c349` – Reserved for Lead Names and high-value "Gold" accents.

### The "Subtle Hairline" Rule
While the original request suggested no borders, we will implement **0.5px Ghost Borders** using `outline_variant` at 20% opacity. 
- **Rule:** Never use a 1px solid border. 
- **Execution:** Boundaries must be defined by the shift from `surface` to `surface_container_low`. If a separation is still required, use a 0.5px stroke to mimic the precision of an architectural blueprint.

### Surface Hierarchy & Nesting
Instead of shadows, we create "physicality" through value-shifting:
1.  **Level 0 (Base):** `surface` (`#10141a`)
2.  **Level 1 (Main Content):** `surface_container` (`#1c2026`)
3.  **Level 2 (In-Card Accents):** `surface_container_high` (`#262a31`)
4.  **Level 3 (Floating Sliders):** `surface_bright` (`#353940`)

---

## 3. Typography: Be Vietnam Pro
Optimized for high-density data and Hebrew RTL support. The type must feel "engineered."

| Role | Token | Size | Weight | Character Spacing |
| :--- | :--- | :--- | :--- | :--- |
| **Display** | `display-md` | 2.75rem | 700 (Bold) | -0.02em |
| **Headline** | `headline-sm` | 1.5rem | 600 (Semi) | -0.01em |
| **Lead Names** | `title-md` | 1.125rem | 600 (Semi) | 0.05em (Caps) |
| **Financials** | `title-lg` | 1.375rem | 700 (Bold) | 0.02em |
| **Body Mono** | `body-md` | 0.875rem | 400 (Reg) | 0 |
| **Micro Data** | `label-sm` | 0.6875rem | 500 (Med) | 0.03em |

**Typography Strategy:**
- **Lead Names:** Always use `secondary` (Gold) in `title-md` to signify high-value entities.
- **Financial Values:** Use `primary` (Green) with slightly increased weight to ensure they are the first thing the eye tracks.
- **RTL Optimization:** Ensure `Be Vietnam Pro` line-heights are increased by 15% for Hebrew characters to maintain legibility without crowding.

---

## 4. Elevation & Depth (Non-Shadow)
In this system, "Up" does not mean "Shadowed." It means "Lighter."

- **The Stacking Principle:** To lift an element (like a sliding panel), increase its surface brightness. A Left-side Sliding Panel should use `surface_bright` to visually sit "above" the `surface_container` center content.
- **The "Ghost Border":** For buttons and input fields, use `outline` at 0.5px. This provides a "sharp" edge that feels premium and intentional, rather than the "fuzzy" feel of shadows.
- **Interactive Glass:** For the 3-column layout, use a subtle `backdrop-blur` (12px) on the Left Sidebar Nav to allow the dark background tones to bleed through, creating an "Obsidian Glass" effect.

---

## 5. Components & Layout
The layout is a rigid 3-column structure: 
1. **Nav Sidebar (Narrow)**
2. **Center Content (Wide)** 
3. **Sliding Detail Panel (Medium)**

### Buttons
- **Primary:** `primary` background with `on_primary` (dark) text. Square corners (`0px`).
- **Secondary:** Transparent background, `secondary` (Gold) 0.5px ghost border.
- **States:** Hover should not "glow." Hover should simply shift the background color to the next tier higher (e.g., `primary` to `primary_fixed`).

### Input Fields
- **Style:** Underline only or 0.5px Ghost Border. 
- **Focus:** When focused, the bottom border shifts to `secondary_fixed` (Gold).
- **Text:** Input text for financial values should default to the "Stock Market Green" `primary` color.

### Cards & Lists
- **No Dividers:** Prohibit horizontal lines between list items. Use `spacing-4` (0.9rem) of vertical whitespace or a subtle background toggle (`surface_container` vs `surface_container_low`).
- **Financial Row:** Every financial row must include a "trend" indicator using the `0.5` spacing scale for tight, tactical alignment.

---

## 6. Do's and Don'ts

### Do
- **Do** use `0px` radius for everything. Sharp corners imply precision.
- **Do** use `secondary` (Gold) sparingly—only for Lead Names and key interactive accents.
- **Do** prioritize RTL flow; the user's eye should start at the top-right and move left, with the sliding panel appearing from the left.
- **Do** use the `px` (1px) and `0.5` (0.1rem) spacing tokens for tight, "Excel-style" data density.

### Don't
- **Don't** use standard "Success" greens. Use the specific `primary` (#74daae) which has a colder, more metallic "money" feel.
- **Don't** use 1px borders. If a line is needed, it must be 0.5px or a tonal shift.
- **Don't** use gradients. This is a flat, "high-fidelity" environment where color purity is paramount.
- **Don't** use `primary` (Green) for anything other than financial values or "Success" actions. Using it for navigation or headings dilutes the "Money" signal.