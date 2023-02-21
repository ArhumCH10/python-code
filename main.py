from flask import Flask, render_template, request
import openai
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'dbName'
 
mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def hello_world():

    if request.method == 'POST':
        person = request.form['text']
        query = get_query(person)

        with open('queries.txt', 'a') as f:
            f.write('\n<query start>'+str(person))
            f.write(query)
            f.write('<query end>')

    query_list, author_list = read_queries()
    query_list_reverse = [i for i in query_list[::-1]]
    author_list_reverse = [i for i in author_list[::-1]]

    return render_template('index.html', query_list=query_list_reverse, author_list=author_list_reverse)

    if request.method == 'POST':
        query = request.form['query']
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO info_table VALUES(%s)''',(query))

def get_query(person):
    openai.api_key = "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"

    response = openai.Completion.create(
    model="text-davinci-003",
    prompt="give me  a joke about",
    temperature=0.9,
    max_tokens=150,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.6,
    stop=[" Human:", " AI:"]
    )

    print(response.choices[0].text)

def read_queries():
    query_list = []
    author_list = []
    with open('queries.txt', 'r') as f:
        
        query_text = []

        for line in f:
            if '<query start>' in line:
                author = line[12:-1]
                author_list.append(author)
                continue
            if line == '/n':
                continue
            if '<query end>' in line:
                query_list.append(query_text)
                query_text = []
                continue
            query_text.append(line)
    return query_list, author_list

if __name__ == '__main__':
    app.run(debug=True)
