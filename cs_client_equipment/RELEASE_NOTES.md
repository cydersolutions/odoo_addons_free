# Client Equipment — Release Notes

---

## v19.0.1.0.8 — Multi-Language Support
**Released:** May 2026

This release adds full multi-language infrastructure to the module. All user-facing strings are now correctly marked for translation, a master translation template is in place, and Spanish translations are provided for both Spain and Latin America out of the box.

### Translation Infrastructure

A master `.pot` template file has been added to the `i18n/` directory. It covers every translatable string in the module: field labels, help text, model names, menu items, action names, view strings including placeholders and empty-state messages, security group names, and constraint error messages. This file is the source from which all language translations are derived and is the mechanism by which Odoo's translation export identifies strings belonging to this module.

### Spanish Translations

Two Spanish `.po` files are included:

`es.po` targets Spain Spanish. Key terminology choices reflect Castilian convention — "Equipamiento" for Equipment, "Incidencias" for Issues, "Informe" for Report, "Provincia" for State, and "Añada" in instructional strings.

`es_419.po` targets Latin American Spanish. Terminology follows regional convention — "Equipo" for Equipment, "Problemas" for Issues, "Reporte" for Report, "Estado" for State, and "Agregue" in instructional strings.

Both files cover the full string set. Regional differences are deliberate and reflect genuine variation in business Spanish across the two markets.

### Code Corrections

Two Python files were corrected as part of this work.

`contacts.py` was missing the `_` translation function import. The `listEquipment()` method was returning an action dictionary with the window title as a bare string, meaning it would not be translated regardless of the user's language setting. Both issues are resolved.

`equipment.py` constraint error messages for serial number and asset tag uniqueness were bare strings. These are now wrapped with `_()` so they are correctly extracted into the translation template and routed through Odoo's translation system at runtime.

### Files Added
- `i18n/cs_client_equipment.pot`
- `i18n/es.po`
- `i18n/es_419.po`

### Files Changed
- `models/contacts.py`
- `models/equipment.py`

---

## v19.0.1.0.7 — Product Linkage and System Improvements
**Released:** April 2026

### Product Field on Equipment
Equipment records can now be linked to a product via a new `product_id` field. When a product is selected, the manufacturer, model, internal reference, and equipment category are populated automatically from the product record where those values exist and the corresponding equipment fields are empty. This enables equipment to be tied into the product catalogue without overwriting data already entered on the record.

### Uniqueness Constraints
Serial number and asset tag fields are now enforced as unique at the database level using `models.Constraint`. Duplicate values will be rejected on save with a clear error message identifying the conflict.

### System Field
Equipment records now carry a `system_id` convenience field alongside the existing `system_ids` many-to-many. The field is computed from the first linked system and is writable via an inverse — setting it replaces the system assignment entirely. This simplifies the common case where equipment belongs to a single system while preserving the underlying many-to-many for more complex arrangements.

### Files Changed
- `models/equipment.py`
- `views/equipment_view.xml`

---

*Client Equipment — Cyder Solutions*
*Last updated: May 2026*
