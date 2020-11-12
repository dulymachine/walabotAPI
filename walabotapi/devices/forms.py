from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from walabotapi.models import User, Device



class DeviceForm(FlaskForm):
  device_id = StringField('Device ID', validators=[DataRequired()])
  patient_name = StringField('Patient Name', validators=[DataRequired()])
  location = TextAreaField('Location Description', validators=[DataRequired()])
  submit = SubmitField('Register')

  def validate_device_id(self, device_id):
    device = Device.query.filter_by(device_id=device_id.data).first()
    if device:
      raise ValidationError('That device ID has already been registered. Please register another device.')