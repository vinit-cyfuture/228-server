# Code on before validate event, script type is doctype event

# if doc.gst_tds and not doc.gst_tds_category:
#     frappe.throw("Please select Tax Categoty")
# if doc.gst_tds and not doc.gst_percentage:
#     frappe.throw("Please select GST %")
if doc.custom_is_outsourcing and doc.currency=="INR":
    doc.custom_gst_credit_to = frappe.db.get_value("Unit",doc.unit,'custom_gst_credit_to')
# else:
#     doc.gst_credit_to = frappe.db.get_value("Company",doc.company,'gst_credit_account')

# Check if GST TDS checkbox & GST TDS Category based on that append rows in taxes table
# If SGST, CGST then 1% is applied, if IGST then 2% is applied and labour cess percentage is taken from Labour cess field
# CGST, SGST, IGST TDS and labour cess is deducted on Actual
if doc.custom_gst_tds==1:
    if doc.custom_gst_tds_category=="In State":
        if not frappe.db.exists("Purchase Taxes and Charges",{"parent":doc.name,"custom_cgst_tds": 1}):
            doc.append("taxes",{
                "description" :"CGST-TDS",
                "charge_type":"Actual",
                "account_head":doc.custom_cgst_tds_account,
                "custom_rate": 1,
                "custom_cgst_tds": 1,
                "add_deduct_tax": "Deduct",
                "category":"Total",
                "cost_center": doc.cost_center,
                "country": doc.country,
                "state": doc.state,
                "tax_amount": round((doc.total)*(1/100))
            })
        if not frappe.db.exists("Purchase Taxes and Charges",{"parent":doc.name,"custom_sgst_tds": 1}):
            doc.append("taxes",{
                "description":"SGST-TDS",
                "charge_type": "Actual",
                "account_head":doc.custom_sgst_tds_account,
                "custom_rate":1,
                "custom_sgst_tds":1,
                "add_deduct_tax": "Deduct",
                "category":"Total",
                "cost_center": doc.cost_center,
                "country": doc.country,
                "state": doc.state,
                "tax_amount": round((doc.total)*(1/100))
            })
    else:
        if not frappe.db.exists("Purchase Taxes and Charges",{"parent":doc.name,"custom_igst_tds": 1}):
            doc.append("taxes",{
                "description": "IGST-TDS",
                "charge_type": "Actual",
                "account_head":doc.custom_igst_tds_account,
                "custom_rate":2,
                "custom_igst_tds": 1,
                "add_deduct_tax": "Deduct",
                "category":"Total",
                "cost_center": doc.cost_center,
                "country": doc.country,
                "state": doc.state,
                "tax_amount": round((doc.total)*(2/100))
            })

if doc.custom_retention_percentage != 'Nil' and doc.custom_retention_percentage_account:
    if not frappe.db.exists("Purchase Taxes and Charges",{"parent":doc.name,"custom_retention": 1}):
        # id = frappe.db.get_value("Purchase Taxes and Charges",{"parent":doc.name,"description":"Retention Percentage"},'name')
        # frappe.delete_doc("Purchase Taxes and Charges",id)
        doc.append("taxes",{
            "description":"Retention Percentage",
            "charge_type": "Actual",
            "custom_retention": 1,
            "account_head":doc.custom_retention_percentage_account,
            "rate": doc.custom_retention_percentage,
            "add_deduct_tax":"Deduct",
            "category":"Total",
            "cost_center":doc.cost_center,
            "tax_amount": round((doc.total)*(float(doc.custom_retention_percentage)/100))
            # "total":(doc.total+(doc.total/100)*float(doc.retention_percentage))
        })
if doc.custom_labour_cess != 'Nil' and doc.custom_labour_cess_account:
    if not frappe.db.exists("Purchase Taxes and Charges",{"parent":doc.name,"custom_labour_cess": 1}):
        doc.append("taxes",{
            "description":"Labour Cess",
            "charge_type": "Actual",
            "account_head": doc.custom_labour_cess_account,
            "custom_labour_cess": 1,
            "custom_rate": doc.custom_labour_cess,
            "add_deduct_tax": "Deduct",
            "category": "Total",
            "cost_center": doc.cost_center,
            "country": doc.country,
            "state": doc.state,
            "tax_amount": round((doc.total)*(float(doc.custom_labour_cess)/100))
        })