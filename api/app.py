import json
from flask import app, request, jsonify
from sqlalchemy import func, desc
from model import app, metadata, db_session, Base, cschema
from sqlalchemy.exc import InterfaceError, DatabaseError


@app.route('/v1/data/query/structure/', methods = ['GET'])
def return_db_info():
    if request.method == "GET":
        #Dictionary that will hold the table name and its columns.
        tbi = {}
        #List containing primary keys from the tables to be removed from the response as the user have no use to thoses.
        keystoremove = ['codigo_ocorrencia', 'codigo_ocorrencia1', 'codigo_ocorrencia2', 'codigo_ocorrencia3', 'codigo_ocorrencia4']
        #Function that remove the primary keys from the respose.
        def remove_keys(values):
            if values not in keystoremove:
                return True  

            return False
        #Loop that get the table name and columns.
        for t in metadata.sorted_tables:
            tbi[t.name] = list(filter(remove_keys, t.columns.keys()))

        response = jsonify(tbi)
    return response


@app.route('/v1/data/query/column/', methods = ['GET'])
def get_data():
    if request.method == "GET":
        #Checks if the table was sent in the request if its wasnt theres no way that the column was sent either, and without both its impossible to do the query.
        if not request.args.get("table"):
            return jsonify("No table was sent in the request to create the chart."), 400
        #Variables that hold the value in the request, this is used to make the code more readable
        rtable = request.args.get("table")
        rcolumn = request.args.get('column')
        sorted_checked = request.args.get("sort")
        
        #This dictionary will hold the data that is going to be query, it will be used to make the response.
        jdata = {}
        
        #A try execept block in case that the database is offline or somehow the user sends an invalid column.
        try:
            query_value = Base.metadata.tables[cschema + '.' + rtable].columns[rcolumn]
        except KeyError:
            return jsonify("No table or column with the name sent was found."), 400
        except (InterfaceError, DatabaseError):
            return jsonify("Could not reach the database."), 503

        #Checks the value of the sort check box if its 1 it sorts the data.
        if int(sorted_checked) == 1:
            #This query is using the count function to count the results on the back-end, this way originaly done by the chart.js libary on the browser, but that left the processing of the data to the user machine doing this removes some of the processing weight from the user machine.
            query = db_session.query(query_value, func.count(query_value).label("total_count")).order_by(desc("total_count")).group_by(query_value).all()
        else:
            #This query is using the count function to count the results on the back-end, this way originaly done by the chart.js libary on the browser, but that left the processing of the data to the user machine doing this removes some of the processing weight from the user machine.
            query = db_session.query(query_value, func.count(query_value).label("total_count")).group_by(query_value).all()

        #A for loop that sets the data of the query in the dictionary
        for data in query:
            #data[0] is the name of the value and data[1] is the result of the count function.
            jdata[data[0]] = data[1]

        #I am using json.dumps to preserve the order of the data, as when i tried to do this with jsonify it would always change the order of the result making sorting on the back-end impossible.
        response = json.dumps(jdata, sort_keys=False ,ensure_ascii=False)
        return response

@app.route('/v1/data/query/where/', methods = ['GET'])
def comple_data():
    if request.method == "GET":
        #Checks if the tableWhere was sent in the request if its wasnt theres no way that the column was sent either, and without both its impossible to do the query. 
        if not request.args.get("tableWhere"):
            return jsonify("No option selected in one of the fields."), 400
        #Variables that hold the value in the request, this is used to make the code more readable
        rtable = request.args.get("table")
        rcolumn = request.args.get('column')
        rtablewhere = request.args.get("tableWhere")
        rcolumnwhere = request.args.get('columWhere')
        equals_to = (request.args.get("equalTo")).upper()
        sorted_checked = request.args.get("sort")

        #This will recive the primary key of the table to be joined in case a join is needed.
        pkeytojoin = ''

        #A try execept block in case that the database is offline or somehow the user sends an invalid column.
        try:
            queryValue1 = Base.metadata.tables[cschema + '.' + rtable].columns[rcolumn]
            table_1 = Base.metadata.tables[cschema + '.' + rtable]
            table_2 = Base.metadata.tables[cschema + '.' + rtablewhere]
            filtered_by = Base.metadata.tables[cschema + '.' + rtablewhere].columns[rcolumnwhere] == equals_to
        except KeyError:
            return jsonify("No table or column with the name sent was found."), 400
        except (InterfaceError, DatabaseError):
            return jsonify("Could not reach the database."), 503

        #This dictionary is used to get the primary keys of the table to do a join based on the args.get variable that hold the values sent from the front-end.
        pkeys = {
            'ocorrencia':'codigo_ocorrencia',
            'ocorrencia_tipo': 'codigo_ocorrencia1',
            'aeronave':'codigo_ocorrencia2',
            'fator_contribuinte': 'codigo_ocorrencia3',
            'recomendacao': 'codigo_ocorrencia4'        
        }


        #This dictionary will hold the data that is going to be query, it will be used to make the response.
        jdata = {}

        #Checks if both primary keys are the same, to see if a join is necessary.
        if pkeys[rtable] == pkeys[rtablewhere]:
            if int(sorted_checked) == 1:
                complex_query_witjoin = db_session.query(queryValue1, func.count(queryValue1).label("total_count")).order_by(desc("total_count")).filter(filtered_by).group_by(queryValue1).all()
            else:
                complex_query_witjoin = db_session.query(queryValue1, func.count(queryValue1).label("total_count")).filter(filtered_by).group_by(queryValue1).all()
        else:
            #This if checks which of the two variable values is not ocorrencia, and then set pkeytojoin as the primary key of that value, in the database the ocorrencia table is the only one with foreign keys so it will always be sent in the request.
            if rtable == 'ocorrencia':
                pkeytojoin = pkeys[rtablewhere]
        
            else:
                pkeytojoin = pkeys[rtable]

            #Querys with join.
            if int(sorted_checked) == 1:
                complex_query_witjoin = db_session.query(queryValue1, func.count(queryValue1).label("total_count")).order_by(desc("total_count")).join(table_2, table_1.columns[pkeytojoin] == table_2.columns[pkeytojoin]).filter(filtered_by).group_by(queryValue1).all()


            else:
                complex_query_witjoin = db_session.query(queryValue1, func.count(queryValue1).label("total_count")).join(table_2, table_1.columns[pkeytojoin] == table_2.columns[pkeytojoin]).filter(filtered_by).group_by(queryValue1).all()

        #A for loop that sets the data of the query in the dictionary
        for data in complex_query_witjoin:
            #data[0] is the name of the value and data[1] is the result of the count function.
            jdata[data[0]] = data[1]

        response = json.dumps(jdata, sort_keys=False ,ensure_ascii=False)
        return response


if __name__ == "__main__":
    app.run(debug=True)