#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xy_compare.settings')
    try:
        from django.core.management import execute_from_command_line #导入 Django 的管理命令执行函数
    except ImportError as exc: #处理 ImportError 异常
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv) #执行命令行指令


if __name__ == '__main__':
    main()
