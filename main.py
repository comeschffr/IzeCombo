from flask import Blueprint, render_template, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
import requests, json


GENDERIZE_URL = 'https://api.genderize.io'
AGIFY_URL = 'https://api.agify.io'
NATIONALIZE_URL = 'https://api.nationalize.io'
COUNTRY_URL = 'https://restcountries.eu/rest/v2/alpha/'


main = Blueprint('main', __name__)


def send_request(url, args={}):
	request = requests.get(url, params=args)
	if request.status_code == 200:
		return request.json()
	else:
		return {}


@main.route('/', methods=['GET', 'POST'])
def home():
	form = NameForm()
	result = {}

	if form.validate_on_submit():
		args = {'name': form.name.data}
		try: # In case name not referenced
			args['country_id'] = send_request(NATIONALIZE_URL, args=args).get('country')[0].get('country_id')
		except IndexError:
			args['country_id'] = ''

		result['country'] = send_request(COUNTRY_URL+args['country_id']).get('demonym')
		result['gender'] = send_request(GENDERIZE_URL, args=args).get('gender')
		result['age'] = send_request(AGIFY_URL, args=args).get('age')
	

	return render_template('main.html', form=form, result=result)


class NameForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	submit = SubmitField('Magic')

	def validate_name(self, name):
		tmp_country = send_request(NATIONALIZE_URL, args={'name': name.data}).get('country')
		if len(tmp_country) < 1:
			raise ValidationError('Name not referenced')
