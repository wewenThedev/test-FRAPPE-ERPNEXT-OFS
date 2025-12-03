// Copyright (c) 2025, Owen d'ALMEIDA and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Total des revenus par cours"] = {
    "filters": [
        {
            "fieldname": "cours",
            "label": __("Cours"),
            "fieldtype": "Link",
            "options": "Cours",
            "width": 200,
        },
        {
            "fieldname": "statut",
            "label": __("Statut du Cours"),
            "fieldtype": "Check",
            // "fieldtype": "Select",
            // "options": "\nActif\nInactif\nArchivé",
            // "default": "Actif",
            "width": 150
        },
        {
            "fieldname": "date_debut",
            "label": __("Date de début"),
            "fieldtype": "Date",
            "width": 100,
            "hidden": 0  // Caché par défaut
        },
        {
            "fieldname": "date_fin",
            "label": __("Date de fin"),
            "fieldtype": "Date",
            "width": 100,
            "hidden": 0
        }
	]
};
