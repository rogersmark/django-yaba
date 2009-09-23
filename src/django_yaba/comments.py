import copy
from django_yaba import captcha
from django.conf import settings  
from django import http  
from django.contrib import comments  
from django.contrib.comments.forms import CommentForm  
from django.contrib.comments.views.comments import post_comment

def wrapped_post_comment(request, next=None):  
    request_copy = copy.copy(request)  
    request_copy.POST = request.POST.copy() # create a mutable copy  
    if '__recaptcha_ip' in request.POST:  
        return http.HttpResponseBadRequest()  
    request_copy.POST['__recaptcha_ip'] = request.META['REMOTE_ADDR']  
    return post_comment(request_copy, next)  

class ReCaptchaCommentForm(CommentForm):
    def __init__(self, target_object, data=None, initial=None):
        super(ReCaptchaCommentForm, self).__init__(target_object, data, initial)
		
    def clean(self):
        # If the form isn't being previewed, check the captcha
        if 'preview' not in self.data:
            challenge_field = self.data.get('recaptcha_challenge_field')
            response_field = self.data.get('recaptcha_response_field')
            client = self.data.get('__recaptcha_ip') # always set by our code
				
            check_captcha = captcha.submit(challenge_field, response_field,
                 settings.RECAPTCHA_PRIVATE_KEY, client)
				
            if check_captcha.is_valid is False:
                self.errors['recaptcha'] = 'Invalid captcha value'

        return self.cleaned_data

def recaptcha_get_form():
    return ReCaptchaCommentForm
	
comments.get_form = recaptcha_get_form
