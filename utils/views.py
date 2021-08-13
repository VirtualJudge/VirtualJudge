import json
import random
from uuid import uuid4
from django_redis import get_redis_connection
from captcha.image import ImageCaptcha
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from utils.response import msg
from vj.settings import CAPTCHA_AGE
from vj.config import remote_ojs


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


class LanguageAPI(APIView):
    @staticmethod
    def get(request, remote_oj, *args, **kwargs):
        if remote_oj not in remote_ojs:
            return JsonResponse(msg([], err='Platform not supported yet.'))
        # Language Identifiers: https://github.com/Microsoft/monaco-editor-webpack-plugin#options
        if remote_oj == 'Codeforces':
            res = [
                {"key": "43", "val": "GNU GCC C11 5.1.0", 'identifier': 'cpp'},
                {"key": "52", "val": "Clang++17 Diagnostics", 'identifier': 'cpp'},
                {"key": "42", "val": "GNU G++11 5.1.0", 'identifier': 'cpp'},
                {"key": "50", "val": "GNU G++14 6.4.0", 'identifier': 'cpp'},
                {"key": "54", "val": "GNU G++17 7.3.0", 'identifier': 'cpp'},
                {"key": "2", "val": "Microsoft Visual C++ 2010", 'identifier': 'cpp'},
                {"key": "59", "val": "Microsoft Visual C++ 2017", 'identifier': 'cpp'},
                {"key": "61", "val": "GNU G++17 9.2.0 (64 bit, msys 2)", 'identifier': 'cpp'},
                {"key": "65", "val": "C# 8, .NET Core 3.1", 'identifier': 'csharp'},
                {"key": "9", "val": "C# Mono 6.8", 'identifier': 'csharp'},
                {"key": "28", "val": "D DMD32 v2.091.0"},
                {"key": "32", "val": "Go 1.15.6", 'identifier': 'go'},
                {"key": "12", "val": "Haskell GHC 8.10.1"},
                {"key": "60", "val": "Java 11.0.6", 'identifier': 'java'},
                {"key": "36", "val": "Java 1.8.0_241", 'identifier': 'java'},
                {"key": "48", "val": "Kotlin 1.4.0", 'identifier': 'kotlin'},
                {"key": "19", "val": "OCaml 4.02.1"},
                {"key": "3", "val": "Delphi 7"},
                {"key": "4", "val": "Free Pascal 3.0.2"},
                {"key": "51", "val": "PascalABC.NET 3.4.2"},
                {"key": "13", "val": "Perl 5.20.1"},
                {"key": "6", "val": "PHP 7.2.13"},
                {"key": "7", "val": "Python 2.7.18", 'identifier': 'python'},
                {"key": "31", "val": "Python 3.8.10", 'identifier': 'python'},
                {"key": "40", "val": "PyPy 2.7 (7.3.0)", 'identifier': 'python'},
                {"key": "41", "val": "PyPy 3.7 (7.3.0)", 'identifier': 'python'},
                {"key": "67", "val": "Ruby 3.0.0"},
                {"key": "49", "val": "Rust 1.49.0", 'identifier': 'rust'},
                {"key": "20", "val": "Scala 2.12.8"},
                {"key": "34", "val": "JavaScript V8 4.8.0"},
                {"key": "55", "val": "Node.js 12.6.3"},
                {"key": "14", "val": "ActiveTcl 8.5"},
                {"key": "15", "val": "Io-2008-01-07 (Win32)"},
                {"key": "17", "val": "Pike 7.8"},
                {"key": "18", "val": "Befunge"},
                {"key": "22", "val": "OpenCobol 1.0"},
                {"key": "25", "val": "Factor"},
                {"key": "26", "val": "Secret_171"},
                {"key": "27", "val": "Roco"},
                {"key": "33", "val": "Ada GNAT 4"},
                {"key": "38", "val": "Mysterious Language"},
                {"key": "39", "val": "FALSE"},
                {"key": "44", "val": "Picat 0.9"},
                {"key": "45", "val": "GNU C++11 5 ZIP", 'identifier': 'cpp'},
                {"key": "46", "val": "Java 8 ZIP", 'identifier': 'java'},
                {"key": "47", "val": "J"},
                {"key": "56", "val": "Microsoft Q#"},
                {"key": "57", "val": "Text"},
                {"key": "62", "val": "UnknownX"},
                {"key": "68", "val": "Secret 2021"}
            ]
            return JsonResponse(msg(res))
        elif remote_oj == 'HDU':
            res = [
                {"key": "0", "val": "G++", 'identifier': 'cpp'},
                {"key": "1", "val": "GCC", 'identifier': 'cpp'},
                {"key": "2", "val": "C++", 'identifier': 'cpp'},
                {"key": "3", "val": "C", 'identifier': 'cpp'},
                {"key": "4", "val": "Pascal", 'identifier': 'pascal'},
                {"key": "5", "val": "Java", 'identifier': 'java'},
                {"key": "6", "val": "C#", 'identifier': 'csharp'}
            ]
            return JsonResponse(msg(res))
        return JsonResponse(msg([]))


class PlatformAPI(APIView):
    @staticmethod
    def get(request, *args, **kwargs):
        return JsonResponse(msg(remote_ojs))
