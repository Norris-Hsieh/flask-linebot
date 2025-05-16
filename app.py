from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask (__name__)

def search_keyword(keyword):
    conn = sqlite3.connect('mydata.db')
    cursor = conn.cursor()

    query = """
    SELECT * FROM industry
    WHERE 行業中文 LIKE ? OR 補充說明 LIKE ?
    """

    cursor.execute(query, (f'%{keyword}%', f'%{keyword}%'))
    results = cursor.fetchall()
    conn.close()
    return results

@app.route('/search',methods = ['GET'])
def search():
    keyword =request.args.get('q')
    if not keyword:
       return jsonify({'error': '請提供 ?q=關鍵字'}),400
    
    results = search_keyword(keyword)
    if not results:
       return jsonify({'message': '找不到資料'}),404
    
    data =[]
    for row in results:
        data.append({
            '行業中文': row[1],
            '行業代碼': row[2],
            '補充說明': row[3],
        })
    return jsonify(data)

if __name__ =='__main__':
    port = int(os.environ.get('port',10000))
    app.run(host='0.0.0.0',port=port)
