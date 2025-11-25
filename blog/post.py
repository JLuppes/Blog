from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, DemoData
from datetime import datetime, timezone
from flask_wtf import FlaskForm
from wtforms.validators import Length
from wtforms.fields import *

blog = Blueprint('blog', __name__)


class DemoForm(FlaskForm):
    dataId = HiddenField()
    demoText = StringField(
        'Demo Text', description="This is a text field", validators=[Length(0, 100)])
    demoNumber = IntegerField(
        'Demo Number', description='This is a number field')
    demoBool = BooleanField(
        'Demo Boolean', description='This is a boolean field')
    submit = SubmitField()


@blog.route('/demo')
def demoHome():
    return render_template('demo.html.jinja')


@blog.route('/demo/admin')
def admin():

    allData = DemoData.query.all()

    titles = [('id', '#'), ('demoText', 'Text'), ('demoNumber', 'Number'), ('demoBool',
                                                                            'Boolean'), ('created', 'Created'), ('updated', 'Updated'), ('deleted', 'Deleted')]

    data = []
    for thisData in allData:
        data.append({'id': thisData.id, 'demoText': thisData.demoText, 'demoNumber': thisData.demoNumber,
                    'demoBool': thisData.demoBool, 'created': thisData.created, 'updated': thisData.updated, 'deleted': thisData.deleted})
    return render_template('demoPages/admin.html.jinja', DemoData=DemoData, data=data, titles=titles)


@blog.route('/demo/create', methods=['GET', 'POST'])
def create():
    form = DemoForm()
    if form.validate_on_submit():
        flash('Form validated!')
        formDemoText = request.form.get("demoText", '').strip()
        formDemoNumber = request.form.get("demoNumber", '').strip()
        formDemoBool = request.form.get("demoBool", '') == "y"

        try:
            newDemoData = DemoData(
                demoText=formDemoText,
                demoNumber=formDemoNumber,
                demoBool=formDemoBool
            )
            db.session.add(newDemoData)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            errorMsg = f"Error during database operation: {str(e)}"
            return render_template('demoPages/create/createForm.html.jinja', error=errorMsg)

        freshDemoData = DemoData.query.filter(
            DemoData.demoText == formDemoText, DemoData.demoNumber == formDemoNumber, DemoData.demoBool == formDemoBool).first()

        return render_template('demoPages/create/createSuccess.html.jinja', demoData=freshDemoData)

    return render_template('demoPages/create/createForm.html.jinja', form=form)


@blog.route('/demo/update', methods=['GET', 'POST'])
def update():
    form = DemoForm()

    dataId = request.args.get("dataId")

    if not dataId:
        errorMsg = "No data id provided!"
        return render_template("demo.html.jinja", error=errorMsg)

    dataToEdit = DemoData.query.filter_by(id=dataId).first()

    if not dataToEdit:
        errorMsg = f"No data found with id = {dataId}"
        return render_template("demopages/admin.html.jinja", error=errorMsg)

    if form.validate_on_submit():

        try:
            dataToEdit.demoText = form.demoText.data
            dataToEdit.demoNumber = form.demoNumber.data
            dataToEdit.demoBool = form.demoBool.data
            dataToEdit.updated = datetime.now(timezone.utc)
            db.session.commit()
            flash(f"Successfully updated data with id: {dataId}")
            return redirect(url_for('demo.admin'))
        except Exception as e:
            db.session.rollback()
            errorMsg = f"Error updating db entry with id = {dataId}. Error = {str(e)}"
            form.dataId.data = dataId
            form.demoText.data = dataToEdit.demoText
            form.demoNumber.data = dataToEdit.demoNumber
            form.demoBool.data = dataToEdit.demoBool
            return render_template('demoPages/update/updateForm.html.jinja', error=errorMsg, form=form)

    form.dataId.data = dataId
    form.demoText.data = dataToEdit.demoText
    form.demoNumber.data = dataToEdit.demoNumber
    form.demoBool.data = dataToEdit.demoBool

    return render_template('demoPages/update/updateForm.html.jinja', form=form)


@blog.route('/demo/delete', methods=['GET', 'POST', 'DELETE'])
def delete():
    if request.method == 'POST' or request.method == 'DELETE':

        dataId = request.form.get("dataId", '').strip()

        if not dataId:
            dataId = request.args.get("dataId", '')
            if not dataId:
                errorMsg = "No data id provided!"
                return render_template("demo.html.jinja", error=errorMsg)

        dataToDelete = DemoData.query.filter_by(id=dataId).first()

        if not dataToDelete:
            errorMsg = f"No data found with id = {dataId}"
            return render_template("demopages/admin.html.jinja", error=errorMsg)

        try:
            oldState = dataToDelete.deleted
            dataToDelete.deleted = not oldState
            db.session.commit()
            flash(
                f"Set 'deleted' for data with id = {dataId} to {dataToDelete.deleted}")
            return redirect(url_for('demo.admin'))
        except Exception as e:
            db.session.rollback()
            errorMsg = f"Error deleting db entry with id = {dataId}"
            return render_template('demoPages/admin.html.jinja', error=errorMsg)

    return render_template('demoPages/admin.html.jinja')
