# -*- coding:utf-8 -*-

from django.http import JsonResponse, HttpResponse
import json

class HttpCode(object):
    """HTTP状态码类"""
    success = 0  # 成功代码
    error = 1  # 错误代码


def success_no_wrapper(data=None):
    """
    返回成功响应，不包装在 JSON 结构中。
    :param data: 要返回的数据，默认为 None
    :return: HttpResponse，包含 JSON 格式的数据
    """
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json")


def result(code=HttpCode.success, message='', data=None, kwargs=None, count=None):
    """
    构建统一的响应结构。
    :param code: 状态码，默认为成功
    :param message: 响应消息，默认为空
    :param data: 返回的数据，默认为 None
    :param kwargs: 其他额外的信息，默认为 None
    :param count: 数据条目计数，默认为 None
    :return: JsonResponse，包含完整的响应结构
    """
    json_dict = {
        'data': data,
        'code': code,
        'message': message,
        'count': count  # 可选: 数据条目计数
    }

    # 打印响应数据到控制台，方便调试
    print(json_dict)

    # 如果有额外的 kwargs 更新到响应字典中
    if kwargs and isinstance(kwargs, dict) and kwargs.keys():
        json_dict.update(kwargs)

    return JsonResponse(json_dict, json_dumps_params={'ensure_ascii': False})


def success(data=None):
    """
    返回成功响应，标准格式。
    :param data: 要返回的数据，默认为 None
    :return: JsonResponse
    """
    return result(code=HttpCode.success, message='OK', data=data)


def success_by_count(data=None, count=""):
    """
    返回成功响应，并包括数据条目计数。
    :param data: 要返回的数据，默认为 None
    :param count: 数据条目计数
    :return: JsonResponse
    """
    return result(code=HttpCode.success, message='OK', data=data, count=count)


def error(message='', data=None):
    """
    返回错误响应。
    :param message: 错误信息
    :param data: 要返回的数据，默认为 None
    :return: JsonResponse
    """
    return result(code=HttpCode.error, message=message, data=data)
