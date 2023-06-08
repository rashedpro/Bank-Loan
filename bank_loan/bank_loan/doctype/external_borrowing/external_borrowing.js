// Copyright (c) 2023, slnee and contributors
// For license information, please see license.txt

frappe.ui.form.on('External Borrowing', {
	refresh: function(frm) {
		add_view_button(frm);
		
		if(frm.doc.docstatus===0){
			frm.set_value("status","Unpaid");
		}
	},
	onload:function(frm){
		frm.set_query("bank_accounts", function () {
			return {
				"filters": {
					"is_group": 0,
				}
			};
		});

		frm.set_query("account_of_deferred_funding_cost", function () {
			return {
				"filters": {
					"is_group": 0,
				}
			};
		});

		frm.set_query("interest_expense_account", function () {
			return {
				"filters": {
					"is_group": 0,
				}
			};
		});

		frm.set_query("lender_account", function () {
			return {
				"filters": {
					"is_group": 0,
				}
			};
		});
		
		frm.set_query("cost_of_financing_account", function () {
			return {
				"filters": {
					"is_group": 0,
				}
			};
		});
	},

	before_save:function(frm){
		calculate_the_payment(frm);
	},
	
	
});
function add_view_button(frm) {
	if (frm.doc.docstatus === 1) {
		frm.add_custom_button(
			__("Ledger"),
			function () {
				frappe.route_options = {
					voucher_no:frm.doc.jouranl_entery_reference,
					from_date: moment(frm.doc.posting_date).format(
						"YYYY-MM-DD"
					),
					to_date: moment(frm.doc.modified).format("YYYY-MM-DD"),
					company: frm.doc.company,
					group_by: "",
				};
				frappe.set_route("query-report", "General Ledger");
			},
			"fa fa-table"
		);
	}
}

function calculate_interest(frm){
	if(frm.doc.interest_expense_account!=="" && frm.doc.interest_expense_account!==undefined){
		const interest_percent=frm.doc.rate_of_interest*0.01;
		return interest_percent*frm.doc.loan_amount;
	}else{
		frappe.throw("You have to set the Interest Expense Account")
	}

}


function calculate_the_payment(frm){
	let total_interest=0;
	let interest_due_monthly=0;
	let payment_date=0;
	const amount_due_monthly=frm.doc.loan_amount/frm.doc.repayment_period_in_months;
	frm.doc.repayment_schedule=[];

	if(frm.doc.rate_of_interest>0){
		total_interest=calculate_interest(frm);
		interest_due_monthly=total_interest/frm.doc.repayment_period_in_months;
	}
	
	
	for (let i=1;i<=frm.doc.repayment_period_in_months;i++){

		let balance_loan_amount=i*amount_due_monthly;
		balance_loan_amount=frm.doc.loan_amount-balance_loan_amount;
		
		balance_loan_amount+=total_interest-(i*interest_due_monthly)
		
		if(i==1){
		payment_date=frappe.datetime.add_months(cur_frm.doc.repayment_start_date, 0);
		}else{
			payment_date=frappe.datetime.add_months(cur_frm.doc.repayment_start_date, i-1);	
		}

		fill_child_table_field(frm,amount_due_monthly,balance_loan_amount,payment_date,interest_due_monthly);
	}
	
}


function fill_child_table_field(frm,amount_due_monthly,balance_loan_amount,payment_date,interest_due_monthly){
	
	frm.add_child("repayment_schedule",{
		"payment_date":payment_date,
		"principal_amount":amount_due_monthly,
		"interest_amount":interest_due_monthly,
		"total_payment":amount_due_monthly+interest_due_monthly,
		"balance_loan_amount":balance_loan_amount,
	});
}



