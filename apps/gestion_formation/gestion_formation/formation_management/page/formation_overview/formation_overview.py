# gestion_formation/pages/formation_overview.py
import frappe
from frappe import _

def get_context(context):
    context.title = "Vue d'ensemble des formations"

@frappe.whitelist()
def get_statistiques_globales():
    """Calcule les statistiques globales"""
    stats = frappe.db.sql("""
        SELECT 
            COUNT(DISTINCT name) as total_sessions,
            COUNT(DISTINCT cours) as total_cours,
            COUNT(DISTINCT formateur) as total_formateurs,
            (SELECT COUNT(*) FROM `tabParticipant`) as total_participants
        FROM `tabSession de Formation`
        WHERE docstatus = 1
    """, as_dict=True)
    
    return stats[0] if stats else {}

@frappe.whitelist()
def get_sessions_a_venir():
    """Récupère les sessions à venir"""
    sessions = frappe.db.sql("""
        SELECT 
            name,
            cours,
            formateur,
            date_debut,
            date_fin,
            lieu,
            (SELECT COUNT(*) FROM `tabParticipant` WHERE parent = name) as nombre_participants
        FROM `tabSession de Formation`
        WHERE date_debut >= CURDATE()
          AND docstatus = 1
        ORDER BY date_debut ASC
        LIMIT 10
    """, as_dict=True)
    
    return sessions

@frappe.whitelist()
def get_session_details(session_name):
    """Récupère les détails d'une session spécifique"""
    if not frappe.db.exists("Session de Formation", session_name):
        return None
    
    session = frappe.get_doc("Session de Formation", session_name)
    return {
        "name": session.name,
        "cours": session.cours,
        "formateur": session.formateur,
        "date_debut": session.date_debut,
        "date_fin": session.date_fin,
        "lieu": session.lieu,
        "participants_count": len(session.participants) if session.participants else 0
    }