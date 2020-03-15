from flask import Flask, render_template, request, redirect, url_for, flash
# from flask.ext.session import Session
import mysql.connector
import json
import app
cred=[]

with open("dbCredentials.txt") as f:
    for line in f:
        cred.append(line)

host = cred[0][6:-2]
db = cred[1][10:-2]
user = cred[2][6:-2]
pd = cred[3][10:-1]
mydb = mysql.connector.connect(
    host=host,
    database = db,
    user=user,
    passwd=pd
)

app = Flask(__name__)
# sess - Session()
shape = ''
shapeName = 0
y = 100
heightNested = 600
lastShapeId = []
total = 0
nestedTotal = 0
num = 0
shape_list = []
height = 0
data = {}
final= ''
subShapeId = ''
finalNested = ''
finalSubNested = ''
id = []
flowChartList = []
fl = []
error = ''
flowChartName = ''
lastAxis = ''
nestedId = []
subNestedId = []
nestedShapeList = []
level4ShapeList = []
level4DelId = []
level5ShapeList = []
level6ShapeList = []
level7ShapeList = []
level8ShapeList = []
level9ShapeList = []
level10ShapeList = []
level5DelId = []
level6DelId = []
level7DelId = []
level8DelId = []
level9DelId = []
level10DelId = []
finallevel1 = []
finallevel2 = []
finallevel3 = []
finallevel4 = []
finallevel5 = []
finallevel6 = []
finallevel7 = []
finallevel8 = []
finallevel9 = []

finallevel10 = []
uniqueID = ''
subNestedShapeList = []
levelList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
parentID = ''
subNestedDelId = ''


def flowChart():
    cursor = mydb.cursor()
    cursor.execute("select distinct(flowChartName) from flowCharts;")
    rows = cursor.fetchall()
    print(rows)
    if rows != ():
        for item in rows:
            flowChartList.append(list(item))
            print(list(item))
        for i in flowChartList:
            if i[0] not in fl:
                fl.append(i[0])

        cursor.close()

    return


@app.route('/', methods=['GET', 'POST'])
def user_input():
    global shape, shapeName, y, count, total, num, delId, error, final, finallevel4, finallevel5 ,finallevel6,\
        finallevel7, finallevel8, finallevel9,levelList, finalSubNested, shapeId, subShapeId, shapeDesc, height,\
        heightNested, flowChartName, shape_list, id, lastShapeId, lastAxis, finalNested, nestedTotal, nestedId,\
        nestedShapeList, parentID, subNestedShapeList, level4ShapeList, level5ShapeList, level6ShapeList,\
        level7ShapeList, level8ShapeList, level9ShapeList, level10ShapeList, subNestedId, subNestedDelId, uniqueID
    flowChart()

    if request.method == 'POST':
        if request.form['submit'] == 'Add':
            shapeId = request.form['shapeId']
            shapeName = request.form['shapeHeading'].lower()
            shape = request.form['shape']
            shapeDesc = request.form['description']
            condition1 = request.form['condition_1']
            condition2 = request.form['condition_2']
            condition3 = request.form['condition_3']
            condition4 = request.form['condition_4']

            print('Conditions', condition1, condition2, condition3, condition4)

            y = 100
            num = 0
            shapeDesc = shapeDesc.replace('\n', '<br>').replace('\r', '<br>')
            print('Shape Desc', shapeDesc)
            print('After retrieval', id)
            lastShapeId.clear()
            lastShapeId.append(shapeId)
            print('Type of shapeId', type(shapeId))

            print("inside add", flowChartName)

            print('Id Shape', id)
            print('SHAPE ID', shapeId)
            if int(shapeId) in id and shapeId != '':
                error = "Shape id already used, please use a different id."
                errorType = "Duplicate shape id"
                return render_template('index.html', value=shape, height=height, heading=shapeName,  shape_list=final,
                                       count=total,  flowChartName=fl, lastAxis=lastAxis, flowChart=flowChartName.upper(), error=error, type=errorType, canvasID="canvas")
            else:
                if flowChartName != '':
                    print('flowchartname', flowChartName)
                    # ######Database############
                    sql = "INSERT INTO shapeDetails(FlowChartId, ParentId, ShapeId, ShapeHeading, " \
                          "ShapeTypeId, ShapeDesc, condition1, condition2, condition3, condition4)" \
                          " VALUES((select flowChartId from flowCharts where flowChartName = %s), " \
                          "%s, %s, %s, (select shapeTypeID from shapeType where shapeType = %s), %s, %s, %s, %s, %s)"
                    data = (flowChartName, None,  shapeId, shapeName, shape, shapeDesc, condition1, condition2, condition3, condition4)

                    cursor = mydb.cursor()

                    cursor.execute(sql, data)
                    mydb.commit()
                    cursor.close()


                    # print(id)
                    # id.append(int(shapeId))
                    # shape_list.append([int(shapeId), shapeName, shape, shapeDesc])
                    id = []
                    shape_list = []
                    database()
                    print("Before sort")
                    print(shape_list)
                    print(final)

        if request.form['submit'] == 'DeleteShape':
             delId = request.form['delId']
             print(delId)
             if delId != '':
                 if flowChartName != '':
                     cursor = mydb.cursor()
                     cursor.execute("""DELETE FROM shapeDetails WHERE flowChartId = (select flowChartId from flowCharts where flowChartName =  %s) and shapeId = %s and ParentId is null;""", (flowChartName, delId))
                     mydb.commit()
                     cursor.close()
                     shape_list = []
                     id = []
                     database()
                     print(final)
        if request.form['submit'] == 'nestedDeleteShape':
            nestedDelId = request.form['nestedDelId']
            # parentDelId = request.form['parentDelId']
            print('Deleted Id = ', nestedDelId, parentID)
            if nestedDelId != '':
                if flowChartName != '':
                    for item in final:
                        if int(item[0]) == int(parentID):
                            uniqueID = item[4]
                            print('UNique id', uniqueID)
                    cursor = mydb.cursor()
                    cursor.execute(
                        """DELETE FROM shapeDetails WHERE flowChartId = (select flowChartId from flowCharts where flowChartName =  %s) and shapeId = %s and parentId = %s;""",
                        (flowChartName, nestedDelId, uniqueID))
                    mydb.commit()
                    cursor.close()
                    nestedShapeList = []
                    nestedShapeId = []
                    databaseNested(uniqueID)
                    print('Deleted shapes', nestedShapeList)
                    nestedli = sort(nestedShapeList)
                    finalNested = axis(nestedli)
                    nestedTotal = len(finalNested)
                    if nestedTotal > 2:
                        heightNested = 250 * len(finalNested) + 100
                    else:
                        heightNested = 600
                        print('nestedShapeList', finalNested)
                if len(nestedShapeList) == 0:
                    display = 'HE:LL::OOO'
                    return render_template('index.html', value=shape, heading=shapeName,
                                           count=nestedTotal, heightNested=heightNested,
                                           displayNestedCanvas=display, flowChartName=fl, lastAxis=lastAxis,
                                           flowChart=flowChartName.upper(), canvasID="nestedCanvas")
                else:
                    return render_template('index.html', value=shape, heading=shapeName, shape_list=finalNested,
                                           count=nestedTotal,
                                           heightNested=heightNested, flowChartName=fl, lastAxis=lastAxis,
                                           flowChart=flowChartName.upper(), canvasID="nestedCanvas")


        # level 3 delete
        if request.form['submit'] == 'level_3_delete':
            nestedDelId = request.form['nestedDelId']
            # parentDelId = request.form['parentDelId']
            print('Deleted Id = ', nestedDelId, parentID)
            if nestedDelId != '':
                if flowChartName != '':
                    for item in finalNested:
                        if int(item[0]) == int(parentID):
                            uniqueID = item[4]
                            print('UNique id level 3', uniqueID)
                    cursor = mydb.cursor()
                    cursor.execute(
                        """DELETE FROM shapeDetails WHERE flowChartId = (select flowChartId from flowCharts where flowChartName =  %s) and shapeId = %s and parentId = %s;""",
                        (flowChartName, nestedDelId, uniqueID))
                    mydb.commit()
                    cursor.close()
                    cursor.close()
                    subNestedId = []
                    subNestedShapeList = []
                    databaselevel3(uniqueID)

                    nestedli = sort(subNestedShapeList)
                    finalSubNested = axis(nestedli)
                    nestedTotal = len(finalSubNested)
                    if nestedTotal > 2:
                        heightSubNested = 250 * len(finalSubNested) + 100
                    else:
                        heightSubNested = 600
                        if nestedTotal > 2:
                            heightSubNested = 250 * len(finalSubNested) + 100
                        else:
                            heightSubNested = 600
                if len(subNestedShapeList) == 0:
                    display = 'HE:LL::OOO'
                    return render_template('index.html', value=shape, heading=shapeName,
                                           count=nestedTotal, heightSubNested=heightSubNested,
                                           displayNestedCanvasLevel2=display, flowChartName=fl,
                                           lastAxis=lastAxis,
                                           flowChart=flowChartName.upper(), canvasID="nestedCanvasLevel2",
                                           displayCanvas='displayCanvas')
                else:
                    return render_template('index.html', value=shape, heading=shapeName,
                                           shape_list=finalSubNested,
                                           count=nestedTotal,
                                           heightSubNested=heightSubNested, flowChartName=fl, lastAxis=lastAxis,
                                           flowChart=flowChartName.upper(), canvasID="nestedCanvasLevel2",
                                           displayCanvas='displayCanvas')

        # level 4 delete
        if request.form['submit'] == 'level_4_delete':
            nestedDelId = request.form['nestedDelId']
            # parentDelId = request.form['parentDelId']
            print('Deleted Id = ', nestedDelId, parentID)
            if nestedDelId != '':
                if flowChartName != '':
                    for item in finalSubNested:
                        if int(item[0]) == int(parentID):
                            uniqueID = item[4]
                            print('UNique id level 4', uniqueID)
                    cursor = mydb.cursor()
                    cursor.execute(
                        """DELETE FROM shapeDetails WHERE flowChartId = (select flowChartId from flowCharts where flowChartName =  %s) and shapeId = %s and parentId = %s;""",
                        (flowChartName, nestedDelId, uniqueID))
                    mydb.commit()
                    cursor.close()
                    cursor.close()
                    level4DelId = []
                    level4ShapeList = []
                    databaselevel4(uniqueID)
                    print("Level 4 shape list", level4ShapeList)
                    nestedli = sort(level4ShapeList)
                    finallevel4 = axis(nestedli)
                    nestedTotal = len(finallevel4)
                    if nestedTotal > 2:
                        level4Height = 250 * len(finallevel4) + 100
                    else:
                        level4Height = 600
                if len(level4ShapeList) == 0:
                    display = 'HE:LL::OOO'
                    return render_template('index.html', value=shape, heading=shapeName,
                                           count=nestedTotal, level4Height=level4Height,
                                           displayNestedCanvasLevel3=display, flowChartName=fl,
                                           lastAxis=lastAxis,
                                           flowChart=flowChartName.upper(), canvasID="nestedCanvasLevel4",
                                           displayCanvas='displayCanvas')
                else:
                    return render_template('index.html', value=shape, heading=shapeName, shape_list=finallevel4,
                                           count=nestedTotal,
                                           level4Height=level4Height, flowChartName=fl, lastAxis=lastAxis,
                                           flowChart=flowChartName.upper(), canvasID="nestedCanvasLevel4",
                                           displayCanvas='displayCanvas')

        #     level 5 delete
        if request.form['submit'] == 'level_5_delete':
            nestedDelId = request.form['nestedDelId']
            # parentDelId = request.form['parentDelId']
            print('Deleted Id = ', nestedDelId, parentID)
            if nestedDelId != '':
                if flowChartName != '':
                    for item in finallevel4:
                        if int(item[0]) == int(parentID):
                            uniqueID = item[4]
                            print('UNique id level 5', uniqueID)
                    cursor = mydb.cursor()
                    cursor.execute(
                        """DELETE FROM shapeDetails WHERE flowChartId = (select flowChartId from flowCharts where flowChartName =  %s) and shapeId = %s and parentId = %s;""",
                        (flowChartName, nestedDelId, uniqueID))
                    mydb.commit()
                    cursor.close()
                    level5DelId = []
                    level5ShapeList = []
                    databaselevel5(uniqueID)

                    nestedli = sort(level5ShapeList)
                    finallevel5 = axis(nestedli)
                    nestedTotal = len(finallevel5)
                if nestedTotal > 2:
                    level5Height = 250 * len(finallevel5) + 100
                else:
                    level5Height = 600
            if len(level5ShapeList) == 0:
                display = 'HE:LL::OOO'
                return render_template('index.html', value=shape, heading=shapeName,
                                       count=nestedTotal, level5Height=level5Height,
                                       displayNestedCanvasLevel4=display, flowChartName=fl, lastAxis=lastAxis,
                                       flowChart=flowChartName.upper(), canvasID="nestedCanvasLevel5",
                                       displayCanvas='displayCanvas')
            else:
                return render_template('index.html', value=shape, heading=shapeName, shape_list=finallevel5,
                                       count=nestedTotal,
                                       level5Height=level5Height, flowChartName=fl, lastAxis=lastAxis,
                                       flowChart=flowChartName.upper(), canvasID="nestedCanvasLevel5",
                                       displayCanvas='displayCanvas')
        #     level 6 delete
        if request.form['submit'] == 'level_6_delete':
            nestedDelId = request.form['nestedDelId']
            # parentDelId = request.form['parentDelId']
            print('Deleted Id = ', nestedDelId, parentID)
            if nestedDelId != '':
                if flowChartName != '':
                    for item in finallevel5:
                        if int(item[0]) == int(parentID):
                            uniqueID = item[4]
                            print('UNique id level 6', uniqueID)
                    cursor = mydb.cursor()
                    cursor.execute(
                        """DELETE FROM shapeDetails WHERE flowChartId = (select flowChartId from flowCharts where flowChartName =  %s) and shapeId = %s and parentId = %s;""",
                        (flowChartName, nestedDelId, uniqueID))
                    mydb.commit()
                    cursor.close()
                    level6DelId = []
                    level6ShapeList = []
                    databaselevel6(uniqueID)
                    print("After datbase level 6", level6ShapeList)
                    nestedli = sort(level6ShapeList)
                    finallevel6 = axis(nestedli)
                    nestedTotal = len(finallevel6)
                    print("Level 6", finallevel6)
                if nestedTotal > 2:
                    level6Height = 250 * len(finallevel6) + 100
                else:
                    level6Height = 600

            if len(level6ShapeList) == 0:
                display = 'HE:LL::OOO'
                return render_template('index.html', value=shape, heading=shapeName,
                                       count=nestedTotal, level6Height=level6Height,
                                       displayNestedCanvasLevel5=display, flowChartName=fl, lastAxis=lastAxis,
                                       flowChart=flowChartName.upper(), canvasID="nestedCanvasLevel6",
                                       displayCanvas='displayCanvas')
            else:
                return render_template('index.html', value=shape, heading=shapeName, shape_list=finallevel6,
                                       count=nestedTotal,
                                       level6Height=level6Height, flowChartName=fl, lastAxis=lastAxis,
                                       flowChart=flowChartName.upper(), canvasID="nestedCanvasLevel6",
                                       displayCanvas='displayCanvas')
        #     level 7 delete
        if request.form['submit'] == 'level_7_delete':
            nestedDelId = request.form['nestedDelId']
            # parentDelId = request.form['parentDelId']
            print('Deleted Id = ', nestedDelId, parentID)
            if nestedDelId != '':
                if flowChartName != '':
                    for item in finallevel6:
                        if int(item[0]) == int(parentID):
                            uniqueID = item[4]
                            print('UNique id level 7', uniqueID)
                    cursor = mydb.cursor()
                    cursor.execute(
                        """DELETE FROM shapeDetails WHERE flowChartId = (select flowChartId from flowCharts where flowChartName =  %s) and shapeId = %s and parentId = %s;""",
                        (flowChartName, nestedDelId, uniqueID))
                    mydb.commit()
                    cursor.close()
                    level7DelId = []
                    level7ShapeList = []
                    databaselevel7(uniqueID)

                    nestedli = sort(level7ShapeList)
                    finallevel7 = axis(nestedli)
                    nestedTotal = len(finallevel7)
                if nestedTotal > 2:
                    level7Height = 250 * len(finallevel7) + 100
                else:
                    level7Height = 600
                    #

            if len(level7ShapeList) == 0:
                display = 'HE:LL::OOO'
                return render_template('index.html', value=shape, heading=shapeName,
                                       count=nestedTotal, level7Height=level7Height,
                                       displayNestedCanvasLevel6=display, flowChartName=fl, lastAxis=lastAxis,
                                       flowChart=flowChartName.upper(), canvasID="nestedCanvasLevel7",
                                       displayCanvas='displayCanvas')
            else:
                return render_template('index.html', value=shape, heading=shapeName, shape_list=finallevel7,
                                       count=nestedTotal,
                                       level7Height=level7Height, flowChartName=fl, lastAxis=lastAxis,
                                       flowChart=flowChartName.upper(), canvasID="nestedCanvasLevel7",
                                       displayCanvas='displayCanvas')

        # level 8 delete
        if request.form['submit'] == 'level_8_delete':
            nestedDelId = request.form['nestedDelId']
            # parentDelId = request.form['parentDelId']
            print('Deleted Id = ', nestedDelId, parentID)
            if nestedDelId != '':
                if flowChartName != '':
                    for item in finallevel7:
                        if int(item[0]) == int(parentID):
                            uniqueID = item[4]
                            print('UNique id level 7', uniqueID)
                    cursor = mydb.cursor()
                    cursor.execute(
                        """DELETE FROM shapeDetails WHERE flowChartId = (select flowChartId from flowCharts where flowChartName =  %s) and shapeId = %s and parentId = %s;""",
                        (flowChartName, nestedDelId, uniqueID))
                    mydb.commit()
                    cursor.close()
                    #
                    level8DelId = []
                    level8ShapeList = []
                    databaselevel8(uniqueID)
                    print('level 8 after database ', level8ShapeList)
                    nestedli = sort(level8ShapeList)
                    finallevel8 = axis(nestedli)
                    nestedTotal = len(finallevel8)
                if nestedTotal > 2:
                    level8Height = 250 * len(finallevel8) + 100
                else:
                    level8Height = 600
                    #

            if len(level8ShapeList) == 0:
                display = 'HE:LL::OOO'
                return render_template('index.html', value=shape, heading=shapeName,
                                       count=nestedTotal, level8Height=level8Height,
                                       displayNestedCanvasLevel7=display, flowChartName=fl, lastAxis=lastAxis,
                                       flowChart=flowChartName.upper(), canvasID="nestedCanvasLevel8",
                                       displayCanvas='displayCanvas')
            else:
                return render_template('index.html', value=shape, heading=shapeName, shape_list=finallevel8,
                                       count=nestedTotal,
                                       level8Height=level8Height, flowChartName=fl, lastAxis=lastAxis,
                                       flowChart=flowChartName.upper(), canvasID="nestedCanvasLevel8",
                                       displayCanvas='displayCanvas')
        #     level 9 delete
        if request.form['submit'] == 'level_9_delete':
            nestedDelId = request.form['nestedDelId']
            # parentDelId = request.form['parentDelId']
            print('Deleted Id = ', nestedDelId, parentID)
            if nestedDelId != '':
                if flowChartName != '':
                    for item in finallevel8:
                        if int(item[0]) == int(parentID):
                            uniqueID = item[4]
                            print('UNique id level 9', uniqueID)
                    cursor = mydb.cursor()
                    cursor.execute(
                        """DELETE FROM shapeDetails WHERE flowChartId = (select flowChartId from flowCharts where flowChartName =  %s) and shapeId = %s and parentId = %s;""",
                        (flowChartName, nestedDelId, uniqueID))
                    mydb.commit()
                    cursor.close()
                    #
                    level9DelId = []
                    level9ShapeList = []
                    databaselevel9(uniqueID)
                    ('level 9 delete after database', level9ShapeList)
                    nestedli = sort(level9ShapeList)
                    finallevel9 = axis(nestedli)
                    nestedTotal = len(finallevel9)
                if nestedTotal > 2:
                    level9Height = 250 * len(finallevel9) + 100
                else:
                    level9Height = 600

            if len(level9ShapeList) == 0:
                display = 'HE:LL::OOO'
                return render_template('index.html', value=shape, heading=shapeName,
                                       count=nestedTotal, level9Height=level9Height,
                                       displayNestedCanvasLevel8=display, flowChartName=fl, lastAxis=lastAxis,
                                       flowChart=flowChartName.upper(), canvasID="nestedCanvasLevel9",
                                       displayCanvas='displayCanvas')
            else:
                return render_template('index.html', value=shape, heading=shapeName, shape_list=finallevel9,
                                       count=nestedTotal,
                                       level9Height=level9Height, flowChartName=fl, lastAxis=lastAxis,
                                       flowChart=flowChartName.upper(), canvasID="nestedCanvasLevel9",
                                       displayCanvas='displayCanvas')
        #     level 10 delete
        if request.form['submit'] == 'level_10_delete':
            nestedDelId = request.form['nestedDelId']
            # parentDelId = request.form['parentDelId']
            print('Deleted Id = ', nestedDelId, parentID)
            if nestedDelId != '':
                if flowChartName != '':
                    for item in finallevel9:
                        if int(item[0]) == int(parentID):
                            uniqueID = item[4]
                            print('UNique id level 10', uniqueID)
                    cursor = mydb.cursor()
                    cursor.execute(
                        """DELETE FROM shapeDetails WHERE flowChartId = (select flowChartId from flowCharts where flowChartName =  %s) and shapeId = %s and parentId = %s;""",
                        (flowChartName, nestedDelId, uniqueID))
                    mydb.commit()
                    cursor.close()
                    #
                    level10DelId = []
                    level10ShapeList = []
                    databaselevel10(uniqueID)
                    ('level 10 after database', level10ShapeList)

                    nestedli = sort(level10ShapeList)
                    finallevel10 = axis(nestedli)
                    nestedTotal = len(finallevel10)
                if nestedTotal > 2:
                    level10Height = 250 * len(finallevel10) + 100
                else:
                    level10Height = 600

            if len(level10ShapeList) == 0:
                display = 'HE:LL::OOO'
                return render_template('index.html', value=shape, heading=shapeName,
                                       count=nestedTotal, level10Height=level10Height,
                                       displayNestedCanvasLevel9=display, flowChartName=fl, lastAxis=lastAxis,
                                       flowChart=flowChartName.upper(), canvasID="nestedCanvasLevel10",
                                       displayCanvas='displayCanvas')
            else:
                return render_template('index.html', value=shape, heading=shapeName, shape_list=finallevel10,
                                       count=nestedTotal,
                                       level10Height=level10Height, flowChartName=fl, lastAxis=lastAxis,
                                       flowChart=flowChartName.upper(), canvasID="nestedCanvasLevel10",
                                       displayCanvas='displayCanvas')
            # level 2 modify
        if request.form['submit'] == 'Modify Shape':
            modId = request.form['modId']
            modHeading = request.form['modHeading']
            modShape = request.form['modShape']
            modDesc = request.form['modDesc']
            originalId = request.form['originalId']
            modShape = modShape.lower()
            print(modId, modShape, modHeading, modDesc)
            print(originalId)
            lastShapeId.clear()
            lastShapeId.append(modId)
            modDesc = modDesc.replace('\n', '<br>').replace('\r', '<br>')

            if originalId == modId:
                cursor = mydb.cursor()

                cursor.execute("""Update shapeDetails set shapeHeading = %s, shapeTypeID = (select shapeTypeID from 
                shapeType where shapeType = %s ), shapeDesc = %s where shapeId = %s and flowChartId = 
                (select flowChartId from flowCharts where flowChartName = %s) and parentId is null;""",
                               (modHeading, modShape, modDesc, modId, flowChartName))
                mydb.commit()
                cursor.close()
                # connection.close()
                for item in shape_list:
                    print("inside")
                    if item[0] == int(modId):
                        print("Equal")

                        item[1] = modHeading
                        item[2] = modShape
                        item[3] = modDesc
            else:
                if int(modId) in id and modId != '':
                    error = "Shape id already used, please use a different id."
                    errorType = "Duplicate shape id"
                    return render_template('index.html', value=shape, height=height, heading=shapeName,
                                           shape_list=final,
                                           count=total, flowChartName=fl, lastAxis=lastAxis,
                                           flowChart=flowChartName.upper(), error=error, type=errorType,
                                           canvasID="canvas")
                else:

                    cursor = mydb.cursor()
                    cursor.execute(
                        """Update shapeDetails set shapeId = %s, shapeHeading = %s, shapeTypeID = (select shapeTypeID from shapeType where shapeType = %s ), shapeDesc = %s where shapeId = %s and flowChartId = (select flowChartId from flowCharts where flowChartName = %s) and parentId is null;""",
                        (modId, modHeading, modShape, modDesc, originalId, flowChartName))
                    mydb.commit()
                    cursor.close()
                    shape_list = []
                    id = []
                    database()

        # Level 1
        if request.form['submit'] == 'Modify Shape':
            modId = request.form['modId']
            modHeading = request.form['modHeading']
            modShape = request.form['modShape']
            modDesc = request.form['modDesc']
            originalId = request.form['originalId']
            modShape = modShape.lower()
            print(modId, modShape, modHeading, modDesc)
            print(originalId)
            lastShapeId.clear()
            lastShapeId.append(modId)
            modDesc = modDesc.replace('\n', '<br>').replace('\r', '<br>')

            if originalId == modId:
                cursor = mydb.cursor()

                cursor.execute("""Update shapeDetails set shapeHeading = %s, shapeTypeID = (select shapeTypeID from 
                shapeType where shapeType = %s ), shapeDesc = %s where shapeId = %s and flowChartId = 
                (select flowChartId from flowCharts where flowChartName = %s) and parentId is null;""",
                               (modHeading, modShape, modDesc, modId, flowChartName))
                mydb.commit()
                cursor.close()
                # connection.close()
                for item in shape_list:
                    print("inside")
                    if item[0] == int(modId):
                        print("Equal")

                        item[1] = modHeading
                        item[2] = modShape
                        item[3] = modDesc
            else:
                if int(modId) in id and modId != '':
                    error = "Shape id already used, please use a different id."
                    errorType = "Duplicate shape id"
                    return render_template('index.html', value=shape, height=height, heading=shapeName, shape_list=final,
                                       count=total, flowChartName = fl, lastAxis = lastAxis, flowChart = flowChartName.upper(), error= error, type=errorType, canvasID = "canvas")
                else:

                    cursor = mydb.cursor()
                    cursor.execute(
                        """Update shapeDetails set shapeId = %s, shapeHeading = %s, shapeTypeID = (select shapeTypeID from shapeType where shapeType = %s ), shapeDesc = %s where shapeId = %s and flowChartId = (select flowChartId from flowCharts where flowChartName = %s) and parentId is null;""",
                        (modId, modHeading, modShape, modDesc, originalId, flowChartName))
                    mydb.commit()
                    cursor.close()
                    shape_list = []
                    id = []
                    database()

            print(shape_list)
        if request.form['submit'] == 'Level_2_Add':
            nestedShapeId = request.form['shapeId']
            nestedShapeHeading = request.form['shapeHeading']
            nestedShape = request.form['shape']
            nestedDesc = request.form['description']
            condition1 = request.form['condition_1']
            condition2 = request.form['condition_2']
            condition3 = request.form['condition_3']
            condition4 = request.form['condition_4']
            # parentShapeId = request.form['nestedID']
            nestedDesc = nestedDesc.replace('\n', '<br>').replace('\r', '<br>')

            print('PARENT ID', parentID)
            # parentFlowChartName = request.form['nestedFlowChartName']
            # databaseNested(parentShapeId)
            print(nestedShapeId, nestedShapeHeading, nestedShape, nestedDesc, parentID)
            print('shape nested',  nestedShapeList, nestedId)
            if int(nestedShapeId) in nestedId and nestedShapeId != '':
                error = "Shape id already used, please use a different id."
                errorType = "Duplicate shape id"
                return render_template('index.html', value = shape, height = height, heading = shapeName,  shape_list = final, count = total,  flowChartName = fl, lastAxis = lastAxis, flowChart = flowChartName.upper(),error = error, type = errorType, canvasID = "canvas")
            else:
                # database()

                for item in final:
                    if int(item[0]) == int(parentID):
                        uniqueID = item[4]
                        break
                print('flowchartname', flowChartName)
                if flowChartName != '':

                    sql = "INSERT INTO shapeDetails(FlowChartId, ParentId, ShapeId, ShapeHeading, " \
                          "ShapeTypeId, ShapeDesc,  condition1, condition2, condition3, condition4)" \
                          "VALUES((select flowChartId from flowCharts where flowChartName = %s), " \
                          "%s, %s, %s, (select shapeTypeID from shapeType where shapeType = %s), %s, %s, %s, %s, %s)"
                    data = (flowChartName, uniqueID, nestedShapeId, nestedShapeHeading, nestedShape, nestedDesc,  condition1, condition2, condition3, condition4)
                    cursor = mydb.cursor()
                    cursor.execute(sql, data)
                    mydb.commit()
                    cursor.close()

                    for item in final:
                        if int(item[0]) == int(parentID):
                            uniqueID = item[4]

                            nestedId = []
                            nestedShapeList = []
                            databaseNested(uniqueID)

                    nestedli = sort(nestedShapeList)
                    finalNested = axis(nestedli)
                    nestedTotal = len(finalNested)
                if nestedTotal > 2:
                    heightNested = 250 * len(finalNested) + 100
                else:
                    heightNested = 600
            return render_template('index.html', value=shape, heading=shapeName,
                                   shape_list=finalNested, count=nestedTotal,
                                   heightNested=heightNested, flowChartName=fl, lastAxis=lastAxis,
                                   flowChart=flowChartName.upper(), canvasID="nestedCanvas")
        if request.form['submit'] == 'Level_3_Add':
            subNestedShapeId = request.form['shapeId']
            subNestedShapeHeading = request.form['shapeHeading']
            subNestedShape = request.form['shape']
            subNestedDesc = request.form['description']
            condition1 = request.form['condition_1']
            condition2 = request.form['condition_2']
            condition3 = request.form['condition_3']
            condition4 = request.form['condition_4']
            # parentShapeId = request.form['nestedID']
            print('PARENT ID', parentID)
            subNestedDesc = subNestedDesc.replace('\n', '<br>').replace('\r', '<br>')

            # parentFlowChartName = request.form['nestedFlowChartName']
            # databaseNested(parentShapeId)
            print(subNestedShapeId, subNestedShapeHeading, subNestedShape, subNestedDesc, parentID)
            print('shape nested',  nestedShapeList, nestedId)
            if int(subNestedShapeId) in nestedId and subNestedShapeId != '':
                error = "Shape id already used, please use a different id."
                errorType = "Duplicate shape id"
                return render_template('index.html', value = shape, height = height, heading = shapeName,  shape_list = final, count = total,  flowChartName = fl, lastAxis = lastAxis, flowChart = flowChartName.upper(),error = error, type = errorType, canvasID = "canvas")
            else:
                print('flowchartname', flowChartName)
                if flowChartName != '':
                    for item in finalNested:
                        if int(item[0]) == int(parentID):
                            uniqueID = item[4]
                            break
                    sql = "INSERT INTO shapeDetails(FlowChartId, ParentId, ShapeId, ShapeHeading, shapeTypeId," \
                          " ShapeDesc, condition1, condition2, condition3, condition4) " \
                          "VALUES((select flowChartId from flowCharts where flowChartName = %s), %s, %s, %s, " \
                          "(select shapeTypeID from shapeType where shapeType = %s), %s, %s, %s, %s, %s)"
                    data = (flowChartName, uniqueID, subNestedShapeId, subNestedShapeHeading, subNestedShape, subNestedDesc, condition1, condition2, condition3, condition4)
                    cursor = mydb.cursor()
                    cursor.execute(sql, data)
                    mydb.commit()
                    for item in final:
                        if item[0] == parentID:
                            uniqueID = item[4]
                    cursor.close()
                    subNestedId = []
                    subNestedShapeList = []
                    databaselevel3(uniqueID)
                    # subNestedId.append(int(subNestedShapeId))
                    # subNestedShapeList.append([int(subNestedShapeId), subNestedShapeHeading, subNestedShape, subNestedDesc])
                    nestedli = sort(subNestedShapeList)
                    finalSubNested = axis(nestedli)
                    nestedTotal = len(finalSubNested)
                if nestedTotal > 2:
                    heightSubNested = 250 * len(finalSubNested) + 100
                else:
                    heightSubNested = 600
            return render_template('index.html', value=shape, heading=shapeName, shape_list=finalSubNested, 
                                   count=nestedTotal,heightSubNested=heightSubNested, flowChartName=fl, 
                                   lastAxis=lastAxis, flowChart=flowChartName.upper(), canvasID = "nestedCanvasLevel2")

        if request.form['submit'] == 'Level_4_Add':
            nestedShapeId = request.form['shapeId']
            nestedShapeHeading = request.form['shapeHeading']
            nestedShape = request.form['shape']
            nestedDesc = request.form['description']
            condition1 = request.form['condition_1']
            condition2 = request.form['condition_2']
            condition3 = request.form['condition_3']
            condition4 = request.form['condition_4']
            print('PARENT ID', parentID)
            nestedDesc = nestedDesc.replace('\n', '<br>').replace('\r', '<br>')

            print(nestedShapeId, nestedShapeHeading, nestedShape, nestedDesc, parentID)
            print('shape nested',  nestedShapeList, nestedId)
            if int(nestedShapeId) in nestedId and nestedShapeId != '':
                error = "Shape id already used, please use a different id."
                errorType = "Duplicate shape id"
                return render_template('index.html', value = shape, level4Height=height, heading = shapeName,  shape_list = finallevel4, count = total,  flowChartName = fl, lastAxis = lastAxis, flowChart = flowChartName.upper(),error = error, type = errorType, canvasID = "canvas")
            else:

                for item in finalSubNested:
                    if int(item[0]) == int(parentID):
                        uniqueID = item[4]
                        break
                print('flowchartname', flowChartName)
                if flowChartName != '':

                    sql = "INSERT INTO shapeDetails(FlowChartId, ParentId, ShapeId, ShapeHeading, " \
                          "ShapeTypeId, ShapeDesc, condition1, condition2, condition3, condition4)" \
                          "VALUES((select flowChartId from flowCharts where flowChartName = %s), " \
                          "%s, %s, %s, (select shapeTypeID from shapeType where shapeType = %s), %s, %s, %s, %s, %s)"
                    data = (flowChartName, uniqueID, nestedShapeId, nestedShapeHeading, nestedShape, nestedDesc, condition1, condition2, condition3, condition4)
                    cursor = mydb.cursor()
                    cursor.execute(sql, data)
                    mydb.commit()
                    cursor.close()

                    for item in finalSubNested:
                        if item[0] == parentID:
                            uniqueID = item[4]

                    level4DelId = []
                    level4ShapeList = []
                    databaselevel4(uniqueID)
                    print("Level 4 shape list", level4ShapeList)
                    nestedli = sort(level4ShapeList)
                    finallevel4 = axis(nestedli)
                    nestedTotal = len(finallevel4)
                if nestedTotal > 2:
                    level4Height = 250 * len(finallevel4) + 100
                else:
                    level4Height = 600
            return render_template('index.html', value=shape, heading=shapeName,
                                   shape_list=finallevel4, count=nestedTotal,
                                   level4Height=level4Height, flowChartName=fl, lastAxis=lastAxis,
                                   flowChart=flowChartName.upper(), canvasID="nestedCanvasLevel4")

        if request.form['submit'] == 'Level_5_Add':
            nestedShapeId = request.form['shapeId']
            nestedShapeHeading = request.form['shapeHeading']
            nestedShape = request.form['shape']
            nestedDesc = request.form['description']
            condition1 = request.form['condition_1']
            condition2 = request.form['condition_2']
            condition3 = request.form['condition_3']
            condition4 = request.form['condition_4']
            print('PARENT ID', parentID)
            nestedDesc = nestedDesc.replace('\n', '<br>').replace('\r', '<br>')

            print(nestedShapeId, nestedShapeHeading, nestedShape, nestedDesc, parentID)
            print('shape nested', nestedShapeList, nestedId)
            if int(nestedShapeId) in nestedId and nestedShapeId != '':
                error = "Shape id already used, please use a different id."
                errorType = "Duplicate shape id"
                return render_template('index.html', value=shape, level4Height=height, heading=shapeName,
                                       shape_list=finallevel4, count=total, flowChartName=fl, lastAxis=lastAxis,
                                       flowChart=flowChartName.upper(), error=error, type=errorType, canvasID="canvas")
            else:

                for item in finallevel4:
                    if int(item[0]) == int(parentID):
                        uniqueID = item[4]
                        break
                print('flowchartname', flowChartName)
                if flowChartName != '':

                    sql = "INSERT INTO shapeDetails(FlowChartId, ParentId, ShapeId, ShapeHeading, " \
                          "ShapeTypeId, ShapeDesc, condition1, condition2, condition3, condition4)" \
                          "VALUES((select flowChartId from flowCharts where flowChartName = %s), " \
                          "%s, %s, %s, (select shapeTypeID from shapeType where shapeType = %s), %s, %s, %s, %s, %s)"
                    data = (flowChartName, uniqueID, nestedShapeId, nestedShapeHeading, nestedShape, nestedDesc, condition1, condition2, condition3, condition4)
                    cursor = mydb.cursor()
                    cursor.execute(sql, data)
                    mydb.commit()
                    cursor.close()

                    for item in finallevel4:
                        if item[0] == parentID:
                            uniqueID = item[4]

                    level5DelId = []
                    level5ShapeList = []
                    databaselevel5(uniqueID)

                    nestedli = sort(level5ShapeList)
                    finallevel5 = axis(nestedli)
                    nestedTotal = len(finallevel5)
                if nestedTotal > 2:
                    level5Height = 250 * len(finallevel5) + 100
                else:
                    level5Height = 600
            return render_template('index.html', value=shape, heading=shapeName,
                                   shape_list=finallevel5, count=nestedTotal,
                                   level5Height=level5Height, flowChartName=fl, lastAxis=lastAxis,
                                   flowChart=flowChartName.upper(), canvasID="nestedCanvasLevel5")

        if request.form['submit'] == 'Level_6_Add':
            nestedShapeId = request.form['shapeId']
            nestedShapeHeading = request.form['shapeHeading']
            nestedShape = request.form['shape']
            nestedDesc = request.form['description']
            condition1 = request.form['condition_1']
            condition2 = request.form['condition_2']
            condition3 = request.form['condition_3']
            condition4 = request.form['condition_4']
            print('PARENT ID', parentID)
            nestedDesc = nestedDesc.replace('\n', '<br>').replace('\r', '<br>')

            print(nestedShapeId, nestedShapeHeading, nestedShape, nestedDesc, parentID)
            print('shape nested', nestedShapeList, nestedId)
            if int(nestedShapeId) in nestedId and nestedShapeId != '':
                error = "Shape id already used, please use a different id."
                errorType = "Duplicate shape id"
                return render_template('index.html', value=shape, level4Height=height, heading=shapeName,
                                       shape_list=finallevel6, count=total, flowChartName=fl, lastAxis=lastAxis,
                                       flowChart=flowChartName.upper(), error=error, type=errorType, canvasID="canvas")
            else:

                for item in finallevel5:
                    if int(item[0]) == int(parentID):
                        uniqueID = item[4]
                        break
                print('flowchartname', flowChartName)
                if flowChartName != '':

                    sql = "INSERT INTO shapeDetails(FlowChartId, ParentId, ShapeId, ShapeHeading, " \
                          "ShapeTypeId, ShapeDesc, condition1, condition2, condition3, condition4)" \
                          "VALUES((select flowChartId from flowCharts where flowChartName = %s), " \
                          "%s, %s, %s, (select shapeTypeID from shapeType where shapeType = %s), %s, %s, %s, %s, %s)"
                    data = (flowChartName, uniqueID, nestedShapeId, nestedShapeHeading, nestedShape, nestedDesc, condition1, condition2, condition3, condition4)
                    cursor = mydb.cursor()
                    cursor.execute(sql, data)
                    mydb.commit()
                    cursor.close()

                    for item in finallevel5:
                        if item[0] == parentID:
                            uniqueID = item[4]

                    level6DelId = []
                    level6ShapeList = []
                    databaselevel6(uniqueID)
                    print("After datbase level 6", level6ShapeList)
                    nestedli = sort(level6ShapeList)
                    finallevel6 = axis(nestedli)
                    nestedTotal = len(finallevel6)
                    print("Level 6", finallevel6)
                if nestedTotal > 2:
                    level6Height = 250 * len(finallevel6) + 100
                else:
                    level6Height = 600
            return render_template('index.html', value=shape, heading=shapeName,
                                   shape_list=finallevel6, count=nestedTotal,
                                   level6Height=level6Height, flowChartName=fl, lastAxis=lastAxis,
                                   flowChart=flowChartName.upper(), canvasID="nestedCanvasLevel6")

        if request.form['submit'] == 'Level_7_Add':
            nestedShapeId = request.form['shapeId']
            nestedShapeHeading = request.form['shapeHeading']
            nestedShape = request.form['shape']
            nestedDesc = request.form['description']
            condition1 = request.form['condition_1']
            condition2 = request.form['condition_2']
            condition3 = request.form['condition_3']
            condition4 = request.form['condition_4']
            print('PARENT ID', parentID)
            nestedDesc = nestedDesc.replace('\n', '<br>').replace('\r', '<br>')

            print(nestedShapeId, nestedShapeHeading, nestedShape, nestedDesc, parentID)
            print('shape nested', nestedShapeList, nestedId)
            if int(nestedShapeId) in nestedId and nestedShapeId != '':
                error = "Shape id already used, please use a different id."
                errorType = "Duplicate shape id"
                return render_template('index.html', value=shape, level4Height=height, heading=shapeName,
                                       shape_list=finallevel7, count=total, flowChartName=fl, lastAxis=lastAxis,
                                       flowChart=flowChartName.upper(), error=error, type=errorType, canvasID="canvas")
            else:

                for item in finallevel6:
                    if int(item[0]) == int(parentID):
                        uniqueID = item[4]
                        break
                print('flowchartname', flowChartName)
                if flowChartName != '':

                    sql = "INSERT INTO shapeDetails(FlowChartId, ParentId, ShapeId, ShapeHeading, " \
                          "ShapeTypeId, ShapeDesc, condition1, condition2, condition3, condition4)" \
                          "VALUES((select flowChartId from flowCharts where flowChartName = %s), " \
                          "%s, %s, %s, (select shapeTypeID from shapeType where shapeType = %s), %s, %s, %s, %s, %s)"
                    data = (flowChartName, uniqueID, nestedShapeId, nestedShapeHeading, nestedShape, nestedDesc, condition1, condition2, condition3, condition4)
                    cursor = mydb.cursor()
                    cursor.execute(sql, data)
                    mydb.commit()
                    cursor.close()

                    for item in finallevel6:
                        if item[0] == parentID:
                            uniqueID = item[4]

                    level7DelId = []
                    level7ShapeList = []
                    databaselevel7(uniqueID)

                    nestedli = sort(level7ShapeList)
                    finallevel7 = axis(nestedli)
                    nestedTotal = len(finallevel7)
                if nestedTotal > 2:
                    level7Height = 250 * len(finallevel7) + 100
                else:
                    level7Height = 600
            return render_template('index.html', value=shape, heading=shapeName,
                                   shape_list=finallevel7, count=nestedTotal,
                                   level7Height=level7Height, flowChartName=fl, lastAxis=lastAxis,
                                   flowChart=flowChartName.upper(), canvasID="nestedCanvasLevel7")

        if request.form['submit'] == 'Level_8_Add':
            nestedShapeId = request.form['shapeId']
            nestedShapeHeading = request.form['shapeHeading']
            nestedShape = request.form['shape']
            nestedDesc = request.form['description']
            condition1 = request.form['condition_1']
            condition2 = request.form['condition_2']
            condition3 = request.form['condition_3']
            condition4 = request.form['condition_4']
            print('PARENT ID ', parentID)
            nestedDesc = nestedDesc.replace('\n', '<br>').replace('\r', '<br>')

            print(nestedShapeId, nestedShapeHeading, nestedShape, nestedDesc, parentID)
            print('shape nested', nestedShapeList, nestedId)
            if int(nestedShapeId) in nestedId and nestedShapeId != '':
                error = "Shape id already used, please use a different id."
                errorType = "Duplicate shape id"
                return render_template('index.html', value=shape, level4Height=height, heading=shapeName,
                                       shape_list=finallevel8, count=total, flowChartName=fl, lastAxis=lastAxis,
                                       flowChart=flowChartName.upper(), error=error, type=errorType,
                                       canvasID="canvas")
            else:

                for item in finallevel7:
                    if int(item[0]) == int(parentID):
                        uniqueID = item[4]
                        break
                print('flowchartname', flowChartName)
                if flowChartName != '':

                    sql = "INSERT INTO shapeDetails(FlowChartId, ParentId, ShapeId, ShapeHeading, " \
                          "ShapeTypeId, ShapeDesc, condition1, condition2, condition3, condition4)" \
                          "VALUES((select flowChartId from flowCharts where flowChartName = %s), " \
                          "%s, %s, %s, (select shapeTypeID from shapeType where shapeType = %s), %s, %s, %s, %s, %s)"
                    data = (flowChartName, uniqueID, nestedShapeId, nestedShapeHeading, nestedShape, nestedDesc, condition1, condition2, condition3, condition4)
                    cursor = mydb.cursor()
                    cursor.execute(sql, data)
                    mydb.commit()
                    cursor.close()

                    for item in finallevel7:
                        if item[0] == parentID:
                            uniqueID = item[4]

                    level8DelId = []
                    level8ShapeList = []
                    databaselevel8(uniqueID)
                    print('level 8 after database ', level8ShapeList)
                    nestedli = sort(level8ShapeList)
                    finallevel8 = axis(nestedli)
                    nestedTotal = len(finallevel8)
                if nestedTotal > 2:
                    level8Height = 250 * len(finallevel8) + 100
                else:
                    level8Height = 600
            return render_template('index.html', value=shape, heading=shapeName,
                                   shape_list=finallevel8, count=nestedTotal,
                                   level8Height=level8Height, flowChartName=fl, lastAxis=lastAxis,
                                   flowChart=flowChartName.upper(), canvasID="nestedCanvasLevel8")

        if request.form['submit'] == 'Level_9_Add':
            nestedShapeId = request.form['shapeId']
            nestedShapeHeading = request.form['shapeHeading']
            nestedShape = request.form['shape']
            nestedDesc = request.form['description']
            condition1 = request.form['condition_1']
            condition2 = request.form['condition_2']
            condition3 = request.form['condition_3']
            condition4 = request.form['condition_4']
            print('PARENT ID', parentID)
            nestedDesc = nestedDesc.replace('\n', '<br>').replace('\r', '<br>')

            print(nestedShapeId, nestedShapeHeading, nestedShape, nestedDesc, parentID)
            print('shape nested', nestedShapeList, nestedId)
            if int(nestedShapeId) in nestedId and nestedShapeId != '':
                error = "Shape id already used, please use a different id."
                errorType = "Duplicate shape id"
                return render_template('index.html', value=shape, level4Height=height, heading=shapeName,
                                       shape_list=finallevel9, count=total, flowChartName=fl, lastAxis=lastAxis,
                                       flowChart=flowChartName.upper(), error=error, type=errorType,
                                       canvasID="canvas")
            else:

                for item in finallevel8:
                    if int(item[0]) == int(parentID):
                        uniqueID = item[4]
                        break
                print('flowchartname', flowChartName)
                if flowChartName != '':

                    sql = "INSERT INTO shapeDetails(FlowChartId, ParentId, ShapeId, ShapeHeading, " \
                          "ShapeTypeId, ShapeDesc, condition1, condition2, condition3, condition4)" \
                          "VALUES((select flowChartId from flowCharts where flowChartName = %s), " \
                          "%s, %s, %s, (select shapeTypeID from shapeType where shapeType = %s), %s, %s, %s, %s, %s)"
                    data = (flowChartName, uniqueID, nestedShapeId, nestedShapeHeading, nestedShape, nestedDesc, condition1, condition2, condition3, condition4)
                    cursor = mydb.cursor()
                    cursor.execute(sql, data)
                    mydb.commit()
                    cursor.close()

                    for item in finallevel8:
                        if item[0] == parentID:
                            uniqueID = item[4]

                    level9DelId = []
                    level9ShapeList = []
                    databaselevel9(uniqueID)
                    ('level 9 after database', level9ShapeList)
                    nestedli = sort(level9ShapeList)
                    finallevel9 = axis(nestedli)
                    nestedTotal = len(finallevel9)
                if nestedTotal > 2:
                    level9Height = 250 * len(finallevel9) + 100
                else:
                    level9Height = 600
            return render_template('index.html', value=shape, heading=shapeName,
                                   shape_list=finallevel9, count=nestedTotal,
                                   level9Height=level9Height, flowChartName=fl, lastAxis=lastAxis,
                                   flowChart=flowChartName.upper(), canvasID="nestedCanvasLevel9")

        if request.form['submit'] == 'Level_10_Add':
            nestedShapeId = request.form['shapeId']
            nestedShapeHeading = request.form['shapeHeading']
            nestedShape = request.form['shape']
            nestedDesc = request.form['description']
            condition1 = request.form['condition_1']
            condition2 = request.form['condition_2']
            condition3 = request.form['condition_3']
            condition4 = request.form['condition_4']
            print('PARENT ID', parentID)
            nestedDesc = nestedDesc.replace('\n', '<br>').replace('\r', '<br>')

            print(nestedShapeId, nestedShapeHeading, nestedShape, nestedDesc, parentID)
            print('shape nested', nestedShapeList, nestedId)
            if int(nestedShapeId) in nestedId and nestedShapeId != '':
                error = "Shape id already used, please use a different id."
                errorType = "Duplicate shape id"
                return render_template('index.html', value=shape, level4Height=height, heading=shapeName,
                                       shape_list=finallevel10, count=total, flowChartName=fl, lastAxis=lastAxis,
                                       flowChart=flowChartName.upper(), error=error, type=errorType,
                                       canvasID="canvas")
            else:

                for item in finallevel9:
                    if int(item[0]) == int(parentID):
                        uniqueID = item[4]
                        break
                print('flowchartname', flowChartName)
                if flowChartName != '':

                    sql = "INSERT INTO shapeDetails(FlowChartId, ParentId, ShapeId, ShapeHeading, " \
                          "ShapeTypeId, ShapeDesc,  condition1, condition2, condition3, condition4)" \
                          "VALUES((select flowChartId from flowCharts where flowChartName = %s), " \
                          "%s, %s, %s, (select shapeTypeID from shapeType where shapeType = %s), %s, %s, %s, %s, %s)"
                    data = (flowChartName, uniqueID, nestedShapeId, nestedShapeHeading, nestedShape, nestedDesc, condition1, condition2, condition3, condition4)
                    cursor = mydb.cursor()
                    cursor.execute(sql, data)
                    mydb.commit()
                    cursor.close()

                    for item in finallevel9:
                        if item[0] == parentID:
                            uniqueID = item[4]

                    level10DelId = []
                    level10ShapeList = []
                    databaselevel10(uniqueID)
                    ('level 10 after database', level10ShapeList)

                    nestedli = sort(level10ShapeList)
                    finallevel10 = axis(nestedli)
                    nestedTotal = len(finallevel10)
                if nestedTotal > 2:
                    level10Height = 250 * len(finallevel10) + 100
                else:
                    level10Height = 600
            return render_template('index.html', value=shape, heading=shapeName,
                                   shape_list=finallevel10, count=nestedTotal,
                                   level10Height=level10Height, flowChartName=fl, lastAxis=lastAxis,
                                   flowChart=flowChartName.upper(), canvasID="nestedCanvasLevel10")

        if request.form['submit'] == 'Close':
            close = request.form['close']
            print(close)
        # Level 1
        if request.form['submit'] == 'nestedSubWorkFlow':
            parentID = request.form['input_type']
            print('Testing parent id', parentID)
            nestedShapeList = []
            nestedId = []
            # databaseNested(parentID)
            for item in final:
                if int(item[0]) == int(parentID):
                    uniqueID = item[4]
                    break
            # databaseNested(uniqueID)
            sql = """select shapeId, shapeHeading, shapeType.shapeType, shapeDesc, ID, condition1, condition2, condition3, 
                 condition4  from shapeDetails 
               left join shapeType on shapeType.shapeTypeID = shapeDetails.ShapeTypeId left join flowCharts
                on flowCharts.flowChartId = shapeDetails.FlowChartId where flowChartName = %s and ParentId = %s """
            cursor = mydb.cursor()
            # print("ID FROM JS", uniqueID, flowChartName)
            cursor.execute(sql, (flowChartName, uniqueID))
            rows = cursor.fetchall()
            print("from sql", rows)
            cursor.close()

            for item in rows:
                nestedShapeList.append(list(item))
                nestedId.append(item[0])
            print('Nested shape list and id', nestedShapeList, nestedId)
            global leng
            leng = len(nestedId)
            print(leng)

            nestedli = sort(nestedShapeList)
            finalNested = axis(nestedli)
            nestedTotal = len(finalNested)
            print("Nsted totl ", nestedTotal)
            if nestedTotal > 2:
                heightNested = 250 * len(finalNested) + 100
            else:
                heightNested = 600
            print('nested workflow', finalNested)
            if len(nestedShapeList) == 0:
                display = 'HE:LL::OOO'
                return render_template('index.html', value=shape, heading=shapeName,
                                       count=nestedTotal, heightNested = heightNested,
                                       displayNestedCanvas = display, flowChartName=fl, lastAxis=lastAxis,
                                       flowChart=flowChartName.upper(), canvasID="nestedCanvas")
            else:
                return render_template('index.html', value=shape, heading=shapeName, shape_list=finalNested,
                                       count=nestedTotal,
                                       heightNested=heightNested, flowChartName=fl, lastAxis=lastAxis,
                                       flowChart=flowChartName.upper(), canvasID="nestedCanvas")
        #     Level 2
        if request.form['submit'] == 'nestedSubWorkFlowLevel2':
            parentID = request.form['input_level_2']
            print('level 2 Testing parent id', parentID)
            subNestedShapeList = []
            subNestedId = []
            # databaseNested(parentID)
            for item in finalNested:
                if int(item[0]) == int(parentID):
                    uniqueID = item[4]
                    break
            # databaseNested(uniqueID)
            sql = """select shapeId, shapeHeading, shapeType.shapeType, shapeDesc, ID, condition1, condition2, condition3, 
               condition4  from shapeDetails 
               left join shapeType on shapeType.shapeTypeID = shapeDetails.ShapeTypeId left join flowCharts
                on flowCharts.flowChartId = shapeDetails.FlowChartId where flowChartName = %s and ParentId = %s """
            cursor = mydb.cursor()
            # print("ID FROM JS", uniqueID, flowChartName)
            cursor.execute(sql, (flowChartName, uniqueID))
            rows = cursor.fetchall()
            print("from sql", rows)
            cursor.close()

            for item in rows:
                subNestedShapeList.append(list(item))
                subNestedId.append(item[0])
            print('Nested shape list and id', subNestedShapeList, subNestedId)
            nestedli = sort(subNestedShapeList)
            finalSubNested = axis(nestedli)
            nestedTotal = len(finalSubNested)
            if nestedTotal > 2:
                heightSubNested = 250 * len(finalSubNested) + 100
            else:
                heightSubNested = 600
            if len(subNestedShapeList) == 0:
                display = 'HE:LL::OOO'
                return render_template('index.html', value=shape, heading=shapeName,
                                       count=nestedTotal, heightSubNested=heightSubNested,
                                       displayNestedCanvasLevel2=display, flowChartName=fl, lastAxis=lastAxis,
                                       flowChart=flowChartName.upper(), canvasID="nestedCanvasLevel2",
                                       displayCanvas='displayCanvas')
            else:
                return render_template('index.html', value=shape, heading=shapeName, shape_list=finalSubNested,
                                       count=nestedTotal,
                                       heightSubNested=heightSubNested, flowChartName=fl, lastAxis=lastAxis,
                                       flowChart=flowChartName.upper(), canvasID="nestedCanvasLevel2",
                                       displayCanvas='displayCanvas')
        #     Level 3
        if request.form['submit'] == 'nestedSubWorkFlowLevel3':
            parentID = request.form['level_3_input']
            print('Testing parent id level 3', parentID)
            level4ShapeList = []
            level4DelId = []
            # databaseNested(parentID)
            for item in finalSubNested:
                if int(item[0]) == int(parentID):
                    uniqueID = item[4]
                    print("level 3 ", uniqueID)
                    break
            # databaseNested(uniqueID)
            sql = """select shapeId, shapeHeading, shapeType.shapeType, shapeDesc, ID, condition1, condition2, condition3, 
                condition4  from shapeDetails 
               left join shapeType on shapeType.shapeTypeID = shapeDetails.ShapeTypeId left join flowCharts
                on flowCharts.flowChartId = shapeDetails.FlowChartId where flowChartName = %s and ParentId = %s """
            cursor = mydb.cursor()
            # print("ID FROM JS", uniqueID, flowChartName)
            cursor.execute(sql, (flowChartName, uniqueID))
            rows = cursor.fetchall()
            print("from sql", rows)
            cursor.close()

            for item in rows:
                level4ShapeList.append(list(item))
                level4DelId.append(item[0])
            print('Nested shape level 3 list and id', level4ShapeList, level4DelId)
            nestedli = sort(level4ShapeList)
            finallevel4 = axis(nestedli)
            nestedTotal = len(finallevel4)
            if nestedTotal > 2:
                level4Height = 250 * len(finallevel4) + 100
            else:
                level4Height = 600


            print('nested workflow', finallevel4)
            if len(level4ShapeList) == 0:
                display = 'HE:LL::OOO'
                return render_template('index.html', value=shape, heading=shapeName,
                                       count=nestedTotal, level4Height=level4Height,
                                       displayNestedCanvasLevel3=display, flowChartName=fl, lastAxis=lastAxis,
                                       flowChart=flowChartName.upper(), canvasID="nestedCanvasLevel4",
                                       displayCanvas='displayCanvas')
            else:
                return render_template('index.html', value=shape, heading=shapeName, shape_list=finallevel4,
                                       count=nestedTotal,
                                       level4Height=level4Height, flowChartName=fl, lastAxis=lastAxis,
                                       flowChart=flowChartName.upper(), canvasID="nestedCanvasLevel4",
                                       displayCanvas='displayCanvas')
                #     Level 4
        if request.form['submit'] == 'nestedSubWorkFlowLevel4':
            parentID = request.form['level_4_input']
            print('Testing parent id level 4', parentID)
            level5ShapeList = []
            level5DelId = []
            # databaseNested(parentID)
            for item in finallevel4:
                if int(item[0]) == int(parentID):
                    uniqueID = item[4]
                    break
            # databaseNested(uniqueID)
            sql = """select shapeId, shapeHeading, shapeType.shapeType, shapeDesc, ID, condition1, condition2, condition3, 
               condition4 from shapeDetails 
               left join shapeType on shapeType.shapeTypeID = shapeDetails.ShapeTypeId left join flowCharts
                on flowCharts.flowChartId = shapeDetails.FlowChartId where flowChartName = %s and ParentId = %s """
            cursor = mydb.cursor()
            # print("ID FROM JS", uniqueID, flowChartName)
            cursor.execute(sql, (flowChartName, uniqueID))
            rows = cursor.fetchall()
            print("from sql", rows)
            cursor.close()

            for item in rows:
                level5ShapeList.append(list(item))
                level5DelId.append(item[0])
            print('Nested shape list and id', level5ShapeList, level5DelId)
            nestedli = sort(level5ShapeList)
            finallevel5 = axis(nestedli)
            nestedTotal = len(finallevel5)
            if nestedTotal > 2:
                level5Height = 250 * len(finallevel5) + 100
            else:
                level5Height = 600

            print('nested workflow', finallevel5)
            if len(level5ShapeList) == 0:
                display = 'HE:LL::OOO'
                return render_template('index.html', value=shape, heading=shapeName,
                                       count=nestedTotal, level5Height=level5Height,
                                       displayNestedCanvasLevel4=display, flowChartName=fl, lastAxis=lastAxis,
                                       flowChart=flowChartName.upper(), canvasID="nestedCanvasLevel5",
                                       displayCanvas='displayCanvas')
            else:
                return render_template('index.html', value=shape, heading=shapeName, shape_list=finallevel5,
                                       count=nestedTotal,
                                       level5Height=level5Height, flowChartName=fl, lastAxis=lastAxis,
                                       flowChart=flowChartName.upper(), canvasID="nestedCanvasLevel5",
                                       displayCanvas='displayCanvas')
                #     Level 6
        if request.form['submit'] == 'nestedSubWorkFlowLevel5':
            parentID = request.form['level_5_input']
            print('Testing parent id level 5', parentID)
            level6ShapeList = []
            level6DelId = []
            # databaseNested(parentID)
            for item in finallevel5:
                if int(item[0]) == int(parentID):
                    uniqueID = item[4]
                    break
            # databaseNested(uniqueID)
            sql = """select shapeId, shapeHeading, shapeType.shapeType, shapeDesc, ID, condition1, condition2, condition3, 
                 condition4  from shapeDetails 
                left join shapeType on shapeType.shapeTypeID = shapeDetails.ShapeTypeId left join flowCharts
                 on flowCharts.flowChartId = shapeDetails.FlowChartId where flowChartName = %s and ParentId = %s """
            cursor = mydb.cursor()
            # print("ID FROM JS", uniqueID, flowChartName)
            cursor.execute(sql, (flowChartName, uniqueID))
            rows = cursor.fetchall()
            print("from sql", rows)
            cursor.close()

            for item in rows:
                level6ShapeList.append(list(item))
                level6DelId.append(item[0])
            print('Nested shape list and id', level6ShapeList, level6DelId)
            nestedli = sort(level6ShapeList)
            finallevel6 = axis(nestedli)
            nestedTotal = len(finallevel6)
            if nestedTotal > 2:
                level6Height = 250 * len(finallevel6) + 100
            else:
                level6Height = 600

            print('nested workflow', finallevel6)
            if len(level6ShapeList) == 0:
                display = 'HE:LL::OOO'
                return render_template('index.html', value=shape, heading=shapeName,
                                       count=nestedTotal, level6Height=level6Height,
                                       displayNestedCanvasLevel5=display, flowChartName=fl, lastAxis=lastAxis,
                                       flowChart=flowChartName.upper(), canvasID="nestedCanvasLevel6",
                                       displayCanvas='displayCanvas')
            else:
                return render_template('index.html', value=shape, heading=shapeName, shape_list=finallevel6,
                                       count=nestedTotal,
                                       level6Height=level6Height, flowChartName=fl, lastAxis=lastAxis,
                                       flowChart=flowChartName.upper(), canvasID="nestedCanvasLevel6",
                                       displayCanvas='displayCanvas')
                #     Level 7
        if request.form['submit'] == 'nestedSubWorkFlowLevel6':
            parentID = request.form['level_6_input']
            print('Testing parent id level 6', parentID)
            level7ShapeList = []
            level7DelId = []
            # databaseNested(parentID)
            for item in finallevel6:
                if int(item[0]) == int(parentID):
                    uniqueID = item[4]
                    break
            # databaseNested(uniqueID)
            sql = """select shapeId, shapeHeading, shapeType.shapeType, shapeDesc, ID, condition1, condition2, condition3, 
                   condition4  from shapeDetails 
                   left join shapeType on shapeType.shapeTypeID = shapeDetails.ShapeTypeId left join flowCharts
                    on flowCharts.flowChartId = shapeDetails.FlowChartId where flowChartName=%s and ParentId=%s"""
            cursor = mydb.cursor()
            # print("ID FROM JS", uniqueID, flowChartName)
            cursor.execute(sql, (flowChartName, uniqueID))
            rows = cursor.fetchall()
            print("from sql", rows)
            cursor.close()

            for item in rows:
                level7ShapeList.append(list(item))
                level7DelId.append(item[0])
            print('Nested shape list and id', level7ShapeList, level7DelId)
            nestedli = sort(level7ShapeList)
            finallevel7 = axis(nestedli)
            nestedTotal = len(finallevel7)
            if nestedTotal > 2:
                level7Height = 250 * len(finallevel7) + 100
            else:
                level7Height = 600

            print('nested workflow', finallevel7)
            if len(level7ShapeList) == 0:
                display = 'HE:LL::OOO'
                return render_template('index.html', value=shape, heading=shapeName,
                                       count=nestedTotal, level7Height=level7Height,
                                       displayNestedCanvasLevel6=display, flowChartName=fl, lastAxis=lastAxis,
                                       flowChart=flowChartName.upper(), canvasID="nestedCanvasLevel7",
                                       displayCanvas='displayCanvas')
            else:
                return render_template('index.html', value=shape, heading=shapeName, shape_list=finallevel7,
                                       count=nestedTotal,
                                       level7Height=level7Height, flowChartName=fl, lastAxis=lastAxis,
                                       flowChart=flowChartName.upper(), canvasID="nestedCanvasLevel7",
                                       displayCanvas='displayCanvas')
        #     Level 8
        if request.form['submit'] == 'nestedSubWorkFlowLevel7':
            parentID = request.form['level_7_input']
            print('Testing parent id level 7', parentID)
            level8ShapeList = []
            level8DelId = []
            # databaseNested(parentID)
            for item in finallevel7:
                if int(item[0]) == int(parentID):
                    uniqueID = item[4]
                    break
            # databaseNested(uniqueID)
            sql = """select shapeId, shapeHeading, shapeType.shapeType, shapeDesc, ID, condition1, condition2, condition3, 
                   condition4  from shapeDetails 
                   left join shapeType on shapeType.shapeTypeID = shapeDetails.ShapeTypeId left join flowCharts
                    on flowCharts.flowChartId = shapeDetails.FlowChartId where flowChartName=%s and ParentId=%s"""
            cursor = mydb.cursor()
            # print("ID FROM JS", uniqueID, flowChartName)
            cursor.execute(sql, (flowChartName, uniqueID))
            rows = cursor.fetchall()
            print("from sql", rows)
            cursor.close()

            for item in rows:
                level8ShapeList.append(list(item))
                level8DelId.append(item[0])
            print('Nested shape list and id 8', level8ShapeList, level8DelId)
            nestedli = sort(level8ShapeList)
            finallevel8 = axis(nestedli)
            nestedTotal = len(finallevel8)
            if nestedTotal > 2:
                level8Height = 250 * len(finallevel8) + 100
            else:
                level8Height = 600

            print('nested workflow', finallevel8)
            if len(level8ShapeList) == 0:
                display = 'HE:LL::OOO'
                return render_template('index.html', value=shape, heading=shapeName,
                                       count=nestedTotal, level8Height=level8Height,
                                       displayNestedCanvasLevel7=display, flowChartName=fl, lastAxis=lastAxis,
                                       flowChart=flowChartName.upper(), canvasID="nestedCanvasLevel8",
                                       displayCanvas='displayCanvas')
            else:
                return render_template('index.html', value=shape, heading=shapeName, shape_list=finallevel8,
                                       count=nestedTotal,
                                       level8Height=level8Height, flowChartName=fl, lastAxis=lastAxis,
                                       flowChart=flowChartName.upper(), canvasID="nestedCanvasLevel8",
                                       displayCanvas='displayCanvas')
                #     Level 9
        if request.form['submit'] == 'nestedSubWorkFlowLevel8':
            parentID = request.form['level_8_input']
            print('Testing parent id level 8', parentID)
            level9ShapeList = []
            level9DelId = []
            # databaseNested(parentID)
            for item in finallevel8:
                if int(item[0]) == int(parentID):
                    uniqueID = item[4]
                    break
            # databaseNested(uniqueID)
            sql = """select shapeId, shapeHeading, shapeType.shapeType, shapeDesc, ID, condition1, condition2, condition3, 
                      condition4  from shapeDetails 
                      left join shapeType on shapeType.shapeTypeID = shapeDetails.ShapeTypeId left join flowCharts
                       on flowCharts.flowChartId = shapeDetails.FlowChartId where flowChartName=%s and ParentId=%s"""
            cursor = mydb.cursor()
            # print("ID FROM JS", uniqueID, flowChartName)
            cursor.execute(sql, (flowChartName, uniqueID))
            rows = cursor.fetchall()
            print("from sql", rows)
            cursor.close()

            for item in rows:
                level9ShapeList.append(list(item))
                level9DelId.append(item[0])
            print('Nested shape list and id level 9', level9ShapeList, level9DelId)
            nestedli = sort(level9ShapeList)
            finallevel9 = axis(nestedli)
            nestedTotal = len(finallevel9)
            if nestedTotal > 2:
                level9Height = 250 * len(finallevel9) + 100
            else:
                level9Height = 600

            print('nested workflow 9', finallevel9)
            if len(level9ShapeList) == 0:
                display = 'HE:LL::OOO'
                return render_template('index.html', value=shape, heading=shapeName,
                                       count=nestedTotal, level9Height=level9Height,
                                       displayNestedCanvasLevel8=display, flowChartName=fl, lastAxis=lastAxis,
                                       flowChart=flowChartName.upper(), canvasID="nestedCanvasLevel9",
                                       displayCanvas='displayCanvas')
            else:
                return render_template('index.html', value=shape, heading=shapeName, shape_list=finallevel9,
                                       count=nestedTotal,
                                       level9Height=level9Height, flowChartName=fl, lastAxis=lastAxis,
                                       flowChart=flowChartName.upper(), canvasID="nestedCanvasLevel9",
                                       displayCanvas='displayCanvas')
            #     Level 10
        if request.form['submit'] == 'nestedSubWorkFlowLevel8':
            parentID = request.form['level_9_input']
            print('Testing parent id level 9', parentID)
            level10ShapeList = []
            level10DelId = []
            # databaseNested(parentID)
            for item in finallevel9:
                if int(item[0]) == int(parentID):
                    uniqueID = item[4]
                    break
            # databaseNested(uniqueID)
            sql = """select shapeId, shapeHeading, shapeType.shapeType, shapeDesc, ID, condition1, condition2, condition3, 
                        condition4 from shapeDetails 
                      left join shapeType on shapeType.shapeTypeID = shapeDetails.ShapeTypeId left join flowCharts
                       on flowCharts.flowChartId = shapeDetails.FlowChartId where flowChartName=%s and ParentId=%s"""
            cursor = mydb.cursor()
            # print("ID FROM JS", uniqueID, flowChartName)
            cursor.execute(sql, (flowChartName, uniqueID))
            rows = cursor.fetchall()
            print("from sql", rows)
            cursor.close()

            for item in rows:
                level10ShapeList.append(list(item))
                level10DelId.append(item[0])
            print('Nested shape list and id level 9', level10ShapeList, level10DelId)
            nestedli = sort(level10ShapeList)
            finallevel10 = axis(nestedli)
            nestedTotal = len(finallevel10)
            if nestedTotal > 2:
                level10Height = 250 * len(finallevel10) + 100
            else:
                level10Height = 600

            print('nested workflow 9', finallevel10)
            if len(level10ShapeList) == 0:
                display = 'HE:LL::OOO'
                return render_template('index.html', value=shape, heading=shapeName,
                                       count=nestedTotal, level10Height=level10Height,
                                       displayNestedCanvasLevel9=display, flowChartName=fl, lastAxis=lastAxis,
                                       flowChart=flowChartName.upper(), canvasID="nestedCanvasLevel10",
                                       displayCanvas='displayCanvas')
            else:
                return render_template('index.html', value=shape, heading=shapeName, shape_list=finallevel10,
                                       count=nestedTotal,
                                       level10Height=level10Height, flowChartName=fl, lastAxis=lastAxis,
                                       flowChart=flowChartName.upper(), canvasID="nestedCanvasLevel10",
                                       displayCanvas='displayCanvas')
        if request.form['submit'] == 'retrieve':
            flowChartName = request.form['nn']
            print('flo', flowChartName)
            shape_list = []
            id = []
            height = 600
            database()
        if request.form['submit'] == 'submit_flowChartName':
            flowChartName = request.form['flowName']
            print('From add', flowChartName)
            shape_list = []
            id = []
            if flowChartName not in fl:
                print(flowChartName)
                # sql = """Insert into shapedesc(flowChartName, shapeId, shapeName, shapeType, shapeDesc) values(%s, %s, %s, %s, %s)"""
                sql = """INSERT INTO flowCharts(flowChartName) values (%s)"""
                cursor = mydb.cursor()
                #displayNestedCanvas cursor.execute(sql, (flowChartName, None, None, None, None,))
                cursor.execute(sql, (flowChartName, ))

                mydb.commit()
                cursor.close()
                # conn.close()
                flowChart()
            else:
                error = "Flow Chart Name already used"
                errorType = "Duplicate FlowChart Name"
                return render_template('index.html', value=shape, height=height, heading=shapeName, shape_list=final,
                                       count=total, error=error, type=errorType, flowChartName = fl, lastAxis = lastAxis, flowChart = flowChartName.upper(), canvasID = "canvas")
        print('second test', shape_list)
        li = sort(shape_list)
        final = axis(li)
        print('FINAL LIST', final)
        if lastShapeId != []:
            sID = lastShapeId[0]
            print('last Shape Id', sID)
            for item in final:
                print("tess",item)
                if int(item[0]) == int(sID):
                    lastAxis = item[5]
                    print('last axis', lastAxis)
                    break


        total = len(shape_list)
        if total > 2:
            height = 250 * len(shape_list) + 100
        else:
            height = 600

    return render_template('index.html', value = shape, heading = shapeName,  shape_list = final, count = total, height = height, flowChartName = fl, lastAxis = lastAxis, flowChart = flowChartName.upper(), canvasID = "canvas")

def sort(shape_list):
        shape_list.sort(key = lambda x: x[0])

        return shape_list


def database():
    sql = """select shapeId, shapeHeading, shapeType.shapeType, shapeDesc, ID, condition1, condition2, condition3, 
    condition4  from shapeDetails 
    left join shapeType on shapeType.shapeTypeID = shapeDetails.ShapeTypeId left join flowCharts
     on flowCharts.flowChartId = shapeDetails.FlowChartId where flowChartName = %s and ParentId is null"""
    print("testing", flowChartName)
    cursor = mydb.cursor()
    cursor.execute(sql, (flowChartName,))
    rows = cursor.fetchall()
    print("from sql", rows)
    cursor.close()
    for item in rows:
        shape_list.append(list(item))
        id.append(item[0])
    print(id)
    print('testing', shape_list)
    return


def databaseNested(parentId):
    print("OOKAY DELETED")
    # for item in final:
    #     if int(item[0]) == int(parentId):
    #         uniqueId = item[4]
    #         print(uniqueId)
    #         break
    sql = """select shapeId, shapeHeading, shapeType.shapeType, shapeDesc, ID, condition1, condition2, condition3, 
                condition4  from shapeDetails 
                left join shapeType on shapeType.shapeTypeID = shapeDetails.ShapeTypeId left join flowCharts
                 on flowCharts.flowChartId = shapeDetails.FlowChartId where flowChartName = %s and ParentId = %s"""
    cursor = mydb.cursor()
    # print("ID FROM JS", uniqueID, flowChartName)

    cursor.execute(sql, (flowChartName, parentId, ))
    rows = cursor.fetchall()
    print("from sql", rows)
    cursor.close()
    # nestedShapeList = []
    # nestedId = []
    for item in rows:
        nestedShapeList.append(list(item))
        nestedId.append(item[0])
    print('Nesteddddd', nestedShapeList, nestedId)
    global leng
    leng = len(nestedId)
    print(leng)

    return

def databaselevel3(id):
    print("OOKAY DELETED")
    # for item in finalNested:
    #     if int(item[0]) == int(id):
    #         uniqueId = item[4]
    #         print(uniqueId)
    #         break
    sql = """select shapeId, shapeHeading, shapeType.shapeType, shapeDesc, ID, condition1, condition2, condition3, 
                condition4  from shapeDetails 
                left join shapeType on shapeType.shapeTypeID = shapeDetails.ShapeTypeId left join flowCharts
                 on flowCharts.flowChartId = shapeDetails.FlowChartId where flowChartName = %s and ParentId = %s"""
    cursor = mydb.cursor()
    print("ID FROM JS", id, flowChartName)

    cursor.execute(sql, (flowChartName, id, ))
    rows = cursor.fetchall()
    print("from sql", rows)
    cursor.close()

    for item in rows:
        subNestedShapeList.append(list(item))
        subNestedId.append(item[0])
    print('Level 3', subNestedShapeList, subNestedDelId)

    return


def databaselevel4(id):
    print("OOKAY DELETED")
    # for item in finalSubNested:
    #     if int(item[0]) == int(id):
    #         uniqueId = item[4]
    #         print(uniqueId)
    #         break
    sql = """select shapeId, shapeHeading, shapeType.shapeType, shapeDesc, ID, condition1, condition2, condition3, 
                condition4  from shapeDetails 
                left join shapeType on shapeType.shapeTypeID = shapeDetails.ShapeTypeId left join flowCharts
                 on flowCharts.flowChartId = shapeDetails.FlowChartId where flowChartName = %s and ParentId = %s"""
    cursor = mydb.cursor()
    print("ID FROM JS", uniqueID, flowChartName)

    cursor.execute(sql, (flowChartName, id, ))
    rows = cursor.fetchall()
    print("from sql", rows)
    cursor.close()

    for item in rows:
        level4ShapeList.append(list(item))
        level4DelId.append(item[0])
    print('Level 4', level4ShapeList, level4DelId)

    return


def databaselevel5(id):
    print("OOKAY DELETED")
    # for item in finalLevel4:
    #     if int(item[0]) == int(id):
    #         uniqueId = item[4]
    #         print(uniqueId)
    #         break
    sql = """select shapeId, shapeHeading, shapeType.shapeType, shapeDesc, ID, condition1, condition2, condition3, 
                condition4  from shapeDetails 
                left join shapeType on shapeType.shapeTypeID = shapeDetails.ShapeTypeId left join flowCharts
                 on flowCharts.flowChartId = shapeDetails.FlowChartId where flowChartName = %s and ParentId = %s"""
    cursor = mydb.cursor()
    print("ID FROM JS", uniqueID, flowChartName)

    cursor.execute(sql, (flowChartName, id, ))
    rows = cursor.fetchall()
    print("from sql", rows)
    cursor.close()

    for item in rows:
        level5ShapeList.append(list(item))
        level5DelId.append(item[0])
    print('Level 5', level5ShapeList, level5DelId)

    return

def databaselevel6(id):
    print("OOKAY DELETED")
    # for item in finalLevel5:
    #     if int(item[0]) == int(id):
    #         uniqueId = item[4]
    #         print(uniqueId)
    #         break
    sql = """select shapeId, shapeHeading, shapeType.shapeType, shapeDesc, ID, condition1, condition2, condition3, 
                condition4  from shapeDetails 
                left join shapeType on shapeType.shapeTypeID = shapeDetails.ShapeTypeId left join flowCharts
                 on flowCharts.flowChartId = shapeDetails.FlowChartId where flowChartName = %s and ParentId = %s"""
    cursor = mydb.cursor()
    print("ID FROM JS", uniqueID, flowChartName)

    cursor.execute(sql, (flowChartName, id, ))
    rows = cursor.fetchall()
    print("from sql", rows)
    cursor.close()

    for item in rows:
        level6ShapeList.append(list(item))
        level6DelId.append(item[0])
    print('Level 6', level6ShapeList, level6DelId)

    return level6ShapeList


def databaselevel7(id):
    print("OOKAY DELETED")
    # for item in finalLevel6:
    #     if int(item[0]) == int(id):
    #         uniqueId = item[4]
    #         print(uniqueId)
    #         break
    sql = """select shapeId, shapeHeading, shapeType.shapeType, shapeDesc, ID, condition1, condition2, condition3, 
                condition4  from shapeDetails 
                left join shapeType on shapeType.shapeTypeID = shapeDetails.ShapeTypeId left join flowCharts
                 on flowCharts.flowChartId = shapeDetails.FlowChartId where flowChartName = %s and ParentId = %s"""
    cursor = mydb.cursor()
    print("ID FROM JS", uniqueID, flowChartName)

    cursor.execute(sql, (flowChartName, id, ))
    rows = cursor.fetchall()
    print("from sql", rows)
    cursor.close()

    for item in rows:
        level7ShapeList.append(list(item))
        level7DelId.append(item[0])
    print('Level 7', level7ShapeList, level7DelId)

    return

def databaselevel8(id):
    # print("OOKAY DELETED")
    # for item in finalLevel7:
    #     if int(item[0]) == int(id):
    #         uniqueId = item[4]
    #         print(uniqueId)
    #         break
    sql = """select shapeId, shapeHeading, shapeType.shapeType, shapeDesc, ID, condition1, condition2, condition3, 
                condition4  from shapeDetails 
                left join shapeType on shapeType.shapeTypeID = shapeDetails.ShapeTypeId left join flowCharts
                 on flowCharts.flowChartId = shapeDetails.FlowChartId where flowChartName = %s and ParentId = %s"""
    cursor = mydb.cursor()
    print("ID FROM JS", uniqueID, flowChartName)

    cursor.execute(sql, (flowChartName, id, ))
    rows = cursor.fetchall()
    print("from sql", rows)
    cursor.close()

    for item in rows:
        level8ShapeList.append(list(item))
        level8DelId.append(item[0])
    print('Level 8', level8ShapeList, level8DelId)

    return


def databaselevel9(id):
    print("OOKAY DELETED")
    # for item in finalLevel8:
    #     if int(item[0]) == int(id):
    #         uniqueId = item[4]
    #         print(uniqueId)
    #         break
    sql = """select shapeId, shapeHeading, shapeType.shapeType, shapeDesc, ID, condition1, condition2, condition3, 
                 condition4  from shapeDetails 
                left join shapeType on shapeType.shapeTypeID = shapeDetails.ShapeTypeId left join flowCharts
                 on flowCharts.flowChartId = shapeDetails.FlowChartId where flowChartName = %s and ParentId = %s"""
    cursor = mydb.cursor()
    print("ID FROM JS", uniqueID, flowChartName)

    cursor.execute(sql, (flowChartName, id, ))
    rows = cursor.fetchall()
    print("from sql", rows)
    cursor.close()

    for item in rows:
        level9ShapeList.append(list(item))
        level9DelId.append(item[0])
    print('Level 9', level9ShapeList, level9DelId)

    return


def databaselevel10(id):
    print("OOKAY DELETED")
    # for item in finalLevel9:
    #     if int(item[0]) == int(id):
    #         uniqueId = item[4]
    #         print(uniqueId)
    #         break
    sql = """select shapeId, shapeHeading, shapeType.shapeType, shapeDesc, ID, condition1, condition2, condition3, 
                 condition4  from shapeDetails 
                left join shapeType on shapeType.shapeTypeID = shapeDetails.ShapeTypeId left join flowCharts
                 on flowCharts.flowChartId = shapeDetails.FlowChartId where flowChartName = %s and ParentId = %s"""
    cursor = mydb.cursor()
    print("ID FROM JS", uniqueID, flowChartName)

    cursor.execute(sql, (flowChartName, id, ))
    rows = cursor.fetchall()
    print("from sql", rows)
    cursor.close()

    for item in rows:
        level10ShapeList.append(list(item))
        level10DelId.append(item[0])
    print('Level 10', level10ShapeList, level10DelId)

    return












@app.route('/getpythondata')
def get_python_data():

    # print('nested IDSS', nestedId)

    # print('length', leng)
    return json.dumps(leng)

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
@app.route('/', methods=['GET', 'POST'])
def modifyShape():
    global shape, shapeName, y, count, total, modShape
    if request.method == 'POST':
        if request.form['submit'] == 'Modify':
            modId = request.form['modId']
            print(modId)
        for item in shape_list:
            if item[4] == modId:
                modShape = item
            break
    print(modShape)
    print(delId, shape_list)
@app.route('/postmethod', methods=['POST'])
def realtimevalue():
    if request.method == "POST":

        id = request.form['data']
        print("from JAVASCRIPT", id)
        databaseNested(id)
    return data



@app.route('/login/', methods=['GET', 'POST'])
def add_user():
    error = None
    if request.method == 'POST':
        if request.form['submit'] == 'signUp':
            user_name = request.form['username']
            firstname = request.form['firstName']
            lastname = request.form['lastName']
            user_email = request.form['email']
            user_password = request.form['password']
            # if user_name and user_email and user_password and request.method == 'POST':
            sql = "INSERT INTO registration(userName, firstName, lastName, emailId, " \
                  "userPassword)" \
                  " VALUES(%s, %s, %s, %s, %s)"
            data = (user_name, firstname, lastname, user_email, user_password)
            try:
                cursor = mydb.cursor()

                cursor.execute(sql, data)
                mydb.commit()
                cursor.close()
            except mysql.connector.Error as err:
                print(err)
                if 'emailId' in str(err):
                    flash('Email Id already used..please use a different emailId')
                else:
                    flash('Username already used please try again with a different username')
        if request.form['submit'] == 'Login':
            user_name = request.form['uname']
            user_password = request.form['psw']
            print(user_name, user_password)
            # sql = """select shapeId, shapeHeading, shapeType.shapeType, shapeDesc, ID, condition1, condition2, condition3,
            #                 condition4  from shapeDetails
            #                left join shapeType on shapeType.shapeTypeID = shapeDetails.ShapeTypeId left join flowCharts
            #                 on flowCharts.flowChartId = shapeDetails.FlowChartId where flowChartName = %s and ParentId = %s """
            sql = """select userPassword from registration where userName = %s;"""

            cursor = mydb.cursor()
            # print("ID FROM JS", uniqueID, flowChartName)
            cursor.execute(sql, (user_name,))
            rows = cursor.fetchall()
            print("from sql", rows)
            cursor.close()
            if len(rows) != 0:
                for item in rows:
                    print('test', item[0], user_password)
                    if item[0] == user_password:
                        print("equal")
                        return redirect(url_for('user_input'))
                    else:
                        error = 'Incorrect Password Please Try Again'
                        flash('Incorrect Password')
                        return render_template('login.html', error=error)

            else:
                error = 'Incorrect UserName Please Try Again'
                flash('Incorrect UserName')
                print('error')
                return render_template('login.html', error=error)

            # data = (user_name)
            # cursor = mydb.cursor()
            #
            # cursor.execute(sql, data)
            # password = cursor.fetchall()
            #
            # mydb.commit()
            # cursor.close()
            # print('password', password)
    return render_template('login.html')








if __name__== '__main__':
     app.secret_key='aheexbeeuqo2999'
     app.config['SESSION_TYPE'] = 'filesystem'
     # sess.init_app(app)
     app.run(debug=True)