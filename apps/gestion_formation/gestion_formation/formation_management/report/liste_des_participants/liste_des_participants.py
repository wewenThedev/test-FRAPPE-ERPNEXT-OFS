import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": _("Session"), "fieldname": "session", "fieldtype": "Link", "options": "Session de Formation", "width": 200},
        {"label": _("Nom du participant"), "fieldname": "nom", "fieldtype": "Data", "width": 200},
        {"label": _("Email"), "fieldname": "email", "fieldtype": "Data", "width": 200},
        {"label": _("Statut"), "fieldname": "statut", "fieldtype": "Data", "width": 150},
    ]

def get_data(filters=None):
    # Récupérer toutes les sessions
    sessions = frappe.get_all('Session de Formation', fields=['name'])
    
    data = []
    for session in sessions:
        # Récupérer les participants de la child table de cette session
        participants = frappe.get_all('Participant', 
            filters={'parent': session.name, 'parenttype': 'Session de Formation'},
            fields=['nom', 'email','statut', 'parent'])
        
        for participant in participants:
            data.append({
                'session': participant.parent,
                'nom': participant.nom,
                'email': participant.email,
                'statut': participant.statut
            })
    
    return data