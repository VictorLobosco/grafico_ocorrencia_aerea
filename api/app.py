from flask import app, request, jsonify, Flask
from sqlalchemy.engine import row
from model import app, metadata, engine, db_session, Base, cschema


@app.route('/db_info/', methods = ['GET'])
def return_db_info():
    if request.method == "GET":
        tbi = {}
        for t in metadata.sorted_tables:
            tbi[t.name] = t.columns.keys()

        response = jsonify(tbi)
    return response

@app.route('/get_data/', methods = ['GET'])
def get_data():
    if request.method == "GET":
        #this is used to read the arguments on the request, i will use this to get the table and colum to send the info.
        rtable = request.args.get("table")
        rcolumn = request.args.get('column')
        cquery = db_session.query(Base.metadata.tables[cschema + '.' + rtable].columns[rcolumn]).all()
        db1 = [row[0] for row in cquery]
        response = jsonify(db1)
        return response


if __name__ == '__main__':
    app.run(debug=True)