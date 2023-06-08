frappe.listview_settings['External Borrowing'] = {
	get_indicator: function(doc) {
		var status_color = {
			"Unpaid": "orange",
			"Paid": "green",
			"Partly Paid": "blue",
			"Cancelled": "red"
		};
		return [__(doc.status), status_color[doc.status], "status,=,"+doc.status];
	},
}