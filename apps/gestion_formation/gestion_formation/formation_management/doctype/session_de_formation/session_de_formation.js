// Copyright (c) 2025, Owen d'ALMEIDA and contributors
// For license information, please see license.txt

frappe.ui.form.on('Session de Formation', {

	date_fin: function (frm) {

		if (!frm.doc.date_debut && frm.doc.date_fin) {
			frappe.msgprint(__("La date de début de la session de formation est obligatoire. Sélectionnez-en une !"))
		}

		if (frm.doc.date_debut && frm.doc.date_fin) {
			//if (frappe.datetime.str_to_obj(frm.doc.date_fin) <= frappe.datetime.str_to_obj(frm.doc.date_debut)) {
			if (frm.doc.date_fin <= frm.doc.date_debut) {
				//frappe.msgprint("La date de fin doit être en avance sur (ultérieure à) la date de début.");
				frappe.msgprint(__("Date de fin choisie : {0}.\nLa date de fin doit être après (ultérieure à) la date de début.", [frm.doc.date_fin]));
				frm.set_value("date_fin", "");
			}
			//Partie B
			// Quand date_fin change, appeler la fonction de calcul
			calculer_duree_jours(frm);
		}

	},

	date_debut: function (frm) {
		if (frm.doc.date_debut && frm.doc.date_fin) {
			if (frm.doc.date_debut > frm.doc.date_fin) {
				frappe.msgprint(__("Date de début choisie : {0}.\nLa date de début doit être avant (ultérieure à) la date de début.", [frm.doc.date_debut]));
				//frappe.throw(__("Date de début choisie : {0}.\nLa date de début doit être avant (ultérieure à) la date de début.", [frm.doc.date_debut]));
				frm.set_value("date_debut", "");
			}
			// Quand date_debut change, appeler la fonction de calcul
			calculer_duree_jours(frm);
		}
	},


	cours: function (frm) {
		if (frm.doc.cours) {
			//frm.set_intro("Ce cours se déroule en plusieurs étapes. Vous découvrirez les différents modules du cours.\nLa majorité des cours sont au format vidéo, avec des quizz de bilan et une évaluation finale par module. \nSelon le niveau atteint, un exercice pratique d'assimilation est prévu pour étoffer votre CV.");

			// Appel au serveur pour récupérer les détails du cours
			frappe.call({
				method: 'frappe.client.get',  // Méthode Frappe standard pour récupérer un document
				args: {
					doctype: 'Cours',
					name: frm.doc.cours
				},
				callback: function (r) {
					if (r.message) {
						let cours = r.message;  // Stocker les données du cours
						// Afficher le message d'introduction formaté
						frm.set_intro(`
                            <b>Déroulement de la formation :</b><br>
                            - Cours : ${cours.titre}<br>
                            - Durée : ${cours.duree_heures} heures<br>
                            - Autres informations : Ce cours se déroule en plusieurs étapes. Vous découvrirez les différents modules du cours.\nLa majorité des cours sont au format vidéo, avec des quizz de bilan et une évaluation finale par module. \nSelon le niveau atteint, un exercice pratique d'assimilation est prévu pour étoffer votre CV.<br>
                        `);
					}
				}
			});


			//Partie 6
			frappe.call({
        		method: 'gestion_formation.formation_management.doctype.session_de_formation.session_de_formation.get_formateur_et_telephone_par_cours',
        		args: {
            		cours_name: frm.doc.cours
        		},
        		callback: function(r) {
            		if (r.message) {
                		let infos = r.message;
                
                		if (infos.formateur) {
                    	// Afficher l'alerte avec toutes les infos
                    		frappe.show_alert({
                        		message: `Formateur: ${infos.nom_complet || infos.formateur} - Téléphone: ${infos.telephone}`,
                        		indicator: 'blue',
								duration: 5
                    		});
                		}
            		}
        		},
        		error: function(err) {
            		console.error('Erreur chargement formateur:', err);
        		}
    		});
		}
	},

	lieu : function(frm){
		if(frm.doc.lieu){
			//let listeSessions = frappe.get_list('Session de Formation', filters={'date_debut' : ['>=', frappe.utils.nowdate()]})
			let listeSessions = frappe.get_list('Session de Formation',fields=['name', 'cours', 'date_debut', 'date_fin'], debug=True)
			

			listeSessions.array.forEach(element => {
				frappe.msgprint()
			});
		}
	},

	before_save: function (frm) {
		calculer_duree_jours(frm)
	},

	refresh: function (frm) {
		//CONFIRMER TOUS LES PARTICIPANTS marche pour une session de formation en particulier; après je peux faire foreach enfants de session
		// 	frappe.db.get_list('Participant');
		// 	//frappe.db.get_value('Participant', frm.doc, ['nom', 'email']);
		// 	//frappe.db.set_value('Participant', frm.doc, 'statut', 'Confirmé');
		// });

		// Ajouter un bouton personnalisé à la toolbarx
		frm.add_custom_button(__('Confirmer tous les participants'), function () {

			// Vérifier s'il y a des participants dans la table
			if (frm.doc.participants && frm.doc.participants.length > 0) {
				if (frm.doc.participants) {
					// Parcourir tous les participants du tableau
					frm.doc.participants.forEach(function (participant) {
						// Mettre le statut de chaque participant à "Confirmé"
						participant.statut = 'Confirmé';
					});
					// Rafraîchir l'affichage du tableau des participants
					frm.refresh_field('participants');
					frappe.show_alert({
						message: 'Tous les participants ont été confirmés',
						indicator: 'green'  // Couleur verte pour succès
					});
				}

			// 	frappe.get_doc('Customer', frm.doc.customer)
            // .then(customer => {
            //     console.log('Groupe client:', customer.customer_group);
            // });

			}
			else {
				frappe.throw(__('Aucun participant associé à la session de formation. Impossible de mettre à jour le statut !'))
			}
		});

		//Partie 6
        frm.add_custom_button(__('Afficher total participants'), function() {
            
			if (!frm.doc.name) {
        		frappe.msgprint({
            		title: __('Attention'),
            		message: __('Veuillez sauvegarder la session avant de compter les participants'),
            		indicator: 'orange'
        		});
        		return;
    		}
			// Appel serveur vers la méthode compter_participants
			console.log("I call server")
			frm.call({
				method: 'compter_participants',  // Méthode côté serveur
        		// args: {
        	    // 	cours_name: frm.doc.cours  // Passer le nom de la session
        		// },
        		freeze: true,                    // Bloquer l'interface pendant l'appel
        		freeze_message: __('Calcul du nombre de participants...'), // Message d'attente
        		callback: function(response) {
            		if (response.message !== undefined && response.message !== null) {
                		console.log("Nombre de participants:", response.message);
                
                		frappe.show_alert({
                    		message: __(`Nombre total de participants: ${response.message}`),
                    		indicator: 'green',  
                    		duration: 5
                		});
            		} else {
                		frappe.show_alert({
                    		message: __('Erreur lors du calcul des participants'),
                    		indicator: 'red',
							duration: 5
                		});
            		}
        		}
        	});
		});
			
				// .catch(error => {
                //     console.error('Erreur:', error);
                //     frappe.show_alert({
                //         message: 'Erreur lors du calcul des participants',
                //         indicator: 'red'
                //     });
                // });
	},

	//Partie 6
	

	participants_add: function (frm) {
		// Quand on ajoute une nouvelle ligne
		// email: function (frm) {
		// 	const email = frm.doc.participant.email;
		// 	const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

		// 	if (email && !regex.test(email)) {
		// 		frappe.msgprint(__('Veuillez entrer une adresse email valide.'));
		// 		//frappe.validated = false;
		// 	}
		// },
	},

	participants: function (frm, cdt, cdn) {
		const row = frappe.get_doc(cdt, cdn);
		const email = row.email;
		const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

		if (email && !regex.test(email)) {
			frappe.msgprint(__('Veuillez entrer une adresse email valide.'));
			frappe.validated = false;
		}

		if (row.email && (!row.nom || row.nom.trim() === "")) {
			row.nom = "Participant inconnu";
			frm.refresh_field("participants");
		}
	}

	//<div style="color:red;font-weight:bold;">La date de fin doit dépasser la date de début.</div>

	//validate : function (frm) {}

	/* 
	frappe.ui.form.on("Session de Formation", {
	
});*/

	// frm.add_custom_button("2 Confirmer tous les participants", () => {
	// 		frappe.msgprint('You clicked Me!')
	// 	}, 'click me');
	// 	frm.add_custom_button("3 Confirmer tous les participants", () => {
	// 		frappe.msgprint('You clicked Me!')
	// 	}, 'click me')
});

//les fonctions restent en dehors des frappe.ui.form.on de doctypes
function calculer_duree_jours(frm) {

	if (frm.doc.date_debut && frm.doc.date_fin) {
		let duree_session_formation = frappe.datetime.get_diff(frm.doc.date_fin, frm.doc.date_debut) +1
		//frappe.msgprint({
		frappe.show_alert({
			title: "Information Durée Session",
			message: `Cette session de formation va durer ${duree_session_formation} jours`,
			indicator: "blue"
		});
	}
}

// frappe.ui.form.on('Participants', {
frappe.ui.form.on('Participant', {

	email: function (frm, cdt, cdn) {
		// Récupérer la ligne modifiée dans la table enfant
		let row = locals[cdt][cdn];
		// Vérifier si l'email est rempli mais pas le nom
		if (row.email && !row.nom) {
			// Mettre automatiquement le nom à "Participant inconnu"
			frappe.model.set_value(cdt, cdn, 'nom', 'Participant inconnu');
		}
	}

});

frappe.ui.form.on('Participant', {

	email: function (frm, cdt, cdn) {
		// Récupérer la ligne modifiée dans la table enfant
		let row = locals[cdt][cdn];
		// Vérifier si l'email est rempli mais pas le nom
		if (row.email && !row.nom) {
			// Mettre automatiquement le nom à "Participant inconnu"
			frappe.model.set_value(cdt, cdn, 'nom', 'Participant inconnu');
		}
	}

});