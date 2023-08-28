from flask import Flask, render_template, request, url_for, redirect
from urllib import request
import PyPDF2
from sentence_transformers import SentenceTransformer
from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from sklearn.metrics.pairwise import cosine_similarity
import Web_Scrap
from bisect import bisect_left
# from goto import goto, label
import os
import io

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'project'

mysql = MySQL(app)

# Python code to demonstrate working
# of binary search in library


def BinarySearch(a, x):
	i = bisect_left(a, x)
	if i != len(a) and a[i] == x:
		return i
	else:
		return -1


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/university_in')
def university_in():
    return render_template('university_in.html')

@app.route('/university_in', methods=['POST', 'GET'])
def university_in11():
    msg = ''
    names1 = []
    names2 = []
    dict = {}
    dict1 = {}
    dict = {}

    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM comp")
        fetchdata = cur.fetchall()
        sent1 = []
        # Iterate with outer list
        for element in fetchdata:
            for item in element:
                sent1.append(item)
        # return sent1

        #

        pdfFileObj = request.files['syl']

        # creating a pdf reader object
        # pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
###############################################################################################

        # creating a pdf reader object
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

        # printing number of pages in pdf file
        ans = pdfReader.numPages;
        # -----------------------------
        str1 = " "

        for i in range(1, ans):
            str1 += pdfReader.getPage(i).extractText()

        with open("text.txt", "w", encoding='utf-8') as f:
            f.write(str1)
        # -------------------------------
        # # creating a page object
        # data1 = []
        # for i in range(0, ans):
        #     pageObj = pdfReader.getPage(i)
        #     # extracting text from page
        #     raj = pageObj.extractText();
        #     data1.append(raj);
        #
        # closing the pdf file object
        data1 = open("text.txt", encoding='utf-8').readlines()
        # model_name = 'all-MiniLM-L6-v2'
        model_name = 'average_word_embeddings_glove.6B.300d'

        model = SentenceTransformer(model_name)

        sentence_vecs1 = model.encode(sent1)
        sentence_vecs2 = model.encode(data1)



#########################################################################################
        # printing number of pages in pdf file
        # ans = pdfReader.numPages;

        # creating a page object
        # data1 = []
        # for i in range(0, ans):
        #     pageObj = pdfReader.getPage(i)
        #     # extracting text from page
        #     raj = pageObj.extractText();
        #     data1.append(raj);
        #
        # # closing the pdf file object
        # pdfFileObj.close()
        # model_name = 'bert-base-nli-mean-tokens'
        # model_name = 'paraphrase-MiniLM-L6-V2'
        #
        # model = SentenceTransformer(model_name)
        #
        # sentence_vecs1 = model.encode(sent1)
        # sentence_vecs2 = model.encode(data1)
        names1= []
        names2 = []
        names3 = []
        sum = 0;
        for i in range(0, len(sent1)):
            b = cosine_similarity([sentence_vecs1[i]], sentence_vecs2[0:])
            data = b[0]
            ans = max(data)
            sum = sum + ans;
            print(ans)
            if ans >= 0.81:
                # dict1[sent1[i]] = ans
                names1.append(i);
            else:
                # dict2[sent1[i]] = ans
                names2.append(i);


           
        print(sum)
        avg = (float)(sum/34);


        clg = request.form['abhi']
        cursor = mysql.connection.cursor()
        print(type(avg))
        # avg = str(avg)
        print(avg)
        cursor.execute(''' INSERT INTO top VALUES(%s,%b)''', (clg,avg))
        mysql.connection.commit()


        # names1 = list(dict.keys())
        # names2 = list(dict1.keys())

        cursor = mysql.connection.cursor()
        # clg = 'pccoe'
        query = "Alter table comp1 add " + clg + " varchar(100)"
        # cursor.execute("ALTER TABLE demo ADD clg VARCHAR(100)")
        cur.execute(query)
        query1 = "Alter table admin add " + clg + " varchar(100)"
        cur.execute(query1)
        mysql.connection.commit()

        for i in range(len(names1)):
            karea = str(names1[i])
            # query = "update demo set " + clg + "='Found' where fname=" + id
            query = "update comp1 set " + clg + "='Found' where id=" + karea
            query1 = "update admin set " + clg + "='Found' where id=" + karea

            cur.execute(query)
            cur.execute(query1)
            mysql.connection.commit()

        for i in range(len(names2)):
            karea = str(names2[i])
            query = "update comp1 set " + clg + "='Not Found' where id=" + karea
            query1 = "update admin set " + clg + "='Not Found' where id=" + karea
            cur.execute(query)
            cur.execute(query1)
            mysql.connection.commit()

        print(names1)
        print(names2)


        os.remove("text.txt")

    heading3 = ("id","Knowledge_area",clg);
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM comp1")
    fetchdata2 = cur.fetchall()
    cur.execute('alter table comp1 drop column '+clg)
    mysql.connection.commit()
    cur.close()
    return render_template('university_in.html', table_headiing2=heading3, data2=fetchdata2,msg=avg)


headings = ("Subject", "Lecture", "Practical", "Credit","content")


@app.route('/university_in1')
def Home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT clgname, MAX(avg) FROM top")
    fetchdata = cur.fetchall()

    for element in fetchdata:
        sent1 = []
        for i in range(1, len(element)):
            sent1.append(element[i])
        fetch[element[0]] = sent1
    data1 = fetchdata[0][0]
    data2 = str(fetchdata[0][1])
    que = "Top College as per our list is "+data1 + " and its accuracy with knowledge area is : "+data2;
    return render_template('My.html', mm=que)


@app.route('/university_in1', methods=['POST'])
def university_in1():
    text = request.form['text']
    text1 = request.form['text1']
    text2 = request.form['text2']
    text3 = request.form['text3']
    data = []
    dict = {}
    data.append(text1)
    data.append(text2)
    data.append(text3)

    data1 = fetch[text]
    ans = []
    for i in range(len(data)):
        ans.append(int(data[i]) - int(data1[i]))
    return render_template('university_in1.html', ans=ans)

headings1 = ("Domain", "Requirements")
fetch = {}
fetchdata = (())
@app.route('/university_in2')
def university_in2():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM industry")
    fetchdata1 = cur.fetchall()

    for element in fetchdata:
        sent1 = []
        for i in range(1, len(element)):
            sent1.append(element[i])
        fetch[element[0]] = sent1

    return render_template('university_in2.html', table_headiing1=headings1, data1=fetchdata1)

# @app.route('/university_in', methods=['POST'])
# def my_form_pos():
#     text = request.form['a']
#     text1 = request.form['b']
#     text2 = request.form['c']
#     text3 = request.form['d']
#     data = []
#     dict = {}
#     data.append(text1)
#     data.append(text2)
#     data.append(text3)
#
#     data1 = fetch[text]
#     ans = []
#     for i in range(len(data)):
#         ans.append(int(data[i])-int(data1[i]))
#     render_template('university_in.html', disp=ans)
#


@app.route('/industry')
def industry():
    return render_template('industry.html')
@app.route('/industry',methods=['POST'])
def industry_():
    a = request.form['a']
    b = request.form['b']
    if(a=='abhi@gmail.com' and b == 'abc'):
        return redirect(url_for("industry_in"))


    return render_template('industry.html')


@app.route('/industry_in')
def industry_in():
    return render_template('industry_in.html')

@app.route('/industry_in',methods=['POST'])
def My_form_post():
    if request.method == 'POST':
        text1 = request.form['text1']

        # text2 = request.form['text2']

        strx = Web_Scrap.direct_scrape(text1, 4)

        # def Abhi(str1, a):
        #     data = direct_scrape(str1, a)
        #     return str(data);




        cursor = mysql.connection.cursor()

        cursor.execute(''' INSERT INTO industry VALUES(%s,%s)''', (text1,strx))
        mysql.connection.commit()
        cursor.close()
        # cursor.commit()




        mm1 = "data sent successfully"
        return render_template('industry_in.html',mm = mm1)






@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/admin',methods=['POST'])
def admin_():
    a = request.form['a']
    b = request.form['b']
    if(a == "abhi@gmail.com" and b == 'abc'):
        return redirect(url_for("admin_in"))
    else:
        mm4 ="Username or password is incorrect"
        return render_template('admin.html',mm3=mm4)



@app.route('/admin_in')
def admin_in():
    # adm = 'admin'
    # cur = mysql.connection.cursor()
    # res = cur.execute(f"SELECT * FROM {adm}")
    # print(res.keys())

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM admin")
    fetchdata5 = cur.fetchall()

    for element in fetchdata5:
        sent5 = []
        for i in range(1, len(element)):
            sent5.append(element[i])
        fetch[element[0]] = sent5

    cur = mysql.connection.cursor()
    cur.execute('SHOW COLUMNS FROM `admin`')
    fetchdata = cur.fetchall()
    # print(fetchdata)
    cur.close
    data = []
    for ele in fetchdata:
        data.append(ele[0]);
    tup = tuple(data)
    # print(tup)
    return render_template('admin_in.html', table_headiing5=tup, data5=fetchdata5)


# @app.route('/industry', methods=['POST', 'GET'])
# def industry():
#     if request.method == 'POST' and request.form['password'] == 'abcd':
#         return render_template("industry_in.html")
#     return render_template("industry.html")


@app.route('/contactus')
def contactus():
    return render_template('contactus1.html')


import asyncio
from os import path
import urllib.parse
from pyppeteer import launch






if __name__ == '__main__':
    app.secret_key = 'secretive'
    app.run(debug=True)