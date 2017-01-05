from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    FloatField, RadioField, SelectField, IntegerField
from wtforms.validators import InputRequired, Required, Length, Email, Regexp, EqualTo, DataRequired
from wtforms import ValidationError
from ..models import User
from flask_table import Table, Col         

class pyOptionHomeForm(FlaskForm):
    optionStyle = SelectField('style', 
        choices=[('European','European'),
                 ('BullSpread','BullSpread'),
                 ('BullSpreadPathN','BullSpreadPathN'),
                 ('DoubleNoTouch','DoubleNoTouch'), 
                 ('OutOfRangeRate','OutOfRangeRate'),
                 ('DownAndOutAlternative','DownAndOutAlternative'),
                 ('ModerateOption','ModerateOption')], validators=[DataRequired()])
    optionType = SelectField('type', 
        choices=[('call','call'), ('put', 'put')], validators=[DataRequired()])
    S0 = FloatField('S0', validators=[InputRequired()])
    K = FloatField('K', validators=[InputRequired()])
    K1 = FloatField('K1', validators=[InputRequired()])
    K2 = FloatField('K2', validators=[InputRequired()])
    T = FloatField('T', validators=[InputRequired()])
    r = FloatField('r', validators=[InputRequired()])
    q = FloatField('q', validators=[InputRequired()])
    sigma = FloatField('sigma', validators=[InputRequired()])
    N = IntegerField('N', validators=[InputRequired()])
    Rp = FloatField('Rp', validators=[InputRequired()])
    
    I = IntegerField('I (MC)', validators=[InputRequired()])
    M = IntegerField('M (MC)', validators=[InputRequired()])
    seedNum = IntegerField('seed (MC)', validators=[InputRequired()])
    
    submit = SubmitField('Calculate')

class pyOptionForm(FlaskForm):
    optionStyle = SelectField('style', 
        choices=[('European','European'),
                 ('BullSpread','BullSpread'),
                 ('BullSpreadPathN','BullSpreadPathN'),
                 ('DoubleNoTouch','DoubleNoTouch'), 
                 ('OutOfRangeRate','OutOfRangeRate'),
                 ('DownAndOutAlternative','DownAndOutAlternative'),
                 ('ModerateOption','ModerateOption')], validators=[DataRequired()])
    optionType = SelectField('type', 
        choices=[('call','call'), ('put', 'put')], validators=[DataRequired()])
    S0 = FloatField('S0', validators=[InputRequired()])
    K = FloatField('K', validators=[InputRequired()])
    K1 = FloatField('K1', validators=[InputRequired()])
    K2 = FloatField('K2', validators=[InputRequired()])
    T = FloatField('T', validators=[InputRequired()])
    r = FloatField('r', validators=[InputRequired()])
    q = FloatField('q', validators=[InputRequired()])
    sigma = FloatField('sigma', validators=[InputRequired()])
    N = IntegerField('N', validators=[InputRequired()])
    Rp = FloatField('Rp', validators=[InputRequired()])
    
    I = IntegerField('I (MC)', validators=[InputRequired()])
    M = IntegerField('M (MC)', validators=[InputRequired()])
    seedNum = IntegerField('seed (MC)', validators=[InputRequired()])
    
    submit = SubmitField('Calculate')    
    
class BsmForm(FlaskForm):
    S0 = FloatField('S0', validators=[InputRequired()])
    K = FloatField('K', validators=[InputRequired()])
    T = FloatField('T', validators=[InputRequired()])
    r = FloatField('r', validators=[InputRequired()])
    q = FloatField('q', validators=[InputRequired()])
    sigma = FloatField('sigma', validators=[InputRequired()])
    optionType = SelectField('type', choices=[('call','call'), ('put', 'put')], validators=[DataRequired()])
    submit = SubmitField('Calculate')

    def validate_S0(self, field):
        if field.data < 0:
            raise ValidationError('S0 > 0')
            
    def validate_K(self, field):
        if field.data < 0:
            raise ValidationError('K > 0')

    def validate_T(self, field):
        if field.data < 0:
            raise ValidationError('T > 0')

    def validate_r(self, field):
        if field.data < 0:
            raise ValidationError('r > 0')

    def validate_q(self, field):
        if field.data < 0:
            raise ValidationError('q > 0')
            
    def validate_sigma(self, field):
        if field.data <= 0:
            raise ValidationError('sigma > 0')

    def validate_optionType(self, field):
        if field.data not in ['call','put']:
            raise ValidationError('option type error')


class BullSpreadForm(FlaskForm):
    S0 = FloatField('S0', validators=[InputRequired()])
    K1 = FloatField('K1', validators=[InputRequired()])
    K2 = FloatField('K2', validators=[InputRequired()])
    T = FloatField('T', validators=[InputRequired()])
    r = FloatField('r', validators=[InputRequired()])
    q = FloatField('q', validators=[InputRequired()])
    sigma = FloatField('sigma', validators=[InputRequired()])
    optionType = SelectField('type', choices=[('call','call'), ('put', 'put')], validators=[DataRequired()])
    submit = SubmitField('Calculate')

    def validate_S0(self, field):
        if field.data < 0:
            raise ValidationError('S0 > 0')
            
    def validate_K1(self, field):
        if field.data < 0:
            raise ValidationError('K1 > 0')

    def validate_K2(self, field):
        if field.data < 0:
            raise ValidationError('K2 > 0')

    def validate_T(self, field):
        if field.data < 0:
            raise ValidationError('T > 0')

    def validate_r(self, field):
        if field.data < 0:
            raise ValidationError('r > 0')
    
    def validate_q(self, field):
        if field.data < 0:
            raise ValidationError('q > 0')

    def validate_sigma(self, field):
        if field.data <= 0:
            raise ValidationError('sigma > 0')

    def validate_optionType(self, field):
        if field.data not in ['call','put']:
            raise ValidationError('option type error')

class OptionMCSForm1(FlaskForm):
    S0 = FloatField('S0', validators=[InputRequired()])
    K1 = FloatField('K1', validators=[InputRequired()])
    K2 = FloatField('K2', validators=[InputRequired()])
    T = FloatField('T', validators=[InputRequired()])
    r = FloatField('r', validators=[InputRequired()])
    q = FloatField('q', validators=[InputRequired()])
    sigma = FloatField('sigma', validators=[InputRequired()])
    N = IntegerField('N', validators=[InputRequired()])
    optionType = SelectField('type', choices=[('call','call'), ('put', 'put')], validators=[DataRequired()])
    optionStyle = SelectField('style', 
        choices=[('BullSpreadPathN','BullSpreadPathN')], validators=[DataRequired()])
    I = IntegerField('I (MC)', validators=[InputRequired()])
    M = IntegerField('M (MC)', validators=[InputRequired()])
    seedNum = IntegerField('seed (MC)', validators=[InputRequired()])
    submit = SubmitField('Calculate')

    def validate_S0(self, field):
        if field.data < 0:
            raise ValidationError('S0 >= 0')
            
    def validate_K1(self, field):
        if field.data < 0:
            raise ValidationError('K1 >= 0')

    def validate_K2(self, field):
        if field.data < 0:
            raise ValidationError('K2 >= 0')

    def validate_T(self, field):
        if field.data <= 0:
            raise ValidationError('T > 0')

    def validate_r(self, field):
        if field.data < 0:
            raise ValidationError('r >= 0')

    def validate_q(self, field):
        if field.data < 0:
            raise ValidationError('q >= 0')
            
    def validate_sigma(self, field):
        if field.data <= 0:
            raise ValidationError('sigma > 0')
            
    def validate_N(self, field):
        if field.data <= 0:
            raise ValidationError('N > 0')
            
    def validate_optionType(self, field):
        if field.data not in ['call','put']:
            raise ValidationError('option type error')
            
    def validate_optionStyle(self, field):
        if field.data not in ['BullSpreadPathN']:
            raise ValidationError('option style error')

    def validate_I(self, field):
        if field.data < 0:
            raise ValidationError('I > 0')

    def validate_M(self, field):
        if field.data <= 0:
            raise ValidationError('M > 0')
            
    def validate_seedNum(self, field):
        if field.data < 0:
            raise ValidationError('seed > 0')

class OptionMCSForm2(FlaskForm):
    S0 = FloatField('S0', validators=[InputRequired()])
    K1 = FloatField('K1', validators=[InputRequired()])
    K2 = FloatField('K2', validators=[InputRequired()])
    T = FloatField('T', validators=[InputRequired()])
    r = FloatField('r', validators=[InputRequired()])
    q = FloatField('q', validators=[InputRequired()])
    sigma = FloatField('sigma', validators=[InputRequired()])
    Rp = FloatField('Rp', validators=[InputRequired()])
    optionType = SelectField('type', choices=[('call','call'), ('put', 'put')], validators=[DataRequired()])
    optionStyle = SelectField('style', 
        choices=[('DoubleNoTouch','DoubleNoTouch'), 
                 ('OutOfRangeRate','OutOfRangeRate')], validators=[DataRequired()])
    I = IntegerField('I (MC)', validators=[InputRequired()])
    M = IntegerField('M (MC)', validators=[InputRequired()])
    seedNum = IntegerField('seed (MC)', validators=[InputRequired()])
    submit = SubmitField('Calculate')

    def validate_S0(self, field):
        if field.data < 0:
            raise ValidationError('S0 >= 0')
            
    def validate_K1(self, field):
        if field.data < 0:
            raise ValidationError('K1 >= 0')

    def validate_K2(self, field):
        if field.data < 0:
            raise ValidationError('K2 >= 0')

    def validate_T(self, field):
        if field.data <= 0:
            raise ValidationError('T > 0')

    def validate_r(self, field):
        if field.data < 0:
            raise ValidationError('r >= 0')

    def validate_q(self, field):
        if field.data < 0:
            raise ValidationError('q >= 0')
            
    def validate_sigma(self, field):
        if field.data <= 0:
            raise ValidationError('sigma > 0')
    
    def validate_Rp(self, field):
        if field.data < 0:
            raise ValidationError('Rp >= 0')
            
    def validate_optionType(self, field):
        if field.data not in ['call','put']:
            raise ValidationError('option type error')
            
    def validate_optionStyle(self, field):
        if field.data not in ['DoubleNoTouch','OutOfRangeRate']:
            raise ValidationError('option style error')

    def validate_I(self, field):
        if field.data < 0:
            raise ValidationError('I > 0')

    def validate_M(self, field):
        if field.data <= 0:
            raise ValidationError('M > 0')
            
    def validate_seedNum(self, field):
        if field.data < 0:
            raise ValidationError('seed > 0')

class OptionMCSForm3(FlaskForm):
    S0 = FloatField('S0', validators=[InputRequired()])
    K = FloatField('K', validators=[InputRequired()])
    T = FloatField('T', validators=[InputRequired()])
    r = FloatField('r', validators=[InputRequired()])
    q = FloatField('q', validators=[InputRequired()])
    sigma = FloatField('sigma', validators=[InputRequired()])
    Rp = FloatField('Rp', validators=[InputRequired()])
    optionType = SelectField('type', choices=[('call','call'), ('put', 'put')], validators=[DataRequired()])
    optionStyle = SelectField('style', 
        choices=[('DownAndOutAlternative','DownAndOutAlternative'),
                 ('ModerateOption','ModerateOption')], validators=[DataRequired()])
    I = IntegerField('I (MC)', validators=[InputRequired()])
    M = IntegerField('M (MC)', validators=[InputRequired()])
    seedNum = IntegerField('seed (MC)', validators=[InputRequired()])
    submit = SubmitField('Calculate')

    def validate_S0(self, field):
        if field.data < 0:
            raise ValidationError('S0 >= 0')
            
    def validate_K(self, field):
        if field.data < 0:
            raise ValidationError('K1 >= 0')

    def validate_T(self, field):
        if field.data <= 0:
            raise ValidationError('T > 0')

    def validate_r(self, field):
        if field.data < 0:
            raise ValidationError('r >= 0')

    def validate_q(self, field):
        if field.data < 0:
            raise ValidationError('q >= 0')
            
    def validate_sigma(self, field):
        if field.data <= 0:
            raise ValidationError('sigma > 0')
    
    def validate_Rp(self, field):
        if field.data < 0:
            raise ValidationError('Rp >= 0')
            
    def validate_optionType(self, field):
        if field.data not in ['call','put']:
            raise ValidationError('option type error')
            
    def validate_optionStyle(self, field):
        if field.data not in ['DownAndOutAlternative','ModerateOption']:
            raise ValidationError('option style error')

    def validate_I(self, field):
        if field.data < 0:
            raise ValidationError('I > 0')

    def validate_M(self, field):
        if field.data <= 0:
            raise ValidationError('M > 0')
            
    def validate_seedNum(self, field):
        if field.data < 0:
            raise ValidationError('seed > 0')
            
class ItemTable(Table):
    classes = ['table','table-striped']
    name = Col('name')
    valuation = Col('valuation')
    ratio = Col('ratio (v/S0)')

   
