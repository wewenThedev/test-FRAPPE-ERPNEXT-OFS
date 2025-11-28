# Copyright (c) 2025, Owen d'ALMEIDA and contributors
# For license information, please see license.txt

# Fichier: gestion_formation/reports/revenus_par_cours_chart/revenus_par_cours_chart.py

import frappe
from frappe import _

def execute(filters=None):
    columns = [
        {
            "fieldname": "cours",
            "label": _("Cours"), 
            "fieldtype": "Data",
            "width": 200
        },
        {
            "fieldname": "revenu_estime",
            "label": _("Revenu Estimé (FCFA)"),
            "fieldtype": "Currency",
            "width": 150
        }
    ]
    
    # Filtres dynamiques
    conditions = "s.docstatus = 1"
    if filters and filters.get("cours"):
        conditions += f" AND c.name = '{filters['cours']}'"
    if filters and filters.get("date_debut"):
        conditions += f" AND s.date_debut >= '{filters['date_debut']}'"
    if filters and filters.get("date_fin"):
        conditions += f" AND s.date_fin <= '{filters['date_fin']}'"
    
    data = frappe.db.sql(f"""
        SELECT 
            c.titre as cours,
            SUM(COALESCE(c.prix, 0) * (
                SELECT COUNT(*) 
                FROM `tabParticipant` p 
                WHERE p.parent = s.name
            )) as revenu_estime
        FROM `tabCours` c
        LEFT JOIN `tabSession de Formation` s ON s.cours = c.name
        WHERE {conditions}
        GROUP BY c.name, c.titre
        HAVING revenu_estime > 0
        ORDER BY revenu_estime DESC
        LIMIT 8
    """, as_dict=1)
    
    chart = {
        "title": _("Revenus par Cours"),
        "data": {
            "labels": [d["cours"] for d in data],
            "datasets": [
                {
                    "name": _("Revenus (€)"),
                    "values": [d["revenu_estime"] for d in data]
                }
            ]
        },
        "type": "bar",
        "height": 300,
        "colors": ["#2e86ab"]
    }
    
    return columns, data, None, chart

def get_filters():
    return [
        {
            "fieldname": "date_debut",
            "label": _("Date Début"),
            "fieldtype": "Date",
            "default": frappe.utils.add_days(frappe.utils.nowdate(), -90)
        },
        {
            "fieldname": "date_fin",
            "label": _("Date Fin"),
            "fieldtype": "Date", 
            "default": frappe.utils.nowdate()
        },
        {
            "fieldname": "cours",
            "label": _("Cours"),
            "fieldtype": "Link",
            "options": "Cours"
        }
    ]