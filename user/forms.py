from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm, CharField
from user.models import User



class UserForm(ModelForm):
	class Meta:
		model = User
		fields = ['nickname', 'password', 'icon', 'sex', 'age']
		error_messages = {
			'nickname': {
				'required': _('不能为空'),
				'unique': _('昵称已存在！'),
			},
			'password': {
				'required': _('不能为空')
			},
			'age': {
				'Enter a whole number': _('必须为数字')
			}


		}
	password2 = CharField(max_length=128)

	# 校验密码
	def clean_password2(self):
		cleaned_data = super().clean()

		if len(cleaned_data['password']) < 5:
			raise forms.ValidationError('密码长度过短！')
		elif cleaned_data['password'] != cleaned_data['password2']:
			raise forms.ValidationError('两次密码不一致！')
	
