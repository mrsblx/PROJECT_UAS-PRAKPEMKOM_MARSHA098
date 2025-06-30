# untuk install flask: pip install flask 
# install koneksi python flask ke mysql : pip install flask_mysqldb 

from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask import render_template 

app = Flask(__name__)

# MySQL config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root' 
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'universitas'
mysql = MySQL(app) 

@app.route('/')
def root():
    return 'Selamat datang di tutorial restful API'

@app.route('/person') 
def person():
    return jsonify({'name': 'acha', 'address': 'bandung'}) 

@app.route('/dosen', methods=['GET', 'POST'])  
def dosen():
    if request.method == 'GET': 
        cursor = mysql.connection.cursor() 
        cursor.execute("SELECT * FROM DOSEN") 
        column_names = [i[0] for i in cursor.description] 
        data = [dict(zip(column_names, row)) for row in cursor.fetchall()]
        cursor.close() 
        return jsonify(data)

    elif request.method == 'POST': 
        nama = request.json.get('nama')
        univ = request.json.get('univ')
        jurusan = request.json.get('jurusan')

        if not nama or not univ or not jurusan:
            return jsonify({'error': 'Missing required fields'}), 400
        
        cursor = mysql.connection.cursor()
        sql = "INSERT INTO DOSEN (nama, univ, jurusan) VALUES (%s, %s, %s)"
        val = (nama, univ, jurusan) 
        cursor.execute(sql, val) 
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Data added successfully!'})

@app.route('/detaildosen') 
def detaildosen():
    if 'id' in request.args:
        dosen_id = request.args['id']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM DOSEN WHERE dosen_id = %s", (dosen_id,))
        column_names = [i[0] for i in cursor.description] 
        data = [dict(zip(column_names, row)) for row in cursor.fetchall()]
        cursor.close()
        return jsonify(data)
    else:
        return jsonify({'error': 'ID parameter is required'}), 400
    
@app.route('/deletedosen', methods=['DELETE']) 
def deletedosen():    
    if 'id' in request.args:
        dosen_id = request.args['id']
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM DOSEN WHERE dosen_id = %s", (dosen_id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Data deleted successfully!'}) 
    
@app.route('/editdosen', methods=['PUT']) 
def editdosen():    
    data = request.get_json()

    # Pastikan semua data yang dibutuhkan tersedia
    if not all(k in data for k in ("dosen_id", "nama", "univ", "jurusan")):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        cursor = mysql.connection.cursor()
        sql = "UPDATE dosen SET nama=%s, univ=%s, jurusan=%s WHERE dosen_id=%s"
        val = (data['nama'], data['univ'], data['jurusan'], data['dosen_id'])
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Data updated successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    
@app.route('/dosenhtml')
def dosenhtml():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM DOSEN")
    column_names = [i[0] for i in cursor.description]
    data = [dict(zip(column_names, row)) for row in cursor.fetchall()]
    cursor.close()
    return render_template("dosen.html", dosens=data)   

@app.route('/tambahdosen', methods=['GET', 'POST'])
def tambahdosen():
    if request.method == 'POST':
        nama = request.form['nama']
        univ = request.form['univ']
        jurusan = request.form['jurusan']

        if not nama or not univ or not jurusan:
            return "Semua field harus diisi", 400
        
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO DOSEN (nama, univ, jurusan) VALUES (%s, %s, %s)", (nama, univ, jurusan))
        mysql.connection.commit()
        cursor.close()
        return "Dosen berhasil ditambahkan! <br><a href='/dosenhtml'>Lihat Data</a>"

    return render_template('tambahdosen.html')
 
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Ganti port ke 5000 yang lebih umum
