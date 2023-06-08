# Copyright (c) 2023, slnee and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from datetime import date,datetime,timedelta

import frappe

class ExternalBorrowing(Document):

	
	def calculate_interest(self,accounts):	

		interest_percent=self.rate_of_interest*0.01

		interest_amount=interest_percent*self.loan_amount

		accounts.append({
					"account": self.account_of_deferred_funding_cost,
					"credit": interest_amount,
					"credit_in_account_currency":interest_amount,
				})
		accounts.append({
				"account": self.cost_of_financing_account,
				"debit":interest_amount,
				"debit_in_account_currency":interest_amount,
				})	
				
		return accounts
	
	def create_loan(self):
		tmp_list=[]
		accounts=[]

		accounts.append({
						"account": self.lender_account,
						"credit": self.loan_amount,
						"credit_in_account_currency":self.loan_amount,
					})
				
		accounts.append({
					"account": self.bank_accounts,
					"debit":self.loan_amount,
					"debit_in_account_currency":self.loan_amount,
					})
		
		if self.rate_of_interest>0:
			accounts=self.calculate_interest(accounts)
		

		tmp_list = frappe.get_doc({
        "doctype": "Journal Entry",
        'voucher_type': 'Loan Entry',
		"title": "Loan From {} ".format(self.lender),	
        "posting_date":self.posting_date,
        "accounts": accounts,
		"user_remark":self.user_remark
		
		})
		if tmp_list:
			tmp_list.insert()			
			tmp_list.submit()
			self.jouranl_entery_reference=tmp_list.name
			
		
	def before_submit(self):
		self.create_loan()	

def make_interest(accounts,external_borrowing_list,child_obj):

	accounts.append({
					"account":external_borrowing_list["cost_of_financing_account"],
					"credit": child_obj["interest_amount"],
					"credit_in_account_currency":child_obj["interest_amount"],
				})
	accounts.append({
			"account":external_borrowing_list["account_of_deferred_funding_cost"],
			"debit":child_obj["interest_amount"],
			"debit_in_account_currency":child_obj["interest_amount"],
			})	
	
	accounts.append({
					"account":external_borrowing_list["bank_accounts"],
					"credit": child_obj["interest_amount"],
					"credit_in_account_currency":child_obj["interest_amount"],
				})
	
	accounts.append({
			"account":external_borrowing_list["interest_expense_account"],
			"debit":child_obj["interest_amount"],
			"debit_in_account_currency":child_obj["interest_amount"],
			})
	return accounts



def make_journal_entry(external_borrowing_list,child_obj):
	tmp_list=[]
	accounts=[]
	accounts.append({
					"account":external_borrowing_list["bank_accounts"],
					"credit": child_obj["principal_amount"],
					"credit_in_account_currency":child_obj["principal_amount"],
				})
			
	accounts.append({
				"account":external_borrowing_list["lender_account"],
				"debit":child_obj["principal_amount"],
				"debit_in_account_currency":int(child_obj["principal_amount"]),
				})
	
	if external_borrowing_list["rate_of_interest"]>0:
		accounts=make_interest(accounts,external_borrowing_list,child_obj)
	

	tmp_list = frappe.get_doc({
	"doctype": "Journal Entry",
	'voucher_type': 'Loan Repayment',
	"title": "Repay the Loan of  {} ".format(external_borrowing_list.lender),	
	"posting_date":date.today(),
	"accounts": accounts,
	"user_remark":"Repay the Loan of  {} ".format(external_borrowing_list.lender)
	
	})
	if tmp_list:
		tmp_list.insert()
		tmp_list.submit()
		tmp_obj = frappe.get_doc('Custom Repayment Schedule', child_obj["name"])
		tmp_obj.db_set("journal_entry",tmp_list.name,commit=True)
		tmp_obj.save()


def post_loan_entries():
	child_list=frappe.db.get_all("Custom Repayment Schedule",filters={"payment_date":str(date.today()),"docstatus":1},fields=["*"])
	for child_obj in child_list:
		if child_obj["journal_entry"]==None:
			external_borrowing_list=frappe.db.get_all("External Borrowing",filters={"name":child_obj["parent"]},fields=["*"])[0]
			make_journal_entry(external_borrowing_list,child_obj)
