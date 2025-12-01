// Copyright (c) 2025, Owen d'ALMEIDA and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["new Total revenus par cours"] = {
	"filters": [
		{
            "fieldname": "cours",
            "label": _("Cours"),
            "fieldtype": "Link",
            "options": "Cours",
		},
	]
};
