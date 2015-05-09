#coding=utf-8
from django import forms
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from simplemathcaptcha.fields import MathCaptchaField
from simplemathcaptcha.widgets import MathCaptchaWidget
from haystack.forms import SearchForm
from models import Terms
from django.core.files.images import get_image_dimensions
import os


def check_exist(value):
    t = Terms.objects.all()
    value = unicode(value)
    value = ' '.join(value.split())
    if t.filter(term=value).exists():
        uid = t.get(term=value).uid
        error_tips = mark_safe(u'【<a href="/%s.html">%s</a>】已经存在了，请前往该词条查看已有的释义，或添加新的' % (uid, value))
        raise ValidationError(error_tips)


def check_img(self):
    fileExtension = os.path.splitext(self._name)[1].lower()
    if fileExtension not in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
        raise forms.ValidationError(u"文件类型错误： %s" % fileExtension)
    w, h = get_image_dimensions(self)
    if w > 1000:
        raise forms.ValidationError(u"你上传的图片宽度是 %ipx. 不能超过1000px." % w)
    if h > 3000:
        raise forms.ValidationError(u"你上传的图片高度是 %ipx. 不能超过3000px." % h)


class TermForm(forms.Form):
    term = forms.CharField(max_length=20)
    definition = forms.CharField(widget=forms.Textarea, max_length=200, min_length=15, initial=u'释义:\n例句:')
    author = forms.CharField(max_length=65, required=False)
    homepage = forms.URLField(max_length=200, required=False)
    author_email = forms.EmailField(required=False)
    docfile = forms.ImageField(required=False)
    captcha = MathCaptchaField(widget=MathCaptchaWidget(question_tmpl="%(num1)i %(operator)s %(num2)i = "))

    def __init__(self, *args, **kwargs):
        super(TermForm, self).__init__(*args, **kwargs)
        self.fields['term'].validators.append(check_exist)
        self.fields['docfile'].validators.append(check_img)

    def clean_docfile(self):
        if self.cleaned_data['docfile']:
            if self.cleaned_data['docfile'].size > 3145728:
                raise forms.ValidationError(u"图片体积太大了.最多接受3MB.")
        return self.cleaned_data['docfile']


class DefinitionForm(forms.Form):
    definition = forms.CharField(widget=forms.Textarea, max_length=200, min_length=15, initial=u'释义:\n例句:')
    author = forms.CharField(max_length=65, required=False)
    homepage = forms.URLField(max_length=200, required=False)
    author_email = forms.EmailField(required=False)
    docfile = forms.ImageField(required=False)
    captcha = MathCaptchaField(widget=MathCaptchaWidget(question_tmpl="%(num1)i %(operator)s %(num2)i = "))

    def __init__(self, *args, **kwargs):
        super(DefinitionForm, self).__init__(*args, **kwargs)
        self.fields['docfile'].validators.append(check_img)

    def clean_docfile(self):
        if self.cleaned_data['docfile']:
            if self.cleaned_data['docfile'].size > 3145728:
                raise forms.ValidationError(u"图片体积太大了.最多接受3MB.")
        return self.cleaned_data['docfile']


class SearchForm2(SearchForm):
    q = forms.CharField(required=False, label='Search',
                        widget=forms.TextInput(attrs={'placeholder': '...'}))




