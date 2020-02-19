from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length



class AddWorkFlow(FlaskForm):
    work_flow_name = StringField('Work Flow Name', validators=[DataRequired(), Length(min=6, max=100)])
    submit = SubmitField('Create')


class DelWorkFlow(FlaskForm):
    global name

    delete = SubmitField('Delete Work FLow')


class RetWorkFlow(FlaskForm):
    select = SelectField('Select Work Flow', validators=[DataRequired()], choices=[])
    submit = SubmitField('Retrieve')

class ShapeDetails(FlaskForm):
    shapeId = IntegerField('Shape Id', validators=[DataRequired()])
    shapeType = SelectField('Select Shape Type', validators=[DataRequired()], choices=[('draw_circle', 'Circle'),
                                                                                       ('draw_diamond', 'Diamond'),
                                                                                       ('draw_oval', 'Oval'),
                                                                                       ('draw_rectangle', 'Rectangle'),
                                                                                       ('draw_square', 'Square')])
    shapeHeading = StringField('Shape Heading', validators=[DataRequired(), Length(min=4, max=50)])
    shapeDescription = TextAreaField('Shape Description', validators=[DataRequired(), Length(max=5000)])




