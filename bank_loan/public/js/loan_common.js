frappe.ui.form.on('Loan',{
    refresh(frm){
        if(frm.doc.repayment_schedule && frm.doc.custome_repayment_schedule){
            frm.set_df_property("repayment_schedule", "read_only", 0);
        }
    },
    before_submit(frm){
        let repayment_schedule=frm.doc.repayment_schedule.reduce((accumulator,current_item)=>{ 
            const {principal_amount,balance_loan_amount}=current_item
            accumulator.total_principal_amount+=principal_amount;
            accumulator.total_balance_loan_amount-=balance_loan_amount;
            return accumulator
        },{
            total_principal_amount:0,
            total_balance_loan_amount:frm.doc.loan_amount
        });


        if(repayment_schedule.total_principal_amount!==frm.doc.loan_amount && repayment_schedule.total_balance_loan_amount!==0){
        frappe.throw(__(`Total Principal Amount shold be ${frm.doc.loan_amount}, And Total of balance loan amount=${0}`));
        }
    },
    custome_repayment_schedule(frm){
        if(frm.doc.custome_repayment_schedule){
            frm.doc.repayment_schedule=[];
            frm.set_df_property("repayment_schedule", "read_only", 0);
        }else{
            frm.set_df_property("repayment_schedule", "read_only", 1);
        }
        frm.refresh_field("repayment_schedule");   
    }
});

frappe.ui.form.on("Repayment Schedule", {
    payment_date:function(frm,cdt,cdn){
        let d=locals[cdt][cdn];
        let repayment_start_date=frm.doc.repayment_start_date;
        repayment_start_date=new Date(repayment_start_date);
        let payment_date=new Date(d.payment_date);
        if(repayment_start_date.getTime()>payment_date.getTime()){
            frappe.model.set_value(cdt,cdn,"payment_date",frappe.datetime.add_months(frm.doc.repayment_start_date, 1)).then(()=>{
                frappe.throw(__(`Payment Date should be after ${frm.doc.repayment_start_date}`));
            })
        }
    },
    principal_amount:function(frm,cdt,cdn){

        let d=locals[cdt][cdn];
        frappe.model.set_value(cdt,cdn,"total_payment",d.principal_amount+d.interest_amount).then(()=>{
            if(d.idx===1){
                frappe.model.set_value(cdt,cdn,"balance_loan_amount",frm.doc.loan_amount-d.total_payment);
            }else{
                frappe.model.set_value(cdt,cdn,"balance_loan_amount",frm.doc.repayment_schedule[d.idx-2].balance_loan_amount-d.total_payment);
            }

        })
    },
});


