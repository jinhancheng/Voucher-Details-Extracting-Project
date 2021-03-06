import pandas as pd

def read_xml(file):
    with open(file, encoding = "ISO-8859-1") as myfile:
        location = []
        description = []
        x = []
        y = []
        for line in myfile:
            if line[:5] == "<text":
                description.append(line.split(">")[1][:-6])
                x.append(int(line.split(">")[0].split()[2][6:-1]))
                y.append(int(line.split(">")[0].split()[1][5:-1]))                
            if line[:7] == "</page>":
                location.append([description, x, y])
                description = []
                x = []
                y = []
    A = []
    for i in range(0, len(location)):
        data = pd.DataFrame({'description':location[i][0], 'x':location[i][1], 'y':location[i][2]}).sort_values(by=['y', 'x']).reset_index(drop=True)
        A.append(data)
    return A

A = read_xml('sample_currency.xml')

D = []
Payment = []
Frames = []
for i in range(0, len(A)):
    B = {}
    C = {}
    if A[i]['description'][0] == "Property Clerk Invoice":
        Invoice_No = A[i]['description'][2]
        #dict
        B.update({"Invoice Number": Invoice_No})
        for j in range(0, A[i].shape[0]):
## Invoice

            if A[i]['description'][j] == "Invoicing Command":
                Invocing_Command = A[i]['description'][j+2]
                Invoice_Status = A[i]['description'][j+3]
                #dict
                B.update({"Invoicing Command": Invocing_Command})
                B.update({"Invoice Status": Invoice_Status})
            if A[i]['description'][j] == "Invoice Date":
                Invoice_Date = A[i]['description'][j+3]
                Property_Type = A[i]['description'][j+4]
                Property_Category = A[i]['description'][j+5]
                #dict
                B.update({"Invoice Date": Invoice_Date})
                B.update({"Property Type": Property_Type})
                B.update({"Property Category": Property_Category})
            if A[i]['description'][j] == "Officers":
                if A[i]['description'][j+5] == "Invoicing":
                    Invoicing_Officer_Tax_No = A[i]['description'][j+3]
                    Invoicing_Officer_Command = A[i]['description'][j+4]
#                    Invoicing = {"Tax No.": A[i]['description'][j+3], "Command": A[i]['description'][j+4]}
                else:
                    Invoicing_Officer_Tax_No = None
                    Invoicing_Officer_Command = None                    
#                    Invoicing = {"Tax No.": None, "Command": None}
                if A[i]['description'][j+8] == "Arresting" or A[i]['description'][j+6] == "Arresting":
                    if A[i]['description'][j+8] == "Arresting":
                        Arresting_Officer_Tax_No = A[i]['description'][j+6]
                        Arresting_Officer_Command = A[i]['description'][j+7]                        
#                        Arresting = {"Tax No.": A[i]['description'][j+6], "Command": A[i]['description'][j+7]}
                    if A[i]['description'][j+6] == "Arresting":
                        Arresting_Officer_Tax_No = None
                        Arresting_Officer_Command = None                        
#                        Arresting = {"Tax No.": None, "Command": None}
                #dict
#                Officers = {"Invoicing": Invoicing, "Arresting": Arresting}
#                B.update({"Officers": Officers})
                B.update({"Invoicing Officer Tax No.": Invoicing_Officer_Tax_No, "Invoicing Officer Command": Invoicing_Officer_Command, "Arresting Officer Tax No.": Arresting_Officer_Tax_No, "Arresting Officer Command": Arresting_Officer_Command})
            if A[i]['description'][j] == "Total Cash Value":
                Total_Cash_Value = A[i]['description'][j-1]
                B.update({"Total Cash Value": Total_Cash_Value})
            if A[i]['description'][j] == "Date Of Incident":
                if A[i]['description'][j+8] == "Prisoner(s)":
                    Date_Of_Incident = A[i]['description'][j+4][0:10]
                    Penal_Code = A[i]['description'][j+4][10:-1].lstrip()
                    Crime_Classification = A[i]['description'][j+5]
                    Related_To = A[i]['description'][j+6]
                    Receipt = A[i]['description'][j+7]
                else:
                    Date_Of_Incident = A[i]['description'][j+4][0:10]
                    Penal_Code = A[i]['description'][j+4][10:-1].lstrip()
                    Crime_Classification = None
                    Related_To = A[i]['description'][j+5]
                    Receipt = A[i]['description'][j+6]
                #dict
                if Penal_Code == "":
                    Penal_Code = None
                B.update({"Date Of Incident": Date_Of_Incident})
                B.update({"Penal Code/Description": Penal_Code})
                B.update({"Crime Classification": Crime_Classification})
                B.update({"Related To": Related_To})
                B.update({"Receipt": Receipt})
            if A[i]['description'][j] == "Prisoner(s)":
                if A[i][A[i]['x'] == 69].shape[0] != 0:
                    Prisoners = max([int(i) for i in list(A[i][A[i]['x'] == 69]['description'])])
                else:
                    Prisoners = None
                #dict
                B.update({"Prisoner(s)": Prisoners})
            if A[i]['description'][j] == "Related Invoice(s)":
                Related_Invoices = A[i]['description'][j-1]
                #dict
                B.update({"Related Invoice(s)": Related_Invoices})
## Approval
            if A[i]['description'][j] == "Approvals":
#                Entered_By = {"Tax No.": A[i]['description'][j+5], "Command": A[i]['description'][j+6], "Date": A[i]['description'][j+7], "Time": A[i]['description'][j+8]}
#                Invoicing_Officer = {"Tax No.": A[i]['description'][j+10], "Command": A[i]['description'][j+11], "Date": A[i]['description'][j+12], "Time": A[i]['description'][j+13]}
#                Approved_By = {"Tax No.": A[i]['description'][j+15], "Command": A[i]['description'][j+16], "Date": A[i]['description'][j+17], "Time": A[i]['description'][j+18]}
                #dict
#                Approvals = {"Enter By": Entered_By, "Invoicing Officer": Invoicing_Officer, "Approved By": Approved_By}
#                B.update({"Approvals": Approvals})
                B.update({"Entered By Tax No.": A[i]['description'][j+5]})
                B.update({"Entered By Command": A[i]['description'][j+6]})
                B.update({"Entered By Date": A[i]['description'][j+7]})
                B.update({"Entered By Time": A[i]['description'][j+8]})
                B.update({"Invoicing Officer Tax No.": A[i]['description'][j+10]})
                B.update({"Invoicing Officer Command": A[i]['description'][j+11]})
                B.update({"Invoicing Officer Date": A[i]['description'][j+12]})
                B.update({"Invoicing Officer Time": A[i]['description'][j+13]})
                B.update({"Approved By Tax No.": A[i]['description'][j+15]})
                B.update({"Approved By Command": A[i]['description'][j+16]})
                B.update({"Approved By Date": A[i]['description'][j+17]})
                B.update({"Approved By Time": A[i]['description'][j+18]})    
## Item  
            if A[i]['description'][j] == "Item" and A[i]['description'][j+6] == "Disposition":
                a = int((A[i].loc[A[i]['description'] == "Item"]).index.values)
                b = int((A[i].loc[A[i]['description'] == "Receipt"]).index.values)
                A_n = A[i][a+7:b-2].sort_values(by=['x','y']).reset_index(drop=True)
                A_m = A_n.sort_values(by=['y','x']).reset_index(drop=True)
                Item = A_m[A_m['x'] <= 81]["description"].reset_index(drop=True)
                Total_QTY = A_m[(A_m['x'] > 81) & (A_m['x'] <= 122)]["description"].reset_index(drop=True)
                Articles = A_n[(A_n['x'] == 162) & (A_n['y'].isin(list(A_n[A_n['x']<=81]["y"])))]["description"].reset_index(drop=True)
                Description = A_n[A_n['x'] == 162].reset_index(drop=True)
                for k in range(0, Description.shape[0]):
                    if Description['y'][k] in list(A_n[A_n['x']<=81]["y"]):
                        Description['description'][k] = "?"
                Description = (" ".join(list(Description['description']))).split("? ")[1:]
                Cash = A_n[(A_n['x'] > 162) & (A_n['x'] < 638)]["description"].reset_index(drop=True)           
                Cash = [i.split()[0] for i in list(Cash)]
                Disposition = [None] * len(Item)
                if len(A_n[A_n['x'] >= 702]["description"]) != 0:
                    disposition = A_n[A_n['x'] >= 702].sort_values(by=['y','x']).reset_index(drop=True)
                    for k in range(1, disposition.shape[0]):
                        if disposition['x'][k] == 702:
                            replace = " ".join([disposition['description'][k-1], disposition['description'][k]])
                            disposition['description'][k-1] = replace
                    disposition = list(disposition[disposition['x'] == 708]['description'])
                    disposition_y = list(A_n[A_n['x'] == 708]["y"])
                    if len(Item) == 1:
                        Disposition[0] = disposition[0]
                    else:
                        for ki in range(1, len(Item)):
                            for kj in range(0, len(disposition_y)):
                                if disposition_y[kj] >= list(A_n[A_n['x']==81]["y"])[ki-1] and disposition_y[kj] < list(A_n[A_n['x']==81]["y"])[ki]:
                                    Disposition[ki-1] = disposition[kj]  
                        if disposition_y[-1] >= list(A_n[A_n['x']==81]["y"])[-1]:
                            Disposition[-1] = disposition[-1]
                Frames.append(pd.DataFrame({'Invoice Number': Invoice_No, 'Item': list(Item), "Total QTY": list(Total_QTY), "Articles": list(Articles), "Description": Description, "Cash": Cash, "Disposition": Disposition}))        
        
        D.append(B) 
## Payment         
    if A[i]['description'][0] == "RTO Cash - Payment Voucher":
        Invoice_No = A[i]['description'][1]
        Transaction_Date = A[i]['description'][6]
        for j in range(0, A[i].shape[0]):
            if A[i]['description'][j] == "Item":
                a = int((A[i].loc[A[i]['description'] == "Item"]).index.values)
                b = int((A[i].loc[A[i]['description'] == "Total Amount in Invoice"]).index.values)
                A_n = A[i][a+4:b-1].sort_values(by=['x','y']).reset_index(drop=True)
                A_m = A_n.sort_values(by=['y','x']).reset_index(drop=True)
                Item = A_m[A_m['x'] <= 55]["description"].reset_index(drop=True)
                Quantity = A_m[(A_m['x'] > 590) & (A_m['x'] <= 621)]["description"].reset_index(drop=True)
                Article_Description = list(A_n[A_n['x'] == 183]['description'])
                Actual_amt_value = list(A_m[A_m['x'] > 621]["description"].reset_index(drop=True))
            if A[i]['description'][j] == "Returning Officer":
                Tax_No = A[i]['description'][j+5]
                Command = A[i]['description'][j+6]
                Date = A[i]['description'][j+7]
                Time = A[i]['description'][j+8]
        Payment.append(pd.DataFrame({'Invoice Number': Invoice_No, 'Transaction Date': Transaction_Date, 'Returning Officer Tax No.': Tax_No, 'Returning Officer Command': Command, 'Return Date': Date, 'Return Time': Time, 'Item (Number)': list(Item), "Returning Article Description": Article_Description, "Return Quantity": list(Quantity), "Actual amt value": Actual_amt_value}))
        
for i in range(0, len(D)-1):
    if D[i]["Invoice Number"] == D[i+1]["Invoice Number"]:
        D[i].update(D[i+1])
D_n = []
for i in range(0, len(D)):
    if len(D[i]) == 28:
        D_n.append(D[i])
        
General_Frame = pd.DataFrame(D_n)
General_Order = ['Invoice Number', 'Invoice Status', 'Invoice Date', 'Invoicing Command', 'Property Type', 'Property Category', 'Invoicing Officer Tax No.', 'Invoicing Officer Command', 'Arresting Officer Tax No.', 'Arresting Officer Command',"Total Cash Value", 'Date Of Incident', 'Penal Code/Description', 'Crime Classification', 'Related To', 'Receipt', 'Related Invoice(s)', 'Prisoner(s)']
Invoice_Frame = General_Frame[General_Order]
Approvals_Order = ['Invoice Number', 'Entered By Tax No.', 'Entered By Command', 'Entered By Date', 'Entered By Time', 'Invoicing Officer Tax No.', 'Invoicing Officer Command', 'Invoicing Officer Date', 'Invoicing Officer Time', 'Approved By Tax No.', 'Approved By Command', 'Approved By Date', 'Approved By Time']
Approvals_Frame = General_Frame[Approvals_Order]

Item_Frame = pd.concat(Frames)
Item_Order = ['Invoice Number', 'Item', 'Total QTY', 'Articles', 'Description', "Cash", 'Disposition']
Item_Frame = Item_Frame[Item_Order]

Payment_Forms = pd.concat(Payment)
Payment_Order = ['Invoice Number', 'Transaction Date', 'Returning Officer Tax No.', 'Returning Officer Command', 'Return Date', 'Return Time', 'Item (Number)', "Returning Article Description", "Return Quantity", "Actual amt value"]
Payment_Frame = Payment_Forms[Payment_Order]
        
Invoice_Frame.to_csv('Invoice_currency.csv', sep=',', index = False)
Approvals_Frame.to_csv('Approvals_currency.csv', sep=',', index = False)
Item_Frame.to_csv('Item_currency.csv', sep=',', index = False)
Payment_Frame.to_csv('Return_currency.csv', sep=',', index = False)