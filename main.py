from bson import json_util
import json
from flask import Flask, render_template,request,json,jsonify
from flask_socketio import SocketIO
from logger import Logger
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'S3cr3t!'
socket = SocketIO(app)

log = Logger()

@app.route('/')
def index():
    data = log.read_data_Curr()
    return render_template('index.html',data=data)


@app.route('/settings')
def settings():
    return render_template('settings.html')


@app.route('/addValue',methods=['POST'])
def addValue():
    data = request.json
    query = data.get("query")

    conn = sqlite3.connect('database/sensData.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute(query)
        conn.commit()
        response = {'status': 'success', 'message': 'Valor adicionado com sucesso'}
    except Exception as e:
        conn.rollback()
        response = {'status': 'error', 'message': f'Erro ao executar a query: {str(e)}'}
    finally:
        conn.close()
        
    return jsonify(response), 200    

@app.route('/loadDatabase',methods=['GET'])
def loadDatabase():
    conn = sqlite3.connect('database/sensData.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('select id_valor,valor,unidade,timestp from sensor,valores where sensor.id_sensor = valores.sensor;')
        results = cursor.fetchall()
        print(results)
        conn.commit()
        response = {'status': 'success', 'message': 'Valor adicionado com sucesso'}
    except Exception as e:
        conn.rollback()
        response = {'status': 'error', 'message': f'Erro ao executar a query: {str(e)}'}
    finally:
        conn.close()
        
    return jsonify(results), 200   


def data_update(data):
        socket.emit('data_update', json.dumps(data, default=json_util.default))


if __name__ == '__main__':
    log.on_data_updated(data_update)
    app.run(host='0.0.0.0', debug=True)

