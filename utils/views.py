import random
from uuid import uuid4

from captcha.image import ImageCaptcha
from django.core.cache import cache
from django.http import HttpResponse
from rest_framework.views import APIView

from vj.settings import CAPTCHA_AGE


class CaptchaAPI(APIView):

    @staticmethod
    def get(request, *args, **kwargs):
        text = ''.join(random.sample('345689ABCDEFGHIJKLMNPQRSTUVWXY', 4))
        uuid = uuid4()
        image = ImageCaptcha(width=120, height=40, font_sizes=(25, 30, 35))
        result = image.generate(text)
        res = HttpResponse(result, content_type='image/png')
        captcha_cache_key = f'captcha-{uuid}'
        cache.set(captcha_cache_key, text, CAPTCHA_AGE)
        res.set_cookie(key='CAPTCHA', value=captcha_cache_key, max_age=CAPTCHA_AGE, samesite='strict')
        return res

    @staticmethod
    def verify_captcha(request, captcha):
        """
        这是验证图形验证码的函数
        :param request: rest_framework.request.Request
        :type captcha: str
        """
        if 'CAPTCHA' not in request.COOKIES or request.COOKIES['CAPTCHA'] is None:
            return False
        captcha_cache_key = request.COOKIES['CAPTCHA']
        cache_captcha_value = cache.get(captcha_cache_key)
        cache.delete(captcha_cache_key)
        if cache_captcha_value != str.upper(captcha):
            return False
        return True