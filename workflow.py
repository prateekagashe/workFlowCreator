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

def shape_db(shape_list, shape_id):
    sql = """select shape_sequence_id, shape_name, shape_type.shape_type, shape_desc, unique_id from shape_details 
    left join shape_type on shape_type.shape_type_id = shape_details.shape_type_id left join work_flow
     on work_flow.work_flow_id = shape_details.work_flow_id where work_flow_name = %s and parent_id is null"""
    cursor = db.cursor()
    cursor.execute(sql, (session['work_flow_name'],))
    rows = cursor.fetchall()
    print("from sql", rows)
    cursor.close()
    for item in rows:
        shape_list.append(list(item))
        shape_id.append(item[0])
    shape_list = sort_list(shape_list)

    return shape_list, shape_id


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

