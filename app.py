# app.py - Full Tkinter UI for MedicineInventory (requires db.py and MySQL server)
import tkinter as tk
from tkinter import ttk, messagebox
import db
from datetime import datetime

root = tk.Tk()
root.title("Medicine Inventory Management System")
root.geometry("1100x700")

tab_control = ttk.Notebook(root)
tabs = {}
for name in ["Doctor", "Disease", "Medicine", "Prescription", "Bill"]:
    frame = ttk.Frame(tab_control)
    tab_control.add(frame, text=name)
    tabs[name] = frame
tab_control.pack(expand=1, fill="both")

# ---------- DOCTOR TAB ----------
def load_doctors():
    for i in tree_doctors.get_children(): tree_doctors.delete(i)
    for row in db.fetch_all("Doctor"):
        tree_doctors.insert("", tk.END, values=row)

def on_doc_select(event=None):
    sel = tree_doctors.selection()
    if not sel: return
    vals = tree_doctors.item(sel[0])['values']
    ent_doc_id_var.set(vals[0])
    ent_doc_name.delete(0, tk.END); ent_doc_name.insert(0, vals[1])
    ent_doc_qual.delete(0, tk.END); ent_doc_qual.insert(0, vals[2] or "")
    ent_doc_spec.delete(0, tk.END); ent_doc_spec.insert(0, vals[3] or "")

def add_doctor():
    name = ent_doc_name.get().strip(); qual = ent_doc_qual.get().strip(); spec = ent_doc_spec.get().strip()
    if not name or not spec: messagebox.showerror("Error", "Name & Specialization required"); return
    db.insert_doctor(name, qual, spec); load_doctors(); clear_doc_form()

def update_doctor():
    did = ent_doc_id_var.get()
    if not did: messagebox.showerror("Error", "Select doctor first"); return
    db.update_doctor(did, ent_doc_name.get(), ent_doc_qual.get(), ent_doc_spec.get())
    load_doctors(); clear_doc_form()

def delete_doctor():
    sel = tree_doctors.selection()
    if not sel: return
    did = tree_doctors.item(sel[0])['values'][0]
    if messagebox.askyesno("Confirm", "Delete selected doctor?"):
        db.delete_row("Doctor", "doctor_id", did); load_doctors(); clear_doc_form()

def clear_doc_form():
    ent_doc_id_var.set("")
    ent_doc_name.delete(0, tk.END); ent_doc_qual.delete(0, tk.END); ent_doc_spec.delete(0, tk.END)

cols = ("ID","Name","Qualification","Specialization")
tree_doctors = ttk.Treeview(tabs["Doctor"], columns=cols, show="headings", height=12)
for c in cols: tree_doctors.heading(c, text=c)
tree_doctors.bind("<<TreeviewSelect>>", on_doc_select)
tree_doctors.pack(fill=tk.BOTH, padx=10, pady=10)

frm_doc = tk.Frame(tabs["Doctor"]); frm_doc.pack(padx=10, pady=5, fill=tk.X)
ent_doc_id_var = tk.StringVar()
tk.Label(frm_doc, text="ID").grid(row=0,column=0); tk.Entry(frm_doc, textvariable=ent_doc_id_var, state="readonly").grid(row=0,column=1)
tk.Label(frm_doc, text="Name").grid(row=0,column=2); ent_doc_name = tk.Entry(frm_doc); ent_doc_name.grid(row=0,column=3)
tk.Label(frm_doc, text="Qualification").grid(row=1,column=0); ent_doc_qual = tk.Entry(frm_doc); ent_doc_qual.grid(row=1,column=1)
tk.Label(frm_doc, text="Specialization").grid(row=1,column=2); ent_doc_spec = tk.Entry(frm_doc); ent_doc_spec.grid(row=1,column=3)
tk.Button(frm_doc, text="Add", command=add_doctor).grid(row=0,column=4,padx=5)
tk.Button(frm_doc, text="Update", command=update_doctor).grid(row=0,column=5,padx=5)
tk.Button(frm_doc, text="Delete", command=delete_doctor).grid(row=0,column=6,padx=5)
tk.Button(frm_doc, text="Clear", command=clear_doc_form).grid(row=0,column=7,padx=5)
load_doctors()

# ---------- DISEASE TAB ----------
def load_diseases():
    for i in tree_disease.get_children(): tree_disease.delete(i)
    for row in db.fetch_all("Disease"): tree_disease.insert("", tk.END, values=row)

def on_dis_select(event=None):
    sel = tree_disease.selection()
    if not sel: return
    vals = tree_disease.item(sel[0])['values']
    ent_dis_id_var.set(vals[0])
    ent_dis_name.delete(0, tk.END); ent_dis_name.insert(0, vals[1])
    ent_dis_type.set(vals[2])

def add_disease():
    name = ent_dis_name.get().strip(); dtype = ent_dis_type.get()
    if not name or not dtype: messagebox.showerror("Error", "All fields required"); return
    db.insert_disease(name, dtype); load_diseases(); clear_dis_form()
    # Refresh disease combobox in Medicine tab
    ent_med_disease['values'] = [r[0] for r in db.fetch_all("Disease")]

def update_disease():
    did = ent_dis_id_var.get()
    if not did: messagebox.showerror("Error", "Select disease first"); return
    db.update_disease(did, ent_dis_name.get(), ent_dis_type.get()); load_diseases(); clear_dis_form()
    ent_med_disease['values'] = [r[0] for r in db.fetch_all("Disease")]

def delete_disease():
    sel = tree_disease.selection()
    if not sel: return
    did = tree_disease.item(sel[0])['values'][0]
    if messagebox.askyesno("Confirm","Delete disease?"): db.delete_row("Disease","disease_id",did); load_diseases(); clear_dis_form()
    ent_med_disease['values'] = [r[0] for r in db.fetch_all("Disease")]

def clear_dis_form():
    ent_dis_id_var.set(""); ent_dis_name.delete(0,tk.END); ent_dis_type.set("")

cols = ("ID","Name","Type")
tree_disease = ttk.Treeview(tabs["Disease"], columns=cols, show="headings", height=12)
for c in cols: tree_disease.heading(c, text=c)
tree_disease.bind("<<TreeviewSelect>>", on_dis_select)
tree_disease.pack(fill=tk.BOTH, padx=10, pady=10)

frm_dis = tk.Frame(tabs["Disease"]); frm_dis.pack(padx=10,pady=5,fill=tk.X)
ent_dis_id_var = tk.StringVar()
tk.Label(frm_dis,text="ID").grid(row=0,column=0); tk.Entry(frm_dis,textvariable=ent_dis_id_var,state="readonly").grid(row=0,column=1)
tk.Label(frm_dis,text="Name").grid(row=0,column=2); ent_dis_name = tk.Entry(frm_dis); ent_dis_name.grid(row=0,column=3)
tk.Label(frm_dis,text="Type").grid(row=1,column=0); ent_dis_type = ttk.Combobox(frm_dis, values=["infectious","deficiency","genetic hereditary","non-genetic hereditary"]); ent_dis_type.grid(row=1,column=1)
tk.Button(frm_dis,text="Add",command=add_disease).grid(row=0,column=4,padx=5)
tk.Button(frm_dis,text="Update",command=update_disease).grid(row=0,column=5,padx=5)
tk.Button(frm_dis,text="Delete",command=delete_disease).grid(row=0,column=6,padx=5)
tk.Button(frm_dis,text="Clear",command=clear_dis_form).grid(row=0,column=7,padx=5)
load_diseases()

# ---------- MEDICINE TAB ----------
def load_medicines():
    for i in tree_medicine.get_children(): tree_medicine.delete(i)
    rows = db.fetch_all("Medicine")
    for r in rows: tree_medicine.insert("", tk.END, values=r)

def on_med_select(event=None):
    sel = tree_medicine.selection()
    if not sel: return
    vals = tree_medicine.item(sel[0])['values']
    ent_med_id_var.set(vals[0])
    ent_med_name.delete(0,tk.END); ent_med_name.insert(0, vals[1])
    ent_med_mfg.delete(0,tk.END); ent_med_mfg.insert(0, vals[2])
    ent_med_exp.delete(0,tk.END); ent_med_exp.insert(0, vals[3])
    ent_med_price.delete(0,tk.END); ent_med_price.insert(0, vals[4])
    ent_med_dosage.delete(0,tk.END); ent_med_dosage.insert(0, vals[5])
    ent_med_disease.set(vals[6])

def add_medicine():
    try:
        db.insert_medicine(ent_med_name.get(), ent_med_mfg.get(), ent_med_exp.get(),
                           float(ent_med_price.get()), ent_med_dosage.get(), int(ent_med_disease.get()))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add medicine: {e}")
        return
    load_medicines(); clear_med_form()
    ent_presc_med['values'] = [r[0] for r in db.fetch_all("Medicine")]

def update_medicine():
    mid = ent_med_id_var.get()
    if not mid: messagebox.showerror("Error","Select medicine first"); return
    try:
        db.update_medicine(mid, ent_med_name.get(), ent_med_mfg.get(), ent_med_exp.get(),
                           float(ent_med_price.get()), ent_med_dosage.get(), int(ent_med_disease.get()))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update medicine: {e}"); return
    load_medicines(); clear_med_form()
    ent_presc_med['values'] = [r[0] for r in db.fetch_all("Medicine")]

def delete_medicine():
    sel = tree_medicine.selection()
    if not sel: return
    mid = tree_medicine.item(sel[0])['values'][0]
    if messagebox.askyesno("Confirm","Delete medicine?"): db.delete_row("Medicine","medicine_id",mid); load_medicines(); clear_med_form()
    ent_presc_med['values'] = [r[0] for r in db.fetch_all("Medicine")]

def clear_med_form():
    ent_med_id_var.set(""); ent_med_name.delete(0,tk.END); ent_med_mfg.delete(0,tk.END); ent_med_exp.delete(0,tk.END)
    ent_med_price.delete(0,tk.END); ent_med_dosage.delete(0,tk.END); ent_med_disease.set("")

cols = ("ID","Name","Mfg_Date","Exp_Date","Price","Dosage","Disease_ID")
tree_medicine = ttk.Treeview(tabs["Medicine"], columns=cols, show="headings", height=12)
for c in cols: tree_medicine.heading(c, text=c)
tree_medicine.bind("<<TreeviewSelect>>", on_med_select)
tree_medicine.pack(fill=tk.BOTH, padx=10, pady=10)

frm_med = tk.Frame(tabs["Medicine"]); frm_med.pack(padx=10,pady=5,fill=tk.X)
ent_med_id_var = tk.StringVar()
tk.Label(frm_med,text="ID").grid(row=0,column=0); tk.Entry(frm_med,textvariable=ent_med_id_var,state="readonly").grid(row=0,column=1)
tk.Label(frm_med,text="Name").grid(row=0,column=2); ent_med_name = tk.Entry(frm_med); ent_med_name.grid(row=0,column=3)
tk.Label(frm_med,text="Mfg (YYYY-MM-DD)").grid(row=1,column=0); ent_med_mfg = tk.Entry(frm_med); ent_med_mfg.grid(row=1,column=1)
tk.Label(frm_med,text="Exp (YYYY-MM-DD)").grid(row=1,column=2); ent_med_exp = tk.Entry(frm_med); ent_med_exp.grid(row=1,column=3)
tk.Label(frm_med,text="Price").grid(row=2,column=0); ent_med_price = tk.Entry(frm_med); ent_med_price.grid(row=2,column=1)
tk.Label(frm_med,text="Dosage").grid(row=2,column=2); ent_med_dosage = tk.Entry(frm_med); ent_med_dosage.grid(row=2,column=3)
tk.Label(frm_med,text="Disease_ID").grid(row=2,column=4); ent_med_disease = ttk.Combobox(frm_med, values=[r[0] for r in db.fetch_all("Disease")]); ent_med_disease.grid(row=2,column=5)
tk.Button(frm_med,text="Add",command=add_medicine).grid(row=0,column=6,padx=5)
tk.Button(frm_med,text="Update",command=update_medicine).grid(row=0,column=7,padx=5)
tk.Button(frm_med,text="Delete",command=delete_medicine).grid(row=1,column=6,padx=5)
tk.Button(frm_med,text="Clear",command=clear_med_form).grid(row=1,column=7,padx=5)
load_medicines()

# ---------- PRESCRIPTION TAB ----------
def load_prescriptions():
    for i in tree_presc.get_children(): tree_presc.delete(i)
    for r in db.fetch_prescriptions_with_details():
        tree_presc.insert("", tk.END, values=r)

def on_presc_select(event=None):
    sel = tree_presc.selection()
    if not sel: return
    vals = tree_presc.item(sel[0])['values']
    ent_presc_id_var.set(vals[0]); ent_presc_doctor.set(vals[1]); ent_presc_patient.delete(0,tk.END); ent_presc_patient.insert(0, vals[2])
    ent_presc_date.delete(0,tk.END); ent_presc_date.insert(0, vals[3])
    load_presc_details(vals[0])

def load_presc_details(presc_id):
    for i in tree_presc_details.get_children(): tree_presc_details.delete(i)
    for d in db.fetch_prescription_details(presc_id):
        tree_presc_details.insert("", tk.END, values=d)

def add_prescription():
    try:
        doctor_id = int(ent_presc_doctor_id.get())
        patient = ent_presc_patient.get().strip()
        date = ent_presc_date.get().strip() or datetime.today().strftime("%Y-%m-%d")
        pid = db.insert_prescription(doctor_id, patient, date)
        # optionally add details if provided
        if ent_presc_med.get() and ent_presc_qty.get():
            db.insert_prescription_detail(pid, int(ent_presc_med.get()), int(ent_presc_qty.get()))
        load_prescriptions(); clear_presc_form()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add prescription: {e}")

def add_presc_detail_to_selected():
    pid = ent_presc_id_var.get()
    if not pid: messagebox.showerror("Error","Select or add prescription first"); return
    try:
        db.insert_prescription_detail(int(pid), int(ent_presc_med.get()), int(ent_presc_qty.get()))
        load_presc_details(int(pid)); load_prescriptions()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add detail: {e}")

def delete_prescription():
    sel = tree_presc.selection()
    if not sel: return
    pid = tree_presc.item(sel[0])['values'][0]
    if messagebox.askyesno("Confirm","Delete prescription?"): db.delete_row("Prescription","prescription_id",pid); load_prescriptions(); load_presc_details(0)

def clear_presc_form():
    ent_presc_id_var.set(""); ent_presc_doctor_id.delete(0,tk.END); ent_presc_doctor.set(""); ent_presc_patient.delete(0,tk.END); ent_presc_date.delete(0,tk.END)
    for i in tree_presc_details.get_children(): tree_presc_details.delete(i)

cols = ("ID","Doctor","Patient","Date")
tree_presc = ttk.Treeview(tabs["Prescription"], columns=cols, show="headings", height=8)
for c in cols: tree_presc.heading(c, text=c)
tree_presc.bind("<<TreeviewSelect>>", on_presc_select)
tree_presc.pack(fill=tk.BOTH, padx=10, pady=10)

frm_presc = tk.Frame(tabs["Prescription"]); frm_presc.pack(padx=10,pady=5,fill=tk.X)
ent_presc_id_var = tk.StringVar()
tk.Label(frm_presc,text="ID").grid(row=0,column=0); tk.Entry(frm_presc,textvariable=ent_presc_id_var,state="readonly").grid(row=0,column=1)
tk.Label(frm_presc,text="Doctor_ID").grid(row=0,column=2); ent_presc_doctor_id = tk.Entry(frm_presc); ent_presc_doctor_id.grid(row=0,column=3)
tk.Label(frm_presc,text="Doctor (name)").grid(row=0,column=4); ent_presc_doctor = tk.Entry(frm_presc); ent_presc_doctor.grid(row=0,column=5)
tk.Label(frm_presc,text="Patient").grid(row=1,column=0); ent_presc_patient = tk.Entry(frm_presc); ent_presc_patient.grid(row=1,column=1)
tk.Label(frm_presc,text="Date").grid(row=1,column=2); ent_presc_date = tk.Entry(frm_presc); ent_presc_date.grid(row=1,column=3)
tk.Label(frm_presc,text="Med_ID").grid(row=2,column=0); ent_presc_med = ttk.Combobox(frm_presc, values=[r[0] for r in db.fetch_all("Medicine")]); ent_presc_med.grid(row=2,column=1)
tk.Label(frm_presc,text="Qty").grid(row=2,column=2); ent_presc_qty = tk.Entry(frm_presc); ent_presc_qty.grid(row=2,column=3)
tk.Button(frm_presc,text="Add Prescription",command=add_prescription).grid(row=0,column=6,padx=5)
tk.Button(frm_presc,text="Add Detail",command=add_presc_detail_to_selected).grid(row=1,column=6,padx=5)
tk.Button(frm_presc,text="Delete Presc",command=delete_prescription).grid(row=0,column=7,padx=5)
tk.Button(frm_presc,text="Clear",command=clear_presc_form).grid(row=1,column=7,padx=5)

# Prescription details tree
cols_det = ("Prescription_ID","Med_ID","Med_Name","Qty","Price")
tree_presc_details = ttk.Treeview(tabs["Prescription"], columns=cols_det, show="headings", height=6)
for c in cols_det: tree_presc_details.heading(c, text=c)
tree_presc_details.pack(fill=tk.BOTH, padx=10, pady=5)

load_prescriptions()

# ---------- BILL TAB ----------
def load_bills():
    for i in tree_bill.get_children(): tree_bill.delete(i)
    for row in db.fetch_all("Bill"):
        tree_bill.insert("", tk.END, values=row)

def on_bill_select(event=None):
    sel = tree_bill.selection()
    if not sel: return
    vals = tree_bill.item(sel[0])['values']
    ent_bill_id_var.set(vals[0]); ent_bill_presc_id.delete(0,tk.END); ent_bill_presc_id.insert(0, vals[1])
    ent_bill_tax.delete(0,tk.END); ent_bill_tax.insert(0, vals[2])
    ent_bill_discount.delete(0,tk.END); ent_bill_discount.insert(0, vals[3])
    ent_bill_total.delete(0,tk.END); ent_bill_total.insert(0, vals[4])

def create_bill_from_presc():
    pid = ent_bill_presc_id.get()
    if not pid: messagebox.showerror("Error","Provide prescription id"); return
    calc = db.calculate_bill_for_prescription(int(pid))
    ent_bill_total.delete(0,tk.END); ent_bill_total.insert(0, str(calc["total"]))
    ent_bill_tax.delete(0,tk.END); ent_bill_tax.insert(0, str(calc["tax"]))
    ent_bill_discount.delete(0,tk.END); ent_bill_discount.insert(0, str(calc["discount"]))

def add_bill():
    try:
        pid = int(ent_bill_presc_id.get()); tax = float(ent_bill_tax.get()); disc = float(ent_bill_discount.get()); total = float(ent_bill_total.get())
        db.insert_bill(pid, tax, disc, total); load_bills(); clear_bill_form()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add bill: {e}")

def delete_bill():
    sel = tree_bill.selection()
    if not sel: return
    bid = tree_bill.item(sel[0])['values'][0]
    if messagebox.askyesno("Confirm","Delete bill?"): db.delete_row("Bill","bill_id",bid); load_bills(); clear_bill_form()

def clear_bill_form():
    ent_bill_id_var.set(""); ent_bill_presc_id.delete(0,tk.END); ent_bill_tax.delete(0,tk.END); ent_bill_discount.delete(0,tk.END); ent_bill_total.delete(0,tk.END)

cols = ("Bill_ID","Prescription_ID","Tax","Discount","Total")
tree_bill = ttk.Treeview(tabs["Bill"], columns=cols, show="headings", height=12)
for c in cols: tree_bill.heading(c, text=c)
tree_bill.bind("<<TreeviewSelect>>", on_bill_select)
tree_bill.pack(fill=tk.BOTH, padx=10, pady=10)

frm_bill = tk.Frame(tabs["Bill"]); frm_bill.pack(padx=10,pady=5,fill=tk.X)
ent_bill_id_var = tk.StringVar()
tk.Label(frm_bill,text="ID").grid(row=0,column=0); tk.Entry(frm_bill,textvariable=ent_bill_id_var,state="readonly").grid(row=0,column=1)
tk.Label(frm_bill,text="Prescription_ID").grid(row=0,column=2); ent_bill_presc_id = tk.Entry(frm_bill); ent_bill_presc_id.grid(row=0,column=3)
tk.Label(frm_bill,text="Tax").grid(row=1,column=0); ent_bill_tax = tk.Entry(frm_bill); ent_bill_tax.grid(row=1,column=1)
tk.Label(frm_bill,text="Discount").grid(row=1,column=2); ent_bill_discount = tk.Entry(frm_bill); ent_bill_discount.grid(row=1,column=3)
tk.Label(frm_bill,text="Total").grid(row=1,column=4); ent_bill_total = tk.Entry(frm_bill); ent_bill_total.grid(row=1,column=5)
tk.Button(frm_bill,text="Calc From Prescription",command=create_bill_from_presc).grid(row=0,column=4,padx=5)
tk.Button(frm_bill,text="Add Bill",command=add_bill).grid(row=0,column=5,padx=5)
tk.Button(frm_bill,text="Delete Bill",command=delete_bill).grid(row=0,column=6,padx=5)
tk.Button(frm_bill,text="Clear",command=clear_bill_form).grid(row=0,column=7,padx=5)

load_bills()

root.mainloop()
