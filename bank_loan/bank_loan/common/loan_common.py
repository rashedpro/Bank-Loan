from erpnext.loan_management.doctype.loan.loan import Loan,add_single_month
import frappe
import frappe
from frappe import _
from frappe.utils import (
	add_days,
	get_last_day,
    add_months,
    flt
)
class CustomLoan(Loan):
    #this code for version up to 13.40
    # def make_repayment_schedule(self):
    #     if not self.custome_repayment_schedule:
    #         if not self.repayment_start_date:
    #             frappe.throw(_("Repayment Start Date is mandatory for term loans"))

    #         schedule_type_details = frappe.db.get_value(
    #             "Loan Type", self.loan_type, ["repayment_schedule_type", "repayment_date_on"], as_dict=1)

    #         self.repayment_schedule = []
    #         payment_date = self.repayment_start_date
    #         balance_amount = self.loan_amount

    #         while balance_amount > 0:
    #             interest_amount, principal_amount, balance_amount, total_payment = self.get_amounts(
    #                 payment_date,
    #                 balance_amount,
    #                 schedule_type_details.repayment_schedule_type,
    #                 schedule_type_details.repayment_date_on,
    #             )

    #             if schedule_type_details.repayment_schedule_type == "Pro-rated calendar months":
    #                 next_payment_date = get_last_day(payment_date)
    #                 if schedule_type_details.repayment_date_on == "Start of the next month":
    #                     next_payment_date = add_days(next_payment_date, 1)

    #                 payment_date = next_payment_date

    #             self.add_repayment_schedule_row(
    #                 payment_date, principal_amount, interest_amount, total_payment, balance_amount
    #             )

    #             if (
    #                 schedule_type_details.repayment_schedule_type == "Monthly as per repayment start date"
    #                 or schedule_type_details.repayment_date_on == "End of the current month"
    #             ):
    #                 next_payment_date = add_single_month(payment_date)
    #                 payment_date = next_payment_date

    def make_repayment_schedule(self):
        if not self.custome_repayment_schedule:
            if not self.repayment_start_date:
                frappe.throw(_("Repayment Start Date is mandatory for term loans"))

                schedule_type_details = frappe.db.get_value(
                    "Loan Type", self.loan_type, ["repayment_schedule_type", "repayment_date_on"], as_dict=1
                )

                self.repayment_schedule = []
                payment_date = self.repayment_start_date
                balance_amount = self.loan_amount

                while balance_amount > 0:
                    interest_amount, principal_amount, balance_amount, total_payment = self.get_amounts(
                        payment_date,
                        balance_amount,
                        schedule_type_details.repayment_schedule_type,
                        schedule_type_details.repayment_date_on,
                    )

                    if schedule_type_details.repayment_schedule_type == "Pro-rated calendar months":
                        next_payment_date = get_last_day(payment_date)
                        if schedule_type_details.repayment_date_on == "Start of the next month":
                            next_payment_date = add_days(next_payment_date, 1)

                        payment_date = next_payment_date

                    self.add_repayment_schedule_row(
                        payment_date, principal_amount, interest_amount, total_payment, balance_amount
                    )

                    if (
                        schedule_type_details.repayment_schedule_type == "Monthly as per repayment start date"
                        or schedule_type_details.repayment_date_on == "End of the current month"
                    ):
                        next_payment_date = add_single_month(payment_date)
                        payment_date = next_payment_date