# # Fichier: gestion_formation/reports/sessions_par_periode/sessions_par_periode.py

# import frappe
# from frappe import _
# from datetime import datetime

# def execute(filters=None):
#     # Colonnes du rapport
#     columns = [
#         {
#             "fieldname": "name",
#             "label": _("Session"),
#             "fieldtype": "Link",
#             "options": "Session de Formation",
#             "width": 120
#         },
#         {
#             "fieldname": "cours",
#             "label": _("Cours"),
#             "fieldtype": "Link", 
#             "options": "Cours",
#             "width": 150
#         },
#         {
#             "fieldname": "formateur",
#             "label": _("Formateur"),
#             "fieldtype": "Link",
#             "options": "Formateur", 
#             "width": 150
#         },
#         {
#             "fieldname": "date_debut",
#             "label": _("Date Début"),
#             "fieldtype": "Date",
#             "width": 100
#         },
#         {
#             "fieldname": "date_fin", 
#             "label": _("Date Fin"),
#             "fieldtype": "Date",
#             "width": 100
#         },
#         {
#             "fieldname": "nombre_participants",
#             "label": _("Participants"),
#             "fieldtype": "Int",
#             "width": 80
#         }
#     ]
    
#     # Conditions WHERE basées sur les filtres
#     conditions = "1=1"
#     values = {}
    
#     if filters.get("date_debut"):
#         conditions += " AND date_debut >= %(date_debut)s"
#         values["date_debut"] = filters.get("date_debut")
    
#     if filters.get("date_fin"):
#         conditions += " AND date_fin <= %(date_fin)s" 
#         values["date_fin"] = filters.get("date_fin")
    
#     # Requête SQL avec jointures
#     data = frappe.db.sql("""
#         SELECT 
#             s.name,
#             s.cours,
#             s.formateur,
#             s.date_debut,
#             s.date_fin,
#             (SELECT COUNT(*) FROM `tabParticipant` p WHERE p.parent = s.name) as nombre_participants
#         FROM `tabSession de Formation` s
#         WHERE {conditions}
#         ORDER BY s.date_debut
#     """.format(conditions=conditions), values, as_dict=1)
    
#     return columns, data

# def get_filters():
#     """Définition des filtres disponibles"""
#     return [
#         {
#             "fieldname": "date_debut",
#             "label": _("Date Début"),
#             "fieldtype": "Date",
#             "width": 80
#         },
#         {
#             "fieldname": "date_fin",
#             "label": _("Date Fin"), 
#             "fieldtype": "Date",
#             "width": 80
#         }
#     ]
#     def execute(filters=None):
#     # Pas besoin d'importer frappe - c'est disponible automatiquement
    
#     columns = [
#         {"fieldname": "cours", "label": "Cours", "fieldtype": "Link", "options": "Cours", "width": 200},
#         {"fieldname": "prix_cours", "label": "Prix", "fieldtype": "Currency", "width": 100},
#         {"fieldname": "total_participants", "label": "Participants", "fieldtype": "Int", "width": 100},
#         {"fieldname": "revenu_total", "label": "Revenu Total", "fieldtype": "Currency", "width": 150},
#     ]
    
#     # Utiliser frappe.db.sql directement (disponible dans le contexte)
#     data = frappe.db.sql("""
#         SELECT 
#             c.name as cours_id,
#             c.titre as cours_nom,
#             COALESCE(c.prix, 0) as prix,
#             (
#                 SELECT COUNT(*)
#                 FROM `tabParticipant` p
#                 INNER JOIN `tabSession de Formation` s ON s.name = p.parent
#                 WHERE s.cours = c.name 
#                 AND s.docstatus = 1
#             ) as participants_totaux
#         FROM `tabCours` c
#         WHERE c.actif = 1
#         ORDER BY (COALESCE(c.prix, 0) * participants_totaux) DESC
#     """, as_dict=1)
    
#     formatted_data = []
#     for row in data:
#         revenu_total = row['prix'] * row['participants_totaux']
#         formatted_data.append({
#             "cours": row['cours_id'],
#             "prix_cours": row['prix'],
#             "total_participants": row['participants_totaux'],
#             "revenu_total": revenu_total
#         })
    
#     return columns, formatted_data