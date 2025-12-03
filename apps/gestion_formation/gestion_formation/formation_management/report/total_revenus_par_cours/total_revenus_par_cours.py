# Copyright (c) 2025, Owen d'ALMEIDA and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    
    # Calcul du total général
    # total_revenue = sum([flt(row.get("total_revenue", 0)) for row in data])
    # total_participants = sum([flt(row.get("total_participants", 0)) for row in data])
    
    # Ajout de la ligne de total
    # if data:
    #     data.append({
    #         "cours": "<b>TOTAL</b>",
    #         "titre_cours": "",
    #         "statut_cours": "",
    #         "nombre_sessions": len(data),
    #         "total_participants": total_participants,
    #         "total_revenue": total_revenue,
    #         "bold": 1  # Pour mettre en gras dans le rapport
    #     })
    
    return columns, data

def get_columns():
    return [
        {
            "label": _("Cours"),
            "fieldname": "cours",
            "fieldtype": "Link",
            "options": "Cours",
            "width": 150
        },
        {
            "label": _("Titre du Cours"),
            "fieldname": "titre_cours",
            "fieldtype": "Data",
            "width": 250
        },
        {
            "label": _("Statut"),
            "fieldname": "statut_cours",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("Nb. Sessions"),
            "fieldname": "nombre_sessions",
            "fieldtype": "Int",
            "width": 120
        },
        {
            "label": _("Total Participants"),
            "fieldname": "total_participants",
            "fieldtype": "Int",
            "width": 140
        },
        {
            "label": _("Total Revenue (€)"),
            "fieldname": "total_revenue",
            "fieldtype": "Currency",
            "width": 150,
            "precision": 2
        }
    ]

def get_data(filters=None):
    """
    Récupère les données des revenus par cours
    """
    conditions = []
    params = {}
    
    # Gestion des filtres
    if filters:
        if filters.get("cours"):
            conditions.append("c.name = %(cours)s")
            params["cours"] = filters["cours"]
        
        if filters.get("statut"):
            conditions.append("c.actif = %(statut)s")
            params["statut"] = filters["statut"]
    
    # Construction de la clause WHERE
    where_clause = " AND " + " AND ".join(conditions) if conditions else ""
    
    # Requête SQL optimisée
    query = """
        SELECT 
            c.name as cours,
            c.titre as titre_cours,
            c.actif as statut_cours,
            COUNT(DISTINCT s.name) as nombre_sessions,
            COALESCE(SUM(
                (SELECT COUNT(*) 
                 FROM `tabParticipant` p 
                 WHERE p.parent = s.name 
                 AND p.statut != 'Annulé')
            ), 0) as total_participants,
            COALESCE(SUM(
                (SELECT COUNT(*) 
                 FROM `tabParticipant` p 
                 WHERE p.parent = s.name 
                 AND p.statut != 'Annulé')
            ) * c.prix, 0) as total_revenue
        FROM `tabCours` c
        LEFT JOIN `tabSession de Formation` s ON s.cours = c.name 
            AND s.docstatus = 0
        WHERE 1=1 {where_clause}
        GROUP BY c.name, c.titre, c.actif, c.prix
        ORDER BY total_revenue DESC, c.titre ASC
    """.format(where_clause=where_clause)
    
    # Exécution de la requête
    data = frappe.db.sql(query, params, as_dict=True)
    
    # Formatage des données
    for row in data:
        # S'assurer que les nombres sont des entiers/floats
        row["nombre_sessions"] = int(row.get("nombre_sessions", 0))
        row["total_participants"] = int(row.get("total_participants", 0))
        row["total_revenue"] = flt(row.get("total_revenue", 0))
        
        # Si pas de sessions, montrer 0
        if row["nombre_sessions"] == 0:
            row["total_participants"] = 0
            row["total_revenue"] = 0
    
    return data
