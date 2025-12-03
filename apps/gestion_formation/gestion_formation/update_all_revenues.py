# scripts/update_revenue.py
import frappe

def execute():
    """Script bench: bench execute gestion_formation.update_all_revenues.execute"""
    
    sessions = frappe.get_all('Session de Formation', 
        fields=['name', 'cours']
    )
    
    for session in sessions:
        # Calcul direct
        prix = frappe.db.get_value('Cours', session.cours, 'prix') or 0
        participants = frappe.db.count('Participant', {
            'parent': session.name
        })
        
        revenue = float(prix) * participants
        
        frappe.db.set_value(
            'Session de Formation',
            session.name,
            'revenue',
            revenue
        )
    
    frappe.db.commit()
    print("Done")