import frappe


def after_install():
	settings = frappe.get_single("GNU Terry Pratchett Settings")
	if settings.overhead_names:
		return

	settings.append("overhead_names", {"overhead_name": "GNU Terry Pratchett"})
	settings.enabled = 1
	settings.scope = "Both"
	settings.save(ignore_permissions=True)
