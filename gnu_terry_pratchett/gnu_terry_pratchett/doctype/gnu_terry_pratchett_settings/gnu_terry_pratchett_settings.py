# Copyright (c) 2026, BuFf0k and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class GNUTerryPratchettSettings(Document):
	def validate(self):
		for row in self.overhead_names:
			if row.overhead_name:
				row.overhead_name = row.overhead_name.strip()

		if self.enabled and not any(row.overhead_name for row in self.overhead_names):
			frappe.throw(frappe._("Add at least one name under Overhead Names before enabling."))
