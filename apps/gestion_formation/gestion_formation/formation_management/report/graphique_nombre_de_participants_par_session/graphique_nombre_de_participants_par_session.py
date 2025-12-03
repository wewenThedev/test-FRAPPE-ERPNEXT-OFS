# Copyright (c) 2025, Owen d'ALMEIDA and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt, getdate, nowdate

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart(data, filters)
    # report_summary = get_report_summary(data)
    return columns, data, None, chart
    # return columns, data, None, chart, report_summary

def get_columns():
    return [
        {
            "label": _("Session"),
            "fieldname": "session",
            "fieldtype": "Link", 
            "options": "Session de Formation",
            "width": 150
        },
        {
            "label": _("Cours"),
            "fieldname": "cours",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": _("Date Début"),
            "fieldname": "date_debut",
            "fieldtype": "Date",
            "width": 100
        },
        {
            "label": _("Date Fin"),
            "fieldname": "date_fin", 
            "fieldtype": "Date",
            "width": 100
        },
        {
            "label": _("Nombre Participants"),
            "fieldname": "nombre_participants",
            "fieldtype": "Int",
            "width": 120
        }
    ]

def get_data(filters=None):
    """
    Récupère les données du nombre de participants par session
    """
    # Conditions de base
    conditions = ["s.docstatus != 2"]  # Exclure les sessions annulées
    params = {}
    
    # Gestion des filtres
    if filters:
        if filters.get("from_date"):
            conditions.append("s.date_debut >= %(from_date)s")
            params["from_date"] = filters["from_date"]
        
        if filters.get("to_date"):
            conditions.append("s.date_debut <= %(to_date)s") 
            params["to_date"] = filters["to_date"]
        
        if filters.get("session"):
            conditions.append("s.name = %(session)s")
            params["session"] = filters["session"]
        
        if filters.get("cours"):
            conditions.append("s.cours = %(cours)s")
            params["cours"] = filters["cours"]
    
    # Construction de la clause WHERE
    where_clause = " AND " + " AND ".join(conditions) if conditions else "1=1"
    # where_clause = " AND ".join(conditions) if conditions else "1=1"
    
    # Requête SQL
    query = """
        SELECT 
            s.name as session,
            s.titre as titre_session,
            s.cours,
            c.titre as titre_cours,
            s.date_debut,
            s.date_fin,
            COALESCE(
                (SELECT COUNT(*) 
                 FROM `tabParticipant` p 
                 WHERE p.parent = s.name 
                 AND p.parenttype = 'Session de Formation'
                 AND p.statut != 'Annulé'
                ), 0
            ) as nombre_participants
        FROM `tabSession de Formation` s
        LEFT JOIN `tabCours` c ON c.name = s.cours
        WHERE {where_clause}
        ORDER BY s.date_debut DESC, s.name ASC
    """.format(where_clause=where_clause)
    
    # Exécution de la requête
    data = frappe.db.sql(query, params, as_dict=True)
    
    # Formatage des données
    for row in data:
        # Combiner titre et cours pour la colonne cours
        if row.get("titre_cours"):
            row["cours"] = f"{row.get('titre_cours', '')} ({row.get('cours', '')})"
        else:
            row["cours"] = row.get("cours", "")
        
        # S'assurer que le nombre est un entier
        row["nombre_participants"] = int(row.get("nombre_participants", 0))
    
    return data

def get_chart(data, filters=None):
    """
    Crée le graphique pour le rapport
    """
    if not data:
        return None
    
    # Préparer les données pour le graphique
    # Limiter à 20 sessions pour la lisibilité
    chart_data = data[:20]
    
    # Créer les labels (session + date)
    labels = []
    for row in chart_data:
        # Format court pour les labels
        label = f"{row.get('session', '')[:10]}"
        if row.get('date_debut'):
            label += f"\n{row['date_debut']}"
        labels.append(label)
    
    # Valeurs (nombre de participants)
    values = [row.get("nombre_participants", 0) for row in chart_data]
    
    # Déterminer le type de graphique selon le nombre de données
    chart_type = "bar" if len(data) <= 10 else "line"
    
    chart = {
        "data": {
            "labels": labels,
            "datasets": [
                {
                    "name": _("Participants"),
                    "values": values
                }
            ]
        },
        "type": chart_type,
        "colors": ["#2e86ab"],
        "height": 400,
        "axisOptions": {
            "xAxisMode": "tick",
            "xIsSeries": 0
        }
    }
    
    # Options spécifiques pour les barres
    if chart_type == "bar":
        chart["barOptions"] = {
            "stacked": False,
            "spaceRatio": 0.5
        }
    
    return chart

# Fonction optionnelle pour des statistiques
def get_report_summary(data):
    """Retourne un résumé du rapport"""
    if not data:
        return []
    
    total_participants = sum([row.get("nombre_participants", 0) for row in data])
    total_sessions = len(data)
    avg_participants = total_participants / total_sessions if total_sessions > 0 else 0
    
    return [
        {
            "value": total_sessions,
            "label": _("Sessions"),
            "datatype": "Int",
            "color": "blue"
        },
        {
            "value": total_participants,
            "label": _("Participants totaux"),
            "datatype": "Int",
            "color": "green"
        },
        {
            "value": f"{avg_participants:.1f}",
            "label": _("Moyenne par session"),
            "datatype": "Float",
            "color": "orange"
        }
    ]