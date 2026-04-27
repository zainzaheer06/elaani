---
name: i18n-translations
description: Add, update, or compile Arabic/English translations. Use when the user adds new user-facing strings, edits existing copy, asks for "Arabic translation" or "English translation", or reports missing/wrong translations on a page.
---

# Updating Pure Signage translations

This project uses **Flask-Babel** with gettext `.po` (source) / `.mo` (compiled) files. Default locale is **Arabic (`ar`)**, fallback is English (`en`).

## Where translations live

- `Pure Signage/translations/{ar,en}/LC_MESSAGES/messages.{po,mo}`

## Wrap, then extract

In Python:

```python
from flask_babel import gettext
flash(gettext('Screen not found'), 'error')
```

In Jinja templates:

```jinja
<h1>{{ _('Browse Screens') }}</h1>
<p>{{ _('Welcome, %(name)s', name=user.name) }}</p>
```

**Never hardcode Arabic or English copy** in HTML or Python — it won't translate, and the app will look monolingual on language switch.

## Workflow when adding new strings

Run from the app root (`Pure Signage/`):

```bash
# 1. Extract all _() / gettext() calls into messages.pot
pybabel extract -F babel.cfg -o messages.pot .

# 2. Merge into existing .po files (preserves existing translations)
pybabel update -i messages.pot -d translations

# 3. Edit translations/ar/LC_MESSAGES/messages.po — fill in msgstr "..." for each new msgid
# 4. Compile to .mo (Flask-Babel reads the binary .mo at runtime)
pybabel compile -d translations
```

`babel.cfg` already exists in the project root.

## Editing .po files

A `.po` entry looks like:

```po
#: templates/dashboard.html:42
msgid "Browse Screens"
msgstr "تصفح الشاشات"
```

- `msgid` is the English source. Don't change it after extraction unless you also update every `_('...')` call site.
- `msgstr` is the translation. Empty string means "fall back to the msgid".
- **Pluralization** uses `msgid_plural` + `msgstr[0]`, `msgstr[1]`, ... — Arabic has 6 plural forms; English has 2. Use `ngettext()` in code for plurals.

## After editing

- **Always run `pybabel compile -d translations`** — without recompiling, Flask-Babel keeps serving the stale `.mo`.
- **Restart the Flask server** — `.mo` files are loaded at startup, not per-request.
- Test both locales: visit `/set-language/ar` and `/set-language/en` and confirm the new copy renders correctly in both.

## Common pitfalls

- **String with apostrophe:** wrap with double quotes in templates: `{{ _("Don't show again") }}`. In `.po` use `\'` or double-quote the whole msgstr.
- **Same English string, different Arabic depending on context:** gettext can't disambiguate by context alone. Use `pgettext('context', 'string')` in Python and accept that templates will share one translation per msgid.
- **RTL/LTR layout breaks** after adding long Arabic strings: that's a CSS issue, not a translation issue. Check `static/css/rtl.css` for the affected component.
