from flask import Flask, render_template, request, session, redirect, url_for, flash
from database import db
import mysql.connector
from init import AddWorkFlow, DelWorkFlow, RetWorkFlow
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def add_work_flow():
    form = AddWorkFlow()
    if form.validate_on_submit():
        session['work_flow_name'] = form.work_flow_name.data

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
            flash('WorkFlow already present!! Try creating with a different name')

        return redirect(url_for('delete_work_flow', name=session['work_flow_name']))
    return render_template('index.html', form=form)


@app.route('/workFlow/<name>', methods=['GET', 'POST'])
def delete_work_flow(name):
    form = DelWorkFlow()
    if form.validate_on_submit():
        cursor = db.cursor()
        sql = """delete from work_flow where work_flow_name = %s"""
        cursor.execute(sql, session['work_flow_name'])
        db.commit()
        cursor.close()
        return redirect(url_for('add_work_flow'))

    return render_template('workflow.html', form=form)

@app.route('/', methods=['GET', 'POST'])
def retrieve_work_flow():
    form = RetWorkFlow()
    work_flow_list = database()

    form.select.choices = [(a, a) for a in work_flow_list]

    if form.validate_on_submit():
        session['work_flow_name'] = form.select.data
        return redirect(url_for('delete_work_flow', name=session['work_flow_name']))

    return render_template('index.html', form=form)



def database():
    work_flow_list = []
    cursor = db.cursor()
    cursor.execute("select work_flow_name from work_flow;")
    rows = cursor.fetchall()
    if rows != '':
        for items in rows:
            for names in items:
                work_flow_list.append(names)

    print(work_flow_list)
    db.commit()
    cursor.close()
    return work_flow_list


if __name__ == '__main__':
    app.secret_key = 'aheexbeeuqo299ee29'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
