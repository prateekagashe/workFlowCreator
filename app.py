from flask import Flask, render_template, request, session, redirect, url_for, flash
from database import db
import mysql.connector
from workflow import database, shape_db, sort_list, axis
app = Flask(__name__)


counter = 0
@app.route('/', methods=['GET', 'POST'])
def add_work_flow():
    global session_shape_list, error, errorType, count, counter
    error = ''
    counter = 0
    errorType = ''
    work_flow_list = database()
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
    global counter, session_shape_list, session_parent_id, nested_total, display, shape_id
    nested_total, display= None, None
    shape_list = []

    lastshapeid = []
    errorType, error = '', ''
    print(counter)
    if counter == 0:
        session['parent_id'] = ''
        session['shape_list'] = []
        session['parent_list_id'] = []
        counter = counter + 1
        print(counter)
        shape_id = []
        shape_list, shape_id, id = shape_db(session_shape_list=[])

        print('shape ID', shape_id)
        # print('shapeidtype', type(shape_id[0]))
        session_parent_id = []
        session_shape_list = session['shape_list']

# session_shape_list.clear()
# print('shape', shape_list)
    if shape_list:
        if session_shape_list:
            if session_shape_list[-1] == shape_list:
                print('not 1ST EQUEAL')
                session_shape_list.append(shape_list)
                print('session', session_shape_list)
        else:
            print('sssss')
            session_shape_list.append(shape_list)
    print('sess', session_shape_list)


    total = len(shape_list)
    if total > 2:
        height = 250 * len(shape_list) + 100
    else:
        height = 600
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
            print('shape id', shape_id)
            if int(shapeid) in shape_id and shapeid != '':
                error = "Shape id already used, please use a different id."
                errorType = "Duplicate shape id"
                shape_list = session_shape_list[-1]
                total = len(shape_list)
                if total > 2:
                    height = 250 * len(shape_list) + 100
                else:
                    height = 600
                nested_total = len(session_parent_id)
                if nested_total <= 1:
                    display = None
                else:
                    display = nested_total - 1
                return render_template('/workflow.html', name=session['work_flow_name'], shape_list=shape_list,
                                       count=total, height=height, error=error, errorType=errorType, nestedTotal=nested_total, display=display)
            else:
                if session['parent_id']:
                    parent_id = session['parent_id']
                else:
                    parent_id = None

                sql = """INSERT INTO shape_details(work_flow_id, parent_id, shape_sequence_id, shape_name, 
                shape_type_id, shape_desc)  values(%s, %s, %s, %s, (select shape_type_id from shape_type where 
                shape_type = %s), %s);"""
                cursor = db.cursor()
                cursor.execute(sql, (session['work_flow_id'][0], parent_id, shapeid, shapehead, shapetype, shapedesc,))
                db.commit()
                cursor.close()

                shape_list = []
                shape_id = []
                lastshapeid.clear()
                lastshapeid.append(shapeid)
                if session['parent_id']:
                    shape_list, shape_id, id = shape_db(session_shape_list, 0, session['parent_id'])
                else:
                    shape_list, shape_id, id = shape_db(session_shape_list)
                if session_shape_list:
                     session_shape_list.pop(-1)
                session_shape_list.append(shape_list)
                print('final_session', session_shape_list)
                # shape_detail(lastAxis=lastshapeid, height=shape_list)4
                # lastAxis = last_shape_axis(lastshapeid)
                # height = total_shape_count()
                # print('final', lastAxis, height)
                # # lastAxis, height = shape_detail(lastshapeid, shape_list)
                # print('from workflow', shape_list)
                # print('from workflow', type(lastAxis), type(height), shape_list)
                print('insert session', session_shape_list)
                # if shape_list:
                #     if session_shape_list[-1] != shape_list:
                #         print('not equal')
                #         session_shape_list.append(shape_list)
                #         print('session', session_shape_list)
                print('lastshapeid', lastshapeid)
                if lastshapeid != []:
                    sID = lastshapeid[0]
                    print('shape list inside',shape_list)
                    print('last Shape Id', sID)
                    for item in shape_list:
                        print("tess", item)
                        if int(item[0]) == int(sID):
                            lastAxis = item[5]
                            print('last axis', lastAxis)
                            break

                total = len(shape_list)
                if total > 2:
                    height = 250 * len(shape_list) + 100
                else:
                    height = 600
                nested_total = len(session_parent_id)
                if nested_total <= 1:
                    display = None
                else:
                    display = nested_total - 1
                print('from workflow', shape_list)
                print('from las', lastAxis, height, shape_list)
                print('from workflow', type(lastAxis), type(height), shape_list)

            return render_template('/workflow.html', name=session['work_flow_name'], shape_list=shape_list, count=total,
                                   height=int(height), lastAxis=int(lastAxis), errorType=errorType, error=error, nestedTotal=nested_total, display=display)
        if request.form['submit'] == 'DeleteShape':
            print('delete')
            delid = request.form['delId']
            print(delid)
            if session['parent_id']:
                sql = """delete from shape_details where work_flow_id = %s and shape_sequence_id = %s 
                         and parent_id = %s;"""

                data = (session['work_flow_id'][0], delid, session['parent_id'],)

            else:
                sql = """delete from shape_details where work_flow_id = %s and shape_sequence_id = %s 
                and parent_id is null;"""
                data = (session['work_flow_id'][0], delid,)

            cursor = db.cursor()
            cursor.execute(sql, data)
            db.commit()
            cursor.close()
            print(shape_list)
            if session['parent_id']:
                shape_list, shape_id, id = shape_db(session_shape_list, 0, session['parent_id'])
            else:
                shape_list, shape_id, id = shape_db(session_shape_list)
            session_shape_list.pop(-1)
            session_shape_list.append(shape_list)
            print('final_session', session_shape_list)
            total = len(shape_list)
            if total > 2:
                height = 250 * len(shape_list) + 100
            else:
                height = 600
            nested_total = len(session_parent_id)
            if nested_total <= 1:
                display = None
            else:
                display = nested_total - 1
            return render_template('/workflow.html', name=session['work_flow_name'], shape_list=shape_list, count=total,
                                   height=height, nestedTotal=nested_total, display=display)
        if request.form['submit'] == 'Modify_Form':
            modid = request.form['shapeId']
            modshapename = request.form['shapeHeading']
            modshapetype = request.form['shapeType']
            modshapedesc = request.form['shapeDesc']
            originalId = request.form['originalId']
            modshapedesc = modshapedesc.replace('\n', '<br>').replace('\r', '<br>')

            lastshapeid.clear()
            lastshapeid.append(modid)
            if originalId == modid:
                cursor = db.cursor()
                if session['parent_id']:
                    cursor.execute("""Update shape_details set shape_name = %s, shape_type_id = (select shape_type_id from 
                                   shape_type where shape_type = %s ), shape_desc = %s where shape_sequence_id = %s and 
                                   work_flow_id = %s and parent_id = %s;""",
                                   (modshapename, modshapetype, modshapedesc, modid, session['work_flow_id'][0], session['parent_id']))

                else:
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
                    shape_list = session_shape_list[-1]
                    total = len(shape_list)
                    if total > 2:
                        height = 250 * len(shape_list) + 100
                    else:
                        height = 600
                    nested_total = len(session_parent_id)
                    if nested_total <= 1:
                        display = None
                    else:
                        display = nested_total - 1
                    return render_template('/workflow.html', name=session['work_flow_name'], shape_list=shape_list,
                                           count=total, height=height, error=error, errorType=errorType, nestedTotal=nested_total, display=display)
                else:

                    cursor = db.cursor()
                    if session['parent_id']:
                        cursor.execute(
                            """Update shape_details set shape_sequence_id = %s, shape_name = %s, shape_type_id =
                             (select shape_type_id from shape_type where shape_type = %s ), shape_desc = %s 
                             where shape_sequence_id = %s and work_flow_id = %s and parent_id = %s;""",
                            (modid, modshapename, modshapetype, modshapedesc, originalId, session['work_flow_id'][0], session['parent_id']))
                    else:
                        cursor.execute(
                            """Update shape_details set shape_sequence_id = %s, shape_name = %s, shape_type_id =
                             (select shape_type_id from shape_type where shape_type = %s ), shape_desc = %s 
                             where shape_sequence_id = %s and work_flow_id = %s and parent_id is null;""",
                            (modid, modshapename, modshapetype, modshapedesc, originalId, session['work_flow_id'][0]))
                    db.commit()
                    cursor.close()
            lastAxis = ''
            if session['parent_id']:
                shape_list, shape_id, id = shape_db(session_shape_list, 0, session['parent_id'])
            else:
                shape_list, shape_id, id = shape_db(session_shape_list)
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
            nested_total = len(session_parent_id)
            if nested_total <= 1:
                display = None
            else:
                display = nested_total - 1

            return render_template('/workflow.html', name=session['work_flow_name'], shape_list=shape_list,
                                   count=total, lastAxis=lastAxis, height=height, nestedTotal=nested_total, display=display)

        if request.form['submit'] == 'Delete':
            delete = request.form['flowName']
            print('delete', delete)
            sql = """DELETE FROM work_flow where work_flow_name = %s;"""
            cursor = db.cursor()
            cursor.execute(sql, (session['work_flow_name'],))
            db.commit()
            cursor.close()
            return redirect(url_for('add_work_flow'))
        if request.form['submit'] == 'nestedId':
            id = request.form['input_type']

            print('ID', id)
            print(session_shape_list)
            shape_list, shape_id, parent_id = shape_db(session_shape_list, id)
            session['parent_id'] = parent_id
            if parent_id not in session_parent_id:
                session_parent_id.append(parent_id)
            print('parentID', parent_id)
            print('parent_id',session['parent_id'])
            print('shape list', shape_list)
            if shape_list:
                if session_shape_list[-1] != shape_list:
                    print('not equal')
                    session_shape_list.append(shape_list)
                    print('session', session_shape_list)
            nested_total = len(session_parent_id)
            if nested_total <= 1:
                display=None
            else:
                display= nested_total - 1
            print('display', display)
            total = len(shape_list)
            if total > 2:
                height = 250 * len(shape_list) + 100
            else:
                height = 600
            return render_template('/workflow.html', name=session['work_flow_name'], shape_list=shape_list,
                                   count=total, height=height, nestedTotal=nested_total, display=display)

        if request.form['submit'] == 'parentWorkflow':
            parent = request.form['parentWF']
            # session_shape_list.pop(-1)
            session_parent_id.clear()
            shape_list = session_shape_list[0]
            del session_shape_list[1:]
            print('after delete', session_shape_list)
            print(session_parent_id)
            total = len(shape_list)
            if total > 2:
                height = 250 * len(shape_list) + 100
            else:
                height = 600
            print(shape_list)

            print('final shape list', shape_list)
            render_template('/workflow.html', name=session['work_flow_name'], shape_list=shape_list,
                                   count=total, height=height)

        if request.form['submit'] == 'nestedParent':
            nested_parent_id = request.form['nestedParentWF']
            print('before', session_shape_list)
            print(len(session_shape_list), len(session_parent_id))
            if len(session_shape_list) != len(session_parent_id):
                session_shape_list.pop(-1)
            session_parent_id.pop(-1)

            session['parent_id'] = session_parent_id[-1]
            nested_total = len(session_parent_id)
            if nested_total <= 1:
                display = None
            else:
                display = nested_total - 1
            print('display', display)
            print('session parent id',session_parent_id)
            print('sessionshapelist',session_shape_list)
            shape_list = session_shape_list[-1]
            print('ses', session_shape_list)
            total = len(shape_list)
            if total > 2:
                height = 250 * len(shape_list) + 100
            else:
                height = 600


        render_template('/workflow.html', name=session['work_flow_name'], shape_list=shape_list,
                        count=total, height=height, nestedTotal=nested_total, display=display)


    return render_template('workflow.html', shape_list=shape_list, count=total, height=height, nestedTotal=nested_total, display=display)

def last_shape_axis(lastshapeid):
    if lastshapeid != []:
        print(lastshapeid, lastshapeid[0])
        sID = lastshapeid[0]
        for item in session['shape_list'][-1]:
            if int(item[0]) == int(sID):
                lastAxis = item[5]
                print('last', lastAxis)
                break

    return lastAxis

def total_shape_count():
    total = len(session_shape_list[-1])
    if total > 2:
        height = 250 * len(session_shape_list[-1]) + 100
    else:
        height = 600
    return  height


if __name__ == '__main__':
    app.secret_key = 'aheexbeeuqo299ee29'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
