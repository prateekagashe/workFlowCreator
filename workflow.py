from flask import Flask, render_template, request, session, redirect, url_for, flash
from database import db
import mysql.connector
from init import ShapeDetails


@app.route('/', methods=['GET', 'POST'])
def add_work_flow():
    form = ShapeDetails()
    if form.validate_on_submit():
        shape_id = form.shapeId.data
        shape_type = form.shapeType.data
        shape_heading = form.shapeHeading.data
        shape_description = form.shapeDescription.data
        try:
            sql = """Insert into shape_details(work_flow_name) values(%s)"""
            cursor = db.cursor()
            cursor.execute(sql, (session['work_flow_name'],))
            cursor.execute("select last_insert_id();")
            session['work_flow_id'] = cursor.fetchone()
            db.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print(err)
            flash('WorkFlow already present!! Try creating with a different name')

        return redirect(url_for('delete_work_flow', name=session['work_flow_name']))
    return render_template('index.html', form=form)
