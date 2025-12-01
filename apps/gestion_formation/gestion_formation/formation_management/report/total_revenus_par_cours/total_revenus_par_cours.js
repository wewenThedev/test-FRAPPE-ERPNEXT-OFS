// Copyright (c) 2025, Owen d'ALMEIDA and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Total revenus par cours"] = {
	"filters": [
		{
            "fieldname": "cours",
            "label": _("Cours"),
            "fieldtype": "Link",
            "options": "Cours",
		},
        // {
        //     "fieldname": "titre",
        //     "label": _("Titre du Cours"),
        //     "fieldtype": "Data", 
        // },
		{
            "fieldname": "nombre_sessions",
            "label": _("Nb Sessions"),
            "fieldtype": "Int", 
            "width": 100
        },
        {
            "fieldname": "total_participants",
            "label": _("Participants(toutes sessions)"),
            "fieldtype": "Int",
        },
        // {
        //     "fieldname": "prix",
        //     "label": _("Prix"),
        //     "fieldtype": "Currency",
        // },
        // {
        //     "fieldname": "revenu_total",
        //     "label": _("Revenu Total"),
        //     "fieldtype": "Currency",
        // }
	]
};
