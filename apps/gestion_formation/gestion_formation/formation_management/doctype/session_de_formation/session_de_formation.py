# Copyright (c) 2025, Owen d'ALMEIDA and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import datetime, today, add_days, add_months, add_years

class SessiondeFormation(Document):

	def before_save(self) :
		if (self.date_debut and self.date_fin) :
			if not (self.date_debut <= self.date_fin) :
				frappe.throw(_("Date de fin choisie : {0}.\nLa date de fin doit être en avance sur (ultérieure à) la date de début.", [self.date_fin]))

	# @frappe.whitelist()
	# def test_un(self):
	# 	return len(self.participants)
	# 	# return "test"
# # Terminal 1 - Logs du serveur
# bench --site [nom-site] logs

# # Terminal 2 - Logs spécifiques à votre module
# bench --site [nom-site] logs | grep -E "(compter_participants|Session de Formation|Error|Exception)"

	@frappe.whitelist()
	def compter_participants(self) :
		count = int(0)
		# if(hasattr(self, 'participants') and not(self.participants)) :
		# 	count = len(self.participants)
		# else :
		# 	print("Aucun participant trouvé")
		# return count
		try :
			if(hasattr(self, 'participants') and self.participants and len(self.participants) > 0) :
				return len(self.participants)
			else :
				return count
				# return "zéro"
				# return frappe.db.count('Participant', filters={'parent_name': self.name})
				
		except Exception as e:
			frappe.log_error(f"Erreur compter_participants: {e}")
			return f"Erreur: {e}"
	
	def validate(self) :
        #frappe.msgprint("Validation réussie avec succès")
        # Vérifier si le doctype personnalisé existe
		if frappe.db.exists("DocType", "Document Log") :
            # Log personnalisé
            # if frappe.get_doc('Document Log', self.name):  # Si ce n'est pas un nouveau document # if not self.is_new():
			try :
				document_log = frappe.get_doc({
                    'doctype' : 'Document Log',
                    'titre' : "Modification" if self.get("__islocal") else "Création" + f' Session pour {self.cours} enregistrée',
                    'message' : f"""- Cours: {self.cours}\n- Dates: Du {self.date_debut} au {self.date_fin}\n- Participants: {self.compter_participants()}\n- Session: {frappe.session.user},"""
                    # - Formateur: {self.cours.formateur}    
                    # 'La session de formation pour le cours {self.cours.titre} d\'une durée de {self.cours.duree_heures} est enregistrée.\nElle aura lieu du {self.date_debut} au {self.date_fin}.',
                })
				document_log.insert()
				frappe.msgprint(f'Validation réussie.<br>Document Log créé : {document_log.name}')
			except Exception as e:
				frappe.log_error(f"Erreur: {e}")
				return f"Erreur: {e}"
		else :
			frappe.throw('Echec de la validation')
    
	def autres_fonctions_exemple(self):
		"""
        Exemples d'utilisation des fonctions demandées
        """
        
        # 1. get_doc()
		cours_doc = frappe.get_doc('Cours', self.cours)
        # 2. get_list()
		formateurs_actifs = frappe.get_list('Formateur', 
            filters={'actif': 1},
            fields=['nom_complet', 'email']
        )
        
        # 3. exists() - Vérifier si un document existe
		if frappe.db.exists('Formateur', self):
			frappe.msgprint("Le formateur existe dans la base")
        
        # 4. set_value() - Mettre à jour un champ
			frappe.db.set_value('Cours', self.cours, 'actif', 1)
        
        # 5. frappe.db.sql() - Exécuter une requête SQL directe
		sessions_count = frappe.db.sql("""
            SELECT COUNT(*) 
            FROM `tabSession de Formation` 
            WHERE cours = %s
        """, self.cours)
  
	@frappe.whitelist()
	# def get_formateur_et_telephone_par_cours(cours_name):
	def get_infos_formateur(self):
		cours_name = self.cours
		try :
			if not cours_name:
				return "Erreur, Cours inexistant !"
            
			cours = frappe.get_doc("Cours", cours_name)
			if not cours or not cours.formateur:
				return {"formateur": "Aucun formateur assigné à ce cours", "telephone": "Néant"}
            
			formateur_name = cours.formateur
			formateur = frappe.get_doc("Formateur", formateur_name)
			telephone = formateur.telephone if formateur.telephone else "Non renseigné"
            
			return {
                "formateur": formateur_name,
                "telephone": telephone,
                "nom_complet": formateur.nom_complet
            }
		except Exception as e:
			frappe.log_error(f"Erreur get_formateur_et_telephone: {e}")
			return {"formateur": "", "telephone": "Erreur de récupération"}


    #     #frappe.new_doc()
    #     frappe.msgprint(_("{0}. The family member name is {1} and relation is {2}").format(row.idx, row.first_name, row.relation))
    # frappe.msgprint(_("Validation {0} réussie avec succès").format([]))

    # def on_submit(self) :
    #     pass

# gestion_formation.formation_management.doctype.session_de_formation.session_de_formation.

