# Wa Node Browser Extension MVP

[日本語版](README_ja.md)

This folder contains a minimal browser extension prototype for applying the **Artificial Wisdom Guardrail Note** as an optional user-controlled browser layer.

The extension is designed for Chromium-based browsers such as Chrome and Microsoft Edge.

---

## Core Principle

This extension must remain **user-controlled**.

It must not:

- install itself automatically,
- analyze pages without user action,
- send page content to external AI services by default,
- modify web pages silently,
- claim scientific proof or certification.

It may:

- open a side panel when the user clicks the extension icon,
- read the currently active page only after the user clicks **Analyze current page**,
- run local rule-based checks based on the six principles,
- generate a copyable Artificial Wisdom Guardrail Note,
- help users interpret public pages through the lens of Natural Law, Harmony, Circulation, Structure, Order, and Wa.

---

## What This MVP Does

The MVP provides:

1. A browser side panel.
2. A manual **Analyze current page** button.
3. Local extraction of title, URL, headings, and visible text from the active tab.
4. A simple rule-based six-principle check.
5. A local misunderstanding-risk checklist.
6. A copyable Artificial Wisdom Guardrail Note.

No AI API is used in this MVP.

---

## Folder Structure

```text
browser-extension/
├── README.md
├── README_ja.md
├── PRIVACY.md
├── manifest.json
├── background.js
├── sidepanel.html
├── sidepanel.js
└── sidepanel.css
```

---

## Manual Installation for Development

1. Open Chrome or Edge.
2. Go to `chrome://extensions` or `edge://extensions`.
3. Enable **Developer mode**.
4. Click **Load unpacked**.
5. Select the `browser-extension/` folder.
6. Click the extension icon to open the side panel.
7. Press **Analyze current page** only when you want the current page to be checked.

The extension is not distributed or installed automatically.

---

## Safety Model

This MVP uses only local browser-side logic.

- No external network requests.
- No API keys.
- No background page scraping.
- No automatic analysis on page load.
- No automatic page modification.
- No telemetry.

The extension requires user action before analyzing a page.

---

## Future Optional AI Mode

A future version may add optional AI analysis, but only if all of the following are true:

1. The user explicitly enables AI mode.
2. The user chooses the provider or local model.
3. The extension clearly shows what content will be sent.
4. The user confirms before sending.
5. The local-only mode remains available.

---

## Related Portal Documents

- [Artificial Wisdom Guardrail Note](../docs/AW_GUARDRAIL_NOTE.md)
- [Core Concepts](../docs/CORE_CONCEPTS.md)
- [Comparative Role Analysis](../docs/COMPARATIVE_SIMULATION.md)
- [Natural Complementary Science](../docs/NATURAL_COMPLEMENTARY_SCIENCE.md)
