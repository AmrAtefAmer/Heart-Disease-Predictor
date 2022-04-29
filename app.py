from flask import Flask,render_template,redirect,session,url_for,flash
from flask_wtf import FlaskForm
from wtforms import StringField,DateField,EmailField,PasswordField,RadioField,SelectField,SubmitField
from wtforms.validators import DataRequired,email_validator
import joblib
app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'


class InfoForm(FlaskForm):
    smoke = RadioField('Do you smoke ?',choices=[('Yes','Yes'),('No','No')],validators=[DataRequired()])
    alcohol = RadioField('Do you drink alcohol ?',choices=[('Yes','Yes'),('No','No')],validators=[DataRequired()])
    stroke = RadioField('Have you ever been told you have a stroke ?',choices=[('Yes','Yes'),('No','No')],validators=[DataRequired()])
    pyhsicalhealth = StringField('In the past 30 days, how many days did you complain about a physical health problem ?',validators=[DataRequired()])
    mentalhealth = StringField('In the past 30 days, how many days did you complain about a mental health problem ?',validators=[DataRequired()])
    diffwalking = RadioField('Do you have a probelm in walking or up stairs ?',choices=[('Yes','Yes'),('No','No')],validators=[DataRequired()])
    sex = RadioField('Your gender ?',choices=[('Male','Male'),('Female','Female')],validators=[DataRequired()]) 
    agecategory = SelectField('Choice your age category :',choices=[('18-24','18-24'),('25-29','25-29'),('30-34','30-34'),('35-39','35-39'),('40-44','40-44'),('45-49','45-49'),('50-54','50-54'),('55-59','55-59'),('60-64','60-64'),('65-69','65-69'),('70-74','70-74'),('75-79','75-79'),('80 or older','80 or older')],validators=[DataRequired()])
    race = SelectField('Choice your race :',choices=[('White','White'),('Black','Black'),('Asian','Asian'),('American Indian/Alaskan Native','American Indian/Alaskan Native'),('Hispanic','Hispanic'),('Other','Other')],validators=[DataRequired()])
    diabetic = RadioField('Have you ever been told you have a diabetic ?',choices=[('Yes','Yes'),('No','No')],validators=[DataRequired()])
    physicalactivity = RadioField('Did you exercise during the past 30 days or not ?',choices=[('Yes','Yes'),('No','No')],validators=[DataRequired()])
    genhealth = SelectField('Choice your gen health :',choices=[('Poor','Poor'),('Fair','Fair'),('Good','Good'),('Very good','Very good'),('Excellent','Excellent')],validators=[DataRequired()])
    sleeptime = StringField('How many hours do you sleep in a day?',validators=[DataRequired()])
    asthma = RadioField('Do you suffer from asthma or not ?',choices=[('Yes','Yes'),('No','No')],validators=[DataRequired()])
    kidneydisease = RadioField('Do you suffer from kidney disease or not ?',choices=[('Yes','Yes'),('No','No')],validators=[DataRequired()])
    skincancer = RadioField('Do you suffer from skin cancer or not ?',choices=[('Yes','Yes'),('No','No')],validators=[DataRequired()])
    bmi = StringField('Enter your bmi ?',validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/',methods=['GET','POST'])
def index():
    form = InfoForm()
    def convert_agecategory():
            if form.agecategory.data == '18-24':
                return 0
            elif form.agecategory.data == '25-29':
                return 1
            elif form.agecategory.data == '30-34':
                return 2
            elif form.agecategory.data == '35-39':
                return 3
            elif form.agecategory.data == '40-44':
                return 4
            elif form.agecategory.data == '45-49':
                return 5
            elif form.agecategory.data == '50-54':
                return 6
            elif form.agecategory.data == '55-59':
                return 7
            elif form.agecategory.data == '60-64':
                return 8
            elif form.agecategory.data == '65-69':
                return 9
            elif form.agecategory.data == '70-74':
                return 10
            elif form.agecategory.data == '75-79':
                return 11
            elif form.agecategory.data == '80 or older':
                return 12
    def convert_genhealth():
        if form.genhealth.data == 'Poor':
            return 0 
        elif form.genhealth.data == 'Fair':
            return 1 
        elif form.genhealth.data == 'Good':
            return 2
        elif form.genhealth.data == 'Very good':
            return 3 
        elif form.genhealth.data == 'Excellent':
            return 4  
    def convert_bmi_to_categories():
        if float(form.bmi.data) < 16:
            return 0
        elif float(form.bmi.data) >= 16 and float(form.bmi.data) < 17:
            return 1
        elif float(form.bmi.data) >= 17 and float(form.bmi.data) < 18.5:
            return 2
        elif float(form.bmi.data) >= 18.5 and float(form.bmi.data) < 25:
            return 3
        elif float(form.bmi.data) >= 25 and float(form.bmi.data) < 30:
            return 4
        elif float(form.bmi.data) >= 30 and float(form.bmi.data) < 35:
            return 5
        elif float(form.bmi.data) >= 35 and float(form.bmi.data) < 40:
            return 6
        elif float(form.bmi.data) >= 40:
            return 7
        
    if form.validate_on_submit():
        if form.pyhsicalhealth.data.isnumeric()==False or int(form.pyhsicalhealth.data) > 30 or int(form.pyhsicalhealth.data) < 0:
            flash('Physical Health values must contain only numbers from 0 to 30')
            return redirect(url_for('index'))
        
        if form.mentalhealth.data.isnumeric()==False or int(form.mentalhealth.data) > 30 or int(form.mentalhealth.data) < 0:
            flash('Mental Health values must contain only numbers from 0 to 30')
            return redirect(url_for('index'))
        
        if form.sleeptime.data.isnumeric()==False or int(form.sleeptime.data) > 24 or int(form.sleeptime.data) < 0:
            flash('Sleep Time values must contain only numbers from 0 to 24')
            return redirect(url_for('index'))

        if form.bmi.data.isnumeric()==False:
            flash('BMI values must contain only numbers')
            return redirect(url_for('index'))
        
        data = []
        data.append(form.bmi.data)
        data.append(form.pyhsicalhealth.data)
        data.append(form.mentalhealth.data)
        data.append(convert_agecategory())
        data.append(convert_genhealth())
        data.append(form.sleeptime.data)
        data.append(convert_bmi_to_categories())
        data.append(form.smoke.data=='Yes')
        data.append(form.alcohol.data == 'Yes')
        data.append(form.stroke.data == 'Yes')
        data.append(form.diffwalking.data == 'Yes')
        data.append(form.sex.data == 'Male')
        data.append(form.race.data == 'Asian')
        data.append(form.race.data == 'Black')
        data.append(form.race.data == 'Hispanic')
        data.append(form.race.data == 'Other')
        data.append(form.race.data == 'White')
        data.append(form.diabetic.data == 'Yes')
        data.append(form.physicalactivity.data == 'Yes')
        data.append(form.asthma.data == 'Yes')
        data.append(form.kidneydisease.data == 'Yes')
        data.append(form.skincancer.data =='Yes')
        scaler = joblib.load("models/scaler.pkl")
        data_scaled = scaler.transform([data])
        model = joblib.load("models/LogisticRegression.pkl")
        prediction = model.predict(data_scaled)
        return render_template('thankyou.html', prediction=prediction)
    return render_template('home.html',form=form)

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

if __name__ == "__main__":
    app.run(debug=False)