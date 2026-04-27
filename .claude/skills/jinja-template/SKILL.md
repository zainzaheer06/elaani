---
name: jinja-template
description: Create or edit a Jinja template (page or component) for PureSignage. Use when adding a new dashboard page, customer page, admin page, or shared component. Ensures the template inherits the right base, uses brand color tokens, wraps strings in gettext, and supports RTL.
---

# Adding/editing a Jinja template

## Pick the right base layout

Every page must `{% extends %}` one of these — don't create a new base.

| Base | Used by | When |
|---|---|---|
| `base.html` | Vendor sidebar pages (`dashboard.html`, `inventory.html`, `bookings.html`, etc.) | Internal admin/vendor tools |
| `base_customer.html` | Customer-facing pages (`customer/*.html`) | Logged-in customer portal |
| `base_public.html` | Marketing/public pages (`index.html`, `home.html`) | Pre-login, public access |

## Required structure

```jinja
{% extends "base_customer.html" %}

{% block title %}{{ _('My Page Title') }}{% endblock %}

{% block content %}
<div class="p-6">
    <h1 class="text-2xl font-bold text-puresignage-primary mb-4">
        {{ _('Page Heading') }}
    </h1>
    <!-- content -->
</div>
{% endblock %}
```

## Brand styling (Tailwind tokens)

Use these custom Tailwind classes — they're defined inline in each base's `tailwind.config`:

- `puresignage-primary` — `#005430` (dark green, primary actions, headings)
- `puresignage-secondary` — `#057f48` (medium green, hover states, gradients)
- `puresignage-light` — `#e8f5e8` (mint, backgrounds, badges)

**Pattern for primary buttons:**

```html
<button class="bg-puresignage-primary hover:bg-puresignage-secondary text-white px-6 py-3 rounded-lg font-semibold transition-colors">
    {{ _('Submit') }}
</button>
```

**Pattern for gradient hero:**

```html
<section class="bg-gradient-to-r from-puresignage-primary to-puresignage-secondary text-white">
```

## i18n — every user-facing string

Wrap all visible copy in `{{ _('...') }}`. After adding strings, follow the **i18n-translations** skill to extract and translate them.

```jinja
{# good #}
<button>{{ _('Book Now') }}</button>

{# bad — won't translate #}
<button>Book Now</button>
<button>احجز الآن</button>
```

## RTL/LTR awareness

Default locale is Arabic (RTL). The base templates set `dir="rtl"` when `session.lang == 'ar'`.

- Use Tailwind's logical-direction utilities where possible: `ms-4` (margin-start), `me-4` (margin-end), `ps-6`, `pe-6`. These auto-flip in RTL.
- Use `start-0` / `end-0` instead of `left-0` / `right-0`.
- For icons that have direction (chevrons, arrows): the project already loads `rtl.css` / `ltr.css` to flip them. If your icon needs custom flipping, add a rule there — don't duplicate per-page.
- Test in **both** locales before declaring done: `/set-language/ar`, `/set-language/en`.

## Linking to other pages

Always use `url_for()` — never hardcode paths:

```jinja
<a href="{{ url_for('customer_dashboard') }}">{{ _('Dashboard') }}</a>
```

Hardcoded `<a href="/dashboard/customer">` will silently break if the route changes.

## Adding a route + template together

1. Add the route in `app.py`:
   ```python
   @app.route('/customer/new-page')
   def customer_new_page():
       return render_template('customer/new_page.html')
   ```
2. Create the template at `templates/customer/new_page.html` extending the right base.
3. If it should appear in the sidebar, add a nav link in the relevant `base*.html`.
4. Wrap all strings with `_()` and run the i18n extract/compile flow.

## Common pitfalls

- **Forgetting `{% extends %}`** — page renders without the layout, no sidebar, no nav.
- **Hardcoding hex colors** instead of `puresignage-primary` — looks fine in isolation, drifts from brand over time.
- **Using `left/right` margins** in RTL pages — layout breaks in Arabic.
- **Skipping `_()`** — Arabic users see English text; you'll be asked to fix it later anyway.
