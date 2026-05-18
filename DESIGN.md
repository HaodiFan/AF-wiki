---
version: alpha
name: AF Public Console
description: A dark, precise public interface for Anthony Fan's knowledge, fitness, and agent-system pages.
colors:
  primary: "#F4F1E8"
  secondary: "#A9A49A"
  tertiary: "#3DD6C6"
  neutral: "#080807"
  surface: "#11110F"
  surface-raised: "#171715"
  border: "#34332E"
  accent-green: "#66D37E"
  accent-blue: "#77A7FF"
  accent-amber: "#FFB454"
  accent-coral: "#FF6B5D"
  accent-gold: "#E6C55A"
  on-tertiary: "#06100F"
typography:
  h1:
    fontFamily: Inter
    fontSize: 4.5rem
    fontWeight: 650
    lineHeight: 0.98
    letterSpacing: "0px"
  h2:
    fontFamily: Inter
    fontSize: 3rem
    fontWeight: 620
    lineHeight: 1.05
    letterSpacing: "0px"
  h3:
    fontFamily: Inter
    fontSize: 1.125rem
    fontWeight: 620
    lineHeight: 1.2
    letterSpacing: "0px"
  body-md:
    fontFamily: Inter
    fontSize: 1rem
    fontWeight: 400
    lineHeight: 1.65
    letterSpacing: "0px"
  mono-label:
    fontFamily: JetBrains Mono
    fontSize: 0.75rem
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: "0px"
rounded:
  sm: 4px
  md: 8px
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 48px
  xxl: 96px
components:
  button-primary:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.on-tertiary}"
    rounded: "{rounded.md}"
    padding: 12px
  button-primary-hover:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.neutral}"
  panel:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    rounded: "{rounded.md}"
    padding: 24px
  panel-raised:
    backgroundColor: "{colors.surface-raised}"
    textColor: "{colors.primary}"
    rounded: "{rounded.md}"
    padding: 24px
  badge:
    backgroundColor: "{colors.surface-raised}"
    textColor: "{colors.secondary}"
    rounded: "{rounded.sm}"
    padding: 8px
  badge-border:
    backgroundColor: "{colors.border}"
    textColor: "{colors.primary}"
    rounded: "{rounded.sm}"
    padding: 8px
  badge-green:
    backgroundColor: "{colors.accent-green}"
    textColor: "{colors.neutral}"
    rounded: "{rounded.sm}"
    padding: 8px
  badge-blue:
    backgroundColor: "{colors.accent-blue}"
    textColor: "{colors.neutral}"
    rounded: "{rounded.sm}"
    padding: 8px
  badge-amber:
    backgroundColor: "{colors.accent-amber}"
    textColor: "{colors.neutral}"
    rounded: "{rounded.sm}"
    padding: 8px
  badge-coral:
    backgroundColor: "{colors.accent-coral}"
    textColor: "{colors.neutral}"
    rounded: "{rounded.sm}"
    padding: 8px
  badge-gold:
    backgroundColor: "{colors.accent-gold}"
    textColor: "{colors.neutral}"
    rounded: "{rounded.sm}"
    padding: 8px
---

## Overview

AF Public Console is a dark technical interface for the public layer of Anthony Fan's personal system. It should feel closer to a precise agent console than a portfolio page: structured, quiet, dense enough for scanning, and explicit about public/private boundaries.

The system borrows the discipline of Linear, the utility feel of Raycast, and the monospace clarity of OpenCode. It does not use decorative gradient blobs, oversized marketing cards, or generic dashboards.

## Colors

- **Neutral ({colors.neutral}):** Page canvas. Use near-black as the native medium, not as a theme slapped on top.
- **Surface ({colors.surface}):** Default panels, tables, and repeated items.
- **Surface Raised ({colors.surface-raised}):** Active nodes, featured links, and selected state containers.
- **Primary ({colors.primary}):** Main text. Warm off-white avoids harsh pure white.
- **Secondary ({colors.secondary}):** Metadata, explanatory copy, timestamps, and inactive nav.
- **Tertiary ({colors.tertiary}):** Main interaction color. Use sparingly for current route, links, and primary focus.
- **Accent Green / Blue / Amber / Coral / Gold:** Data categories only. They should help decode the system, not become background decoration.

## Typography

Use Inter for readable interface text and JetBrains Mono for labels, counters, routes, dates, and source IDs. Keep all letter spacing at `0px`; hierarchy comes from weight, size, spacing, and color.

Chinese and English copy should be short, direct, and operational. Avoid marketing-style adjectives in UI labels. Prefer nouns such as `Fitness`, `Knowledge`, `Boundary`, `Runtime`, `Source`.

## Layout

Use full-width page sections with constrained inner content. The hero may be split into a copy column and a system-map column. Repeated items can be cards, but page sections should not look like floating cards.

Spacing follows an 8px grid. Dense UI areas use 12-16px gaps; major sections use 72-96px vertical rhythm. Fixed-format elements such as charts, graph nodes, nav pills, and metric tiles must keep stable dimensions so text and hover states do not shift layout.

## Elevation & Depth

Depth is primarily border-based. Use one-pixel borders, inset highlights, and restrained shadows only where they improve legibility on dark surfaces. Avoid soft glowing orbs, background blobs, and decorative blur.

## Shapes

Use 4px for small controls and 8px for cards, panels, graph nodes, and buttons. Full pills are reserved for compact nav or status chips. Do not use large rounded marketing cards.

## Components

- `button-primary` is for one high-emphasis route or action.
- `panel` is for grouped information: charts, timelines, source boundaries, and public links.
- `panel-raised` is for selected or current nodes.
- `badge` is for route labels, counts, and source states.

## Do's and Don'ts

- **Do** make public/private boundaries visible near source links.
- **Do** keep fitness and knowledge as equally important operating areas.
- **Do** use data color accents consistently across charts, nodes, and tags.
- **Do** preserve GitHub Pages and GitHub Markdown constraints.
- **Don't** expose raw AF-wiki source documents, private notes, OCR text, or client details.
- **Don't** use generic SaaS dashboard cards, decorative gradients, or one-note blue/purple palettes.
- **Don't** add new claims about Anthony unless they already exist in the public repo context.
