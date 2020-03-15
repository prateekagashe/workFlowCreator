from database import db
from flask import session
def database():
    work_flow_list = []
    cursor = db.cursor()
    cursor.execute("select work_flow_name from work_flow;")
    rows = cursor.fetchall()
    if rows != '':
        for items in rows:
            for names in items:
                work_flow_list.append(names)


    db.commit()
    cursor.close()
    return work_flow_list

def shape_db(session_shape_list, id=0, parent_id=0):
    shape_list = []
    shape_id = []
    print('ses', session_shape_list)
    print('from app', id)

    if id != 0:
        for item in session_shape_list[-1]:
            print('inside for', item, item[0], id)
            if int(item[0]) == int(id):
                parent_id = item[4]
                print(parent_id)
                break
    if parent_id == 0:
        sql = """select shape_sequence_id, shape_name, shape_type.shape_type, shape_desc, unique_id from shape_details 
        left join shape_type on shape_type.shape_type_id = shape_details.shape_type_id left join work_flow
         on work_flow.work_flow_id = shape_details.work_flow_id where work_flow_name = %s and parent_id is null"""

        data = (session['work_flow_name'],)
    else:
        sql= """select shape_sequence_id, shape_name, shape_type.shape_type, shape_desc, unique_id from shape_details 
        left join shape_type on shape_type.shape_type_id = shape_details.shape_type_id left join work_flow
         on work_flow.work_flow_id = shape_details.work_flow_id where work_flow_name = %s and parent_id = %s"""
        data = (session['work_flow_name'], parent_id,)
    cursor = db.cursor()
    cursor.execute(sql, data)
    rows = cursor.fetchall()
    print("from sql", rows)
    cursor.close()
    if rows:
        for item in rows:
            shape_list.append(list(item))
            shape_id.append(item[0])
        shape_list = sort_list(shape_list)
    else:
        shape_list.clear()
        shape_id.clear()
    return shape_list, shape_id, parent_id


def axis(li):
    global num, y
    num = 0
    y = 100
    for item in li:
        num = num + 1
        if len(li) == 1 or li.index(item) == 0:
            if len(item) > 9:
                item[9] = y
                item[10] = num
            else:
                item.insert(9, y)
                item.insert(10, num)
        else:
            y = y + 250
            y = y
            if len(item) > 9:
                item[9] = y
                item[10] = num
            else:
                item.insert(9, y)
                item.insert(10, num)
    return(li)




def sort_list(shape_list):

    shape_list.sort(key=lambda x: x[0])
    final = axis(shape_list)
    return final

