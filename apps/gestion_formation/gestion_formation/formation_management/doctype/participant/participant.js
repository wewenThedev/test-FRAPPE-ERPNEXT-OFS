//créé par moi-meme pour tester

frappe.ui.form.on('Participant', {
    // email: function(frm, cdt, cdn) {
    //     let row = frappe.get_doc(cdt, cdn);

    //     if (row.email && (!row.nom || row.nom.trim() === "")) {
    //         row.nom = "Participant inconnu";
    //         frm.refresh_field("participants");
    //     }
    // }

    
    email: function(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);
        const email = row.email;
		const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

		if (email && !regex.test(email)) {
			frappe.msgprint(__('Veuillez entrer une adresse email valide.'));
			frappe.validated = false;
		}
    }
});