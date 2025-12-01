import frappe
from frappe import _

def get_context(context):
    context.title = "Vue d'ensemble des formations"
    
    # context.update({
    #     'intro_title': _("Vue d'ensemble des formations"),
    #     'intro_text': _("Cette page présente toutes les sessions de formation à venir. Cliquez sur 'Afficher détails' pour plus d'informations."),
    # })
    
    return context

@frappe.whitelist()
def get_statistiques_globales():
    stats = frappe.db.sql("""
        SELECT 
            COUNT(DISTINCT name) as total_sessions,
            COUNT(DISTINCT cours) as total_cours,
            (SELECT COUNT(*) FROM `tabParticipant`) as total_participants
        FROM `tabSession de Formation`
        WHERE docstatus = 1
    """, as_dict=True)
    
    return stats[0] if stats else {}

@frappe.whitelist()
def get_sessions_a_venir():
    sessions = frappe.get_list('Session de Formation',
        filters={
            'date_debut': ['>=', frappe.utils.nowdate()],
        },
        fields=['name', 'cours', 'date_debut', 'date_fin', 'lieu'],
        order_by='date_debut asc',
        # limit_page_length=50
    )
    #ajouter le nombre de participants
    for session in sessions:
        # Récupérer le titre du cours
        if session['cours']:
            cours = frappe.get_doc('Cours', session['cours'])
            session['cours_nom'] = cours.titre

        # Compter les participants
        session['participants_count'] = frappe.db.count('Participant', {
            'parent': session['name'],
            'parentfield': 'participants'
        })
    
    return sessions
    # sessions = frappe.db.sql("""
    #     SELECT 
    #         name,
    #         cours,
    #         formateur,
    #         date_debut,
    #         date_fin,
    #         lieu,
    #         (SELECT COUNT(*) FROM `tabParticipant` WHERE parent = name) as nombre_participants
    #     FROM `tabSession de Formation`
    #     WHERE date_debut >= CURDATE()
    #       AND docstatus = 1
    #     ORDER BY date_debut ASC
    #     LIMIT 10
    # """, as_dict=True)
    
    # return sessions

@frappe.whitelist()
def get_session_details(session_name):
    
    if not frappe.db.exists("Session de Formation", session_name):
        return None
    
    session = frappe.get_doc("Session de Formation", session_name)
    
    # Récupérer le titre du cours
    # if session['cours']:
    #     cours = frappe.get_doc('Cours', session['cours'])
    #     session['cours_nom'] = cours.titre
    #     session['duree'] = cours.duree_heures
    #     session['prix'] = cours.prix
        
    # # Récupérer la liste des participants
    #     participants = frappe.get_all('Participant',
    #         filters={
    #             'parent': session['name'],
    #             'parentfield': 'participants'
    #         },
    #         fields=['nom', 'email', 'statut']
    #     )
        # session['participants'] = participants
            
    return {
        "name": session.name,
        "cours": session.cours,
        "cours": session.cours,
        "date_debut": session.date_debut,
        "date_fin": session.date_fin,
        "lieu": session.lieu,
        "participants_count": len(session.participants) if session.participants else 0,
        # "participants" : participants
        # "participants" : participants if session.participants else None
    }
   