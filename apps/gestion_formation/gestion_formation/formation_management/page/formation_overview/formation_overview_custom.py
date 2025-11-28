# Fichier: gestion_formation/pages/formation_overview.py

import frappe
from frappe import _
import json
from datetime import datetime

def get_context(context):
    # Titre de la page
    context.title = _("Vue d'ensemble des formations")
    
    # Message d'introduction
    context.intro_message = _("Gestion complète des sessions de formation à venir")
    
    # Récupérer les sessions à venir
    context.sessions_a_venir = get_sessions_a_venir()
    
    # Statistiques globales
    context.stats = get_statistiques_globales()

def get_sessions_a_venir():
    """Récupère les sessions de formation à venir"""
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
          AND docstatus = 1  -- Seulement les sessions validées
        ORDER BY date_debut ASC
        LIMIT 10
    """, as_dict=True)
    
    return sessions

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

#####

# Ajouter ces méthodes dans formation_overview.py

@frappe.whitelist()
def get_session_details(session_name):
    """Récupère les détails complets d'une session"""
    if not session_name:
        return None
    
    session = frappe.get_doc("Session de Formation", session_name)
    
    # Formater les données pour l'affichage
    details = {
        "name": session.name,
        "cours": session.cours,
        "formateur": session.formateur,
        "date_debut": session.date_debut,
        "date_fin": session.date_fin,
        "lieu": session.lieu,
        "participants_count": len(session.participants) if session.participants else 0,
        "participants": []
    }
    
    # Ajouter les détails des participants
    if session.participants:
        for participant in session.participants:
            details["participants"].append({
                "nom": participant.nom,
                "email": participant.email,
                "statut": participant.statut
            })
    
    return details

@frappe.whitelist()
def get_sessions_a_venir_ajax():
    """Version AJAX de get_sessions_a_venir"""
    return get_sessions_a_venir()