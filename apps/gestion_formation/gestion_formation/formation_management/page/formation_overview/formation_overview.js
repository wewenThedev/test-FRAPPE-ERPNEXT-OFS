frappe.pages['formation-overview'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Vue d\'ensemble des formations',
		single_column: true
	});
}