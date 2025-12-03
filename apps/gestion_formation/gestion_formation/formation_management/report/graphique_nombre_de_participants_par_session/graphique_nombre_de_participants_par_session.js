// Copyright (c) 2025, Owen d'ALMEIDA and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Graphique Nombre de participants par session"] = {
	"filters": [
		{
            "fieldname": "from_date",
            "label": __("Date Début"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_days(frappe.datetime.get_today(), -30),
            "reqd": 0,
            "width": 80
        },
        {
            "fieldname": "to_date",
            "label": __("Date Fin"),
            "fieldtype": "Date", 
            "default": frappe.datetime.get_today(),
            "reqd": 0,
            "width": 80
        },
        {
            "fieldname": "session",
            "label": __("Session"),
            "fieldtype": "Link",
            "options": "Session de Formation",
            "reqd": 0,
            "width": 100,
            "get_query": function() {
                return {
                    "filters": {
                        "docstatus": ["!=", 2]
                    }
                };
            }
        },
        {
            "fieldname": "cours",
            "label": __("Cours"),
            "fieldtype": "Link",
            "options": "Cours",
            "reqd": 0,
            "width": 100
        },
	]
};
