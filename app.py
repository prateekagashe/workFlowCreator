from flask import Flask, render_template, request, session, redirect, url_for, flash
from database import db
import mysql.connector
from workflow import database, shape_db, sort_list, axis
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def add_work_flow():
    work_flow_list = database()
    print('before')
    # if request.method == 'POST':
    #     if request.form['submit'] == 'Add':
    #         shapeId = request.form['shapeId']
    if request.method == 'POST':
        if request.form['submit'] == 'Add':
            session['work_flow_name'] = request.form['add']
            try:
                sql = """Insert into work_flow(work_flow_name) values(%s)"""
                cursor = db.cursor()
                cursor.execute(sql, (session['work_flow_name'],))
                cursor.execute("select last_insert_id();")
                session['work_flow_id'] = cursor.fetchone()
                db.commit()
                cursor.close()
                database()
            except mysql.connector.Error as err:
                print(err)
                error = 'WorkFlow already present!! Try creating with a different name'
                errorType = "Duplicate WorkFlow"
            if error:
                return render_template('index.html', error=error, errorType=errorType)
            else:
                return redirect(url_for('del_work_flow', name=session['work_flow_name']))
        if request.form['submit'] == 'Retrieve':
            print('inside ret')
            session['work_flow_name'] = request.form['nn']
            sql = """select work_flow_id from work_flow where work_flow_name = %s;"""
            cursor = db.cursor()
            cursor.execute(sql, (session['work_flow_name'],))
            session['work_flow_id'] = cursor.fetchone()
            print('work_id', session['work_flow_id'])
            db.commit()
            cursor.close()

            return redirect(url_for('del_work_flow', name=session['work_flow_name']))

    return render_template('index.html', workFlowList=work_flow_list)


@app.route('/workflow/<name>', methods=['GET', 'POST'])
def del_work_flow(name):
    shape_list = []
    shape_id = []
    lastshapeid = []
    errorType, error = '', ''
    data = shape_db(shape_list, shape_id)
    total = len(shape_list)
    if total > 2:
        height = 250 * len(shape_list) + 100
    else:
        height = 600
    # print(shape_list, count, height)
    if request.method == 'POST':
        if request.form["submit"] == 'AddShape':
            shapeid = request.form['shapeId']
            shapehead = request.form['shapeHeading']
            shapetype = request.form['shapeType']
            shapedesc = request.form['shapeDesc']
            print(shapedesc, shapehead, shapeid)
            y = 100
            num = 0

            shapedesc = shapedesc.replace('\n', '<br>').replace('\r', '<br>')
            if int(shapeid) in shape_id and shapeid != '':
                error = "Shape id already used, please use a different id."
                errorType = "Duplicate shape id"
                return render_template('/workflow.html', name=session['work_flow_name'], shape_list=shape_list,
                                       count=total, height=height, error=error, errorType=errorType)
            else:
                sql = """INSERT INTO shape_details(work_flow_id, parent_id, shape_sequence_id, shape_name, shape_type_id,
                 shape_desc)  values(%s, %s, %s, %s, (select shape_type_id from shape_type where shape_type = %s), %s);"""
                cursor = db.cursor()
                cursor.execute(sql, (session['work_flow_id'][0], None, shapeid, shapehead, shapetype, shapedesc,))
                db.commit()
                cursor.close()
                shape_list = []
                shape_id = []
                lastshapeid.clear()
                lastshapeid.append(shapeid)

                data = shape_db(shape_list, shape_id)

                if lastshapeid != []:
                    sID = lastshapeid[0]
                    for item in shape_list:
                        if int(item[0]) == int(sID):
                            lastAxis = item[5]
                            break
                print('last', lastAxis)
                total = len(shape_list)
                if total > 2:
                    height = 250 * len(shape_list) + 100
                else:
                    height = 600
            return render_template('/workflow.html', name=session['work_flow_name'], shape_list=shape_list, count=total,
                                   height=height, lastAxis=lastAxis)
        if request.form['submit'] == 'DeleteShape':
            print('delete')
            delid = request.form['delId']
            print(delid)
            sql = """delete from shape_details where work_flow_id = %s and shape_sequence_id = %s 
            and parent_id is null;"""
            cursor = db.cursor()
            cursor.execute(sql, (session['work_flow_id'][0], delid,))
            db.commit()
            cursor.close()
            shape_list = []
            shape_id = []
            data = shape_db(shape_list, shape_id)
            print(shape_list)
            total = len(shape_list)
            if total > 2:
                height = 250 * len(shape_list) + 100
            else:
                height = 600
            return render_template('/workflow.html', name=session['work_flow_name'], shape_list=shape_list, count=total,
                                   height=height)
        if request.form['submit'] == 'Modify_Form':
            modid = request.form['shapeId']
            modshapename = request.form['shapeHeading']
            modshapetype = request.form['shapeType']
            modshapedesc = request.form['shapeDesc']
            originalId = request.form['originalId']
            lastshapeid.clear()
            lastshapeid.append(modid)
            if originalId == modid:


                cursor = db.cursor()
                cursor.execute("""Update shape_details set shape_name = %s, shape_type_id = (select shape_type_id from 
                            shape_type where shape_type = %s ), shape_desc = %s where shape_sequence_id = %s and 
                            work_flow_id = %s and parent_id is null;""",
                               (modshapename, modshapetype, modshapedesc, modid, session['work_flow_id'][0]))
                db.commit()
                cursor.close()
            else:
                if int(modid) in shape_id and modid != '':
                    error = "Shape id already used, please use a different id."
                    errorType = "Duplicate shape id"
                    return render_template('/workflow.html', name=session['work_flow_name'], shape_list=shape_list,
                                           count=total, height=height, error=error, errorType=errorType)
                else:

                    cursor = db.cursor()
                    cursor.execute(
                        """Update shape_details set shape_sequence_id = %s, shape_name = %s, shape_type_id =
                         (select shape_type_id from shape_type where shape_type = %s ), shape_desc = %s 
                         where shape_sequence_id = %s and work_flow_id = %s and parent_id is null;""",
                        (modid, modshapename, modshapetype, modshapedesc, originalId, session['work_flow_id'][0]))
                    db.commit()
                    cursor.close()
            shape_list = []
            shape_id = []
            lastAxis = ''
            data = shape_db(shape_list, shape_id)
            if lastshapeid != []:
                sID = lastshapeid[0]
                for item in shape_list:
                    if int(item[0]) == int(sID):
                        lastAxis = item[5]
                        break
            total = len(shape_list)
            if total > 2:
                height = 250 * len(shape_list) + 100
            else:
                height = 600
            return render_template('/workflow.html', name=session['work_flow_name'], shape_list=shape_list,
                                   count=total, lastAxis=lastAxis, height=height)

        if request.form['submit'] == 'Delete':
            delete = request.form['flowName']
            print('delete', delete)
            sql = """DELETE FROM work_flow where work_flow_name = %s;"""
            cursor = db.cursor()
            cursor.execute(sql, (session['work_flow_name'],))
            db.commit()
            cursor.close()
            return redirect(url_for('add_work_flow'))
    return render_template('workflow.html', shape_list=shape_list, count=total, height=height)


if __name__ == '__main__':
    app.secret_key = 'aheexbeeuqo299ee29'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
