
from flask import Flask, request, render_template 
import os
import smtplib
import imghdr
from email.message import EmailMessage

# Flask constructor
app = Flask(__name__)  

ref = []

@app.route('/',methods =["GET", "POST"])
def index():
    return render_template('form.html')
    

@app.route("/1",methods =["GET", "POST"])
def submit_data():
    
    name=request.form.get("mailID")
    
    subject=request.form.get("subject") 
    body=request.form.get("body")
    multi=[]
    multi=request.form.getlist("multiple")
    EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

    #contacts = ['shubh.gehu@gmail.com', 'ranahimanshi1998@gmail.com','himanshi.rana2110@gmail.com','anvesha123rawat@gmail.com']
    
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] =  name #or ', '.join(contacts)
    msg.set_content(body)
    print("hi from here")
    list_len=len(multi)
    list=[]
    for i in range(list_len):
        list.append("C:/workbook/emailscraping/static/"+multi[i])
    print(list)

    substring = ".pdf"
    pdf_string = [string for string in list if substring in string]
    print(pdf_string)

    substring = ".jpg"
    jpg_string = [string for string in list if substring in string]
    print(jpg_string)


    for file in jpg_string:
        with open(file,'rb') as f:
            file_data=f.read()
            file_type=imghdr.what(f.name)
            file_name=f.name
        msg.add_attachment(file_data,maintype='image',subtype=file_type,filename=file_name)

    for file in pdf_string:
        with open(file,'rb') as f:
            file_data=f.read()
            file_name=f.name
        msg.add_attachment(file_data,maintype='application',subtype='octet-stream',filename=file_name)




    print("hiii 2")
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
        print("done") 
    return render_template('home.html')


if __name__ == "__main__":
    app.run(debug=True)