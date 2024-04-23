import mysql.connector as con
from flask import Flask,render_template,request

mydb=con.connect(host='localhost',user='root',passwd='admin123',database='dcc4',auth_plugin='mysql_native_password')

cursor=mydb.cursor()

app=Flask(__name__)

cursor.execute("Show columns from redemption_details")
p1=cursor.fetchall()
cursor.execute("Show columns from purchase_detail")
p2=cursor.fetchall()

for i in range(len(p1)):
    p1[i]=p1[i][0]
for i in range(len(p2)):
    p2[i]=p2[i][0]

cursor.execute("Select distinct `Name of the Purchaser` from purchase_detail")
purchasername=list(cursor.fetchall())

for i in range(len(purchasername)):
    purchasername[i]=''.join(purchasername[i])

p1=p1+p2[1:4]+p2[6:]

cursor.execute("Select distinct `Name of the Political Party` from redemption_details")
parties=list(cursor.fetchall())

for i in range(len(parties)):
    parties[i]=''.join(parties[i])

@app.route("/",methods=["GET","POST"])
def data():
    return render_template ("index.html",purchaser=purchasername,party=parties)

@app.route("/Q1",methods=["POST","GET"])
def home():
    if request.method=="POST":
        x=(request.form["nm"])
        cursor.execute("select * from redemption_details where `Bond Number` = %s",(str(x),))
        data=cursor.fetchall()
        cursor.execute("select * from purchase_detail where `Bond Number` = %s",(str(x),))
        data1=cursor.fetchall()
        for i in range(len(data1)):
            data[i]=data[i]+data1[i][1:4]+data1[i][6:]
        if len(data)==0:
            return render_template("NA.html")
        else:
             return render_template("question1.html",column=p1,rows=data)

@app.route("/Q2",methods=["GET","POST"])
def Q2():
    if request.method=="POST":
        c=request.form["buyer"]
        print(type(c))
        cursor.execute("select Denominations from purchase_detail where `Name of the Purchaser`=%s",(c,))
        j1=cursor.fetchall()
        cursor.execute("select `Date of Purchase` from purchase_detail where `Name of the Purchaser`=%s",(c,))
        j2=cursor.fetchall()
        if (len(j1)!=0 and len(j2)!=0):
            year19=0
            year20=0
            year21=0
            year22=0
            year23=0
            year24=0
            for i in range(len(j1)):
                j1[i]=(''.join(j1[i])).replace(",", "")
            for i in range(len(j2)):
                if j2[i][0][-2:]=='19':
                     year19+=int(j1[i])
                elif j2[i][0][-2:]=='20':
                     year20+=int(j1[i])
                elif j2[i][0][-2:]=='21':
                     year21+=int(j1[i])
                elif j2[i][0][-2:]=='22':
                     year22+=int(j1[i])
                elif j2[i][0][-2:]=='23':
                     year23+=int(j1[i])
                elif j2[i][0][-2:]=='24':
                     year24+=int(j1[i])
            dt=[year19,year20,year21,year22,year23,year24]
            ey=['19','20','21','22','23','24']
            print(dt)
            return render_template("question2.html",money=dt,year=ey)
        
@app.route("/Q3",methods=["GET","POST"])
def Q3():
    if request.method=="POST":
        h=request.form["party"]
        cursor.execute("select Denominations from redemption_details where `Name of the Political Party`=%s",(h,))
        b=cursor.fetchall()
        cursor.execute("select `Date of Encashment` from redemption_details where `Name of the Political Party`=%s",(h,))
        c=cursor.fetchall()
        if (len(b)!=0 and len(c)!=0):
            y19=0
            y20=0
            y21=0
            y22=0
            y23=0
            y24=0
            for i in range(len(b)):
                b[i]=(''.join(b[i])).replace(",", "")
            # print(b)
            for i in range(len(c)):
                if c[i][0][-2:]=='19':
                     y19+=int(b[i])
                elif c[i][0][-2:]=='20':
                     y20+=int(b[i])
                elif c[i][0][-2:]=='21':
                     y21+=int(b[i])
                elif c[i][0][-2:]=='22':
                     y22+=int(b[i])
                elif c[i][0][-2:]=='23':
                     y23+=int(b[i])
                elif c[i][0][-2:]=='24':
                     y24+=int(b[i])
            dt1=[y19,y20,y21,y22,y23,y24]
            ey1=['19','20','21','22','23','24']
            return render_template("question3.html",money=dt1,year=ey1)
        
@app.route("/Q4",methods=["GET","POST"])
def Q4():
    if request.method=="POST":
        par=request.form["party"]
        cursor.execute("Select Purchase_Detail.Denominations,`Name of the Purchaser` from  purchase_detail inner join redemption_details where redemption_details.`Bond Number`= purchase_detail.`Bond Number` and purchase_detail.Prefix = redemption_details.Prefix and redemption_details.`Name of the Political Party`=%s",(par,))
        cp=cursor.fetchall()
        l={}
        print(cp)
        if len(cp)==0:
            return render_template("NA.html")
        else:
            for i in cp:
                if i[1] not in l:
                   l[i[1]]=0
                l[i[1]]+=int(i[0].replace(",",""))
        k_=[]
        m=[]
        nums=0
        for i in l:
            k_.append([i,l[i]])
            nums+=l[i]
        return render_template("question4.html",person=k_,total=nums)

@app.route("/Q5",methods=["GET","POST"])
def Q5():
        if request.method=="POST":
            b=request.form["buyer"]
            cursor.execute("Select redemption_details.Denominations,`Name of the Political Party` from  redemption_details inner join purchase_detail where redemption_details.`Bond Number`= purchase_detail.`Bond Number` and purchase_detail.Prefix = redemption_details.Prefix and purchase_detail.`Name of the Purchaser`=%s",(b,))
            cp=cursor.fetchall()
            l={}
            print(cp)
            if len(cp)==0:
                return render_template("NA.html")
            else:
                for i in cp:
                    if i[1] not in l:
                        l[i[1]]=0
                    l[i[1]]+=int(i[0].replace(",",""))
            k1=[]
            m=[]
        n1=0
        for i in l:
            k1.append([i,l[i]])
            n1+=l[i]
        return render_template("question5.html",person=k1,total=n1)
    
@app.route("/Q6",methods=["GET","POST"])
def Q6():
    if request.method=="POST":
        y=[]
        y1=[]
        cursor.execute("select distinct(Name of the Political Party) from redemption_details")
        l=list(cursor.fetchall())

        for i in l:
            cursor.execute("Select Denominations from redemption_details where Name of the Political Party=%s",(i[0],))
            k=cursor.fetchall()
            sum=0
            for j in k:
                sum+=int(j[0].replace(",",""))
            y.append([i[0]])
            y1.append(sum)
        return render_template("question6.html",data=y1,label=y)        
    
if __name__== "__main__":
    app.run(debug = True)