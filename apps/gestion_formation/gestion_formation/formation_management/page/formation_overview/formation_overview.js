frappe.pages['formation-overview'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Vue d\'ensemble des formations',
		single_column: true
	});
	// Message d'introduction (set_intro)
    // let $intro = page.set_intro('Cette page formation_overview affiche toutes les sessions de formation à venir. Cliquez sur "Afficher détails" pour plus d\'informations.'));

	//let $btn = page.set_primary_action('New', () => frappe.msgprint('Ajouter nouveau cliqué'));
	
	//$(frappe.render_template('formation_overview.html', {data : 'Hello from html Frappe'})).appendTo(page.body);
	//$(frappe.render_template("formation_overview.html", {})).appendTo(page.body);

	// Afficher un message de chargement
    // $(page.body).html(`
    //     <div class="text-center py-5">
    //         <div class="spinner-border text-primary" role="status">
    //             <span class="sr-only">Chargement...</span>
    //         </div>
    //         <p class="mt-2">Chargement de la page...</p>
    //     </div>
    // `);


	$(page.body).html(`
        <div class="formation-overview">
            <div class="row mb-4">
                <div class="col-md-6">
                    <h4>Sessions à venir</h4>
                    <p class="text-muted">Liste des sessions de formation programmées</p>
                </div>
                <div class="col-md-6 text-right">
                    <button class="btn btn-primary btn-refresh">
                        <i class="fa fa-refresh"></i> Rafraîchir
                    </button>
                    <button class="btn btn-success" onclick="create_new_session()">
                        <i class="fa fa-plus"></i> Nouvelle session
                    </button>
                </div>
            </div>

            <!-- Indicateur de chargement -->
            <div id="loading-indicator" class="text-center">
                <div class="spinner-border text-primary" role="status">
                    <span class="sr-only">Chargement...</span>
                </div>
                <p class="mt-2">Chargement des sessions...</p>
            </div>

            <!-- Conteneur du tableau (vide au départ) -->
            <div id="sessions-table-container" class="d-none">
                <!-- Le tableau récupéré sera ajouté ici dynamiquement -->
            </div>

            <!-- Message si aucune session -->
            <div id="no-sessions-message" class="d-none alert alert-info">
                <i class="fa fa-info-circle"></i> Aucune session à venir pour le moment.
            </div>

            <!-- Section détails (cachée par défaut) -->
            <div id="details-section" class="card mt-4 d-none">
                <div class="card-header bg-secondary text-white">
                    <div class="d-flex justify-content-between align-items-center">
                        <h5 class="mb-0">Détails de la session</h5>
                        <button class="btn btn-sm btn-light" onclick="close_details()">
                            <i class="fa fa-times"></i>
                        </button>
                    </div>
                </div>
                <div class="card-body" id="details-content">
                    <!-- Contenu des détails chargé dynamiquement -->
                </div>
            </div>
        </div>
    `);

    // Initialiser le tableau
    load_sessions_table(page);
    
    // Écouter le bouton de rafraîchissement
    $('.btn-refresh').click(function() {
        load_sessions_table(page);
    });

    // Sauvegarder la référence de la page
    window.current_page = page;
};

function load_sessions_table(page) {
    $('#loading-indicator').removeClass('d-none');
    $('#sessions-table-container').addClass('d-none');
    $('#no-sessions-message').addClass('d-none');

    // Appel au serveur avec frappe.call
    frappe.call({
        //method: 'gestion_formation.formation_management.doctype.session_de_formation.session_de_formation.get_upcoming_sessions',
        method: 'gestion_formation.formation_management.page.formation_overview.formation_overview.get_sessions_a_venir',
        args: {},
        freeze: false,
        freeze_message: __('Chargement des sessions...'),
        callback: function(response) {
            $('#loading-indicator').addClass('d-none');
            
            if (response.message && response.message.length > 0) {
                // Afficher le tableau avec les données
                render_sessions_table(response.message);
                $('#sessions-table-container').removeClass('d-none');
            } else {
                // Afficher le message "aucune session"
                $('#no-sessions-message').removeClass('d-none');
            }
        },
        error: function(error) {
            // Gestion des erreurs
            $('#loading-indicator').addClass('d-none');
            frappe.msgprint({
                title: __('Erreur'),
                message: __('Impossible de charger les sessions. Veuillez réessayer.'),
                indicator: 'red'
            });
            console.error('Erreur lors du chargement:', error);
        }
    });
}

function render_sessions_table(sessions) {
    var table_html = `
        <div class="table-responsive">
            <table class="table table-hover table-striped">
                <thead class="thead-dark">
                    <tr>
                        <th width="15%">Session</th>
                        <th width="25%">ID du Cours</th>
                        <th width="15%">Date début</th>
                        <th width="15%">Date fin</th>
                        <th width="10%" class="text-center">Participants</th>
                        <th width="20%" class="text-center">Actions</th>
                    </tr>
                </thead>
                <tbody>
    `;

    // Ajouter chaque ligne de session
    sessions.forEach(function(session, index) {
        // Formater les dates
        //var date_debut_formatted = format_date(session.date_debut);
        //var date_fin_formatted = format_date(session.date_fin);
        
        table_html += `
            <tr data-session-id="${session.name}" class="session-row">
                <td>
                    <strong>${session.name}</strong>
                    <br>
                    
                </td>
                <td>${session.cours_nom || session.cours || 'Non spécifié'}</td>
                <td>${session.date_debut}</td>
                <td>${session.date_fin}</td>
                <td class="text-center">
                    <span class="badge badge-pill badge-primary">
                        ${session.participants_count || 0}
                    </span>
                </td>
                <td class="text-center">
                    <div class="btn-group" role="group">
                        <button class="btn btn-sm btn-outline-primary btn-details" 
                                data-session="${session.name}">
                            <i class="fa fa-eye"></i> Détails
                        </button>
                        <button class="btn btn-sm btn-outline-success" 
                                onclick="open_session('${session.name}')">
                            <i class="fa fa-edit"></i> Ouvrir
                        </button>
                    </div>
                </td>
            </tr>
        `;
    });

    table_html += `
                </tbody>
            </table>
            
            <div class="alert alert-light mt-3">
                <div class="row">
                    <div class="col-md-6">
                        <i class="fa fa-info-circle"></i>
                        Total: <strong>${sessions.length}</strong> session(s) à venir
                    </div>
                    <div class="col-md-6 text-right">
                        <small class="text-muted">Dernière mise à jour: ${new Date().toLocaleTimeString()}</small>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Injecter le HTML dans le conteneur
    $('#sessions-table-container').html(table_html);
    
    // Attacher les événements aux boutons "Détails"
    $('.btn-details').click(function() {
        var session_name = $(this).data('session');
        show_session_details(session_name);
    });
}

// Fonction pour afficher les détails d'une session
function show_session_details(session_name) {
    // Afficher la section détails
    $('#details-section').removeClass('d-none');
    
    // Afficher un indicateur de chargement
    $('#details-content').html(`
        <div class="text-center py-4">
            <div class="spinner-border text-primary" role="status">
                <span class="sr-only">Chargement...</span>
            </div>
            <p class="mt-2">Chargement des détails...</p>
        </div>
    `);
    
    // Appeler l'API pour récupérer les détails
    frappe.call({
        method: 'gestion_formation.formation_management.page.formation_overview.formation_overview.get_session_details',
        args: {
            session_name: session_name
        },
        freeze: false,
        callback: function(response) {
            if (response.message) {
                render_session_details(response.message);
            } else {
                $('#details-content').html(`
                    <div class="alert alert-warning">
                        Impossible de charger les détails de cette session.
                    </div>
                `);
            }
        }
    });
}

// Fonction pour afficher les détails
function render_session_details(session) {
    var html = `
        <div class="row">
            <div class="col-md-6">
                <h6>Informations de la session</h6>
                <table class="table table-sm table-bordered">
                    <tr>
                        <th width="40%">Référence</th>
                        <td>${session.name}</td>
                    </tr>
                    <tr>
                        <th>Cours</th>
                        <td>${session.cours_nom || session.cours || 'Non spécifié'}</td>
                    </tr>
                    <tr>
                        <th>Date de début</th>
                        <td>${session.date_debut}</td>
                    </tr>
                    <tr>
                        <th>Date de fin</th>
                        <td>${session.date_fin}</td>
                    </tr>
					<tr>
                        <th>Participants</th>
                        <td>${session.participants_count}</td>
                    </tr>
                    
                </table>
            </div>`;
            
    //         <div class="col-md-6">
    //             <h6>Participants (${session.participants_count})</h6>
    // `;
    
    //if (session.participants && session.participants.length > 0) {
    if (session.participants && session.participants_count > 0) {
        html += `
            <div class="list-group" style="max-height: 300px; overflow-y: auto;">
        `;
        // Déterminer la couleur du badge selon le statut
        var badge_class = get_badge_class(session.participant.statut);
        
        session.participants.forEach(function(participant, index) {
            html += `
                <div class="list-group-item">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <strong>${index + 1}. ${participant.nom || 'Anonyme'}</strong>
                            <br>
                            <small>${participant.email || 'Pas d\'email'}</small>
                        </div>
                        <span class="badge badge-${badge_class}">
                            ${participant.statut || 'Inconnu'}
                        </span>
                    </div>
                </div>
            `;
        });
        
        // html += `</div>`;
    } 
	// else {
    //     html += `
    //         <div class="alert alert-warning">
    //             <i class="fa fa-user-slash"></i> Aucun participant inscrit
    //         </div>
    //     `;
    // }
    
    html += `
            </div>
        </div>
        
        <div class="row mt-4">
            <div class="col-md-12">
                <div class="btn-group" role="group">
                    <button class="btn btn-primary" onclick="open_session('${session.name}')">
                        <i class="fa fa-external-link-alt"></i> Ouvrir dans l'application
                    </button>
                    <button class="btn btn-outline-secondary" onclick="close_details()">
                        <i class="fa fa-times"></i> Fermer
                    </button>
                </div>
            </div>
        </div>
    `;
    
    $('#details-content').html(html);
}

function get_badge_class(status) {
    var classes = {
        'Inscrit': 'warning',
        'Confirmé': 'success',
        'Annulée': 'danger'
    };
    return classes[status] || 'light';
}

function open_session(session_name) {
    frappe.set_route('Form', 'Session de Formation', session_name);
}

function close_details() {
    $('#details-section').addClass('d-none');
}

function create_new_session() {
    frappe.new_doc('Session de Formation');

}