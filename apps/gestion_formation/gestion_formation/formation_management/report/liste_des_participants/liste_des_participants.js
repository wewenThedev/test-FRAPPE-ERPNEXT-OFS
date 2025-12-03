// Copyright (c) 2025, Owen d'ALMEIDA and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Liste des Participants"] = {
	"filters": [
		{
            "fieldname": "session",
            "label": _("Session de Formation"),
            "fieldtype": "Link",
            "options": "Session de Formation",
		},
            {
            "fieldname": "statut",
            "label": _("Statut"),
            "fieldtype": "Select",
            "options": "Inscrit\nConfirmé\nAnnulé",
		},
	]
};
