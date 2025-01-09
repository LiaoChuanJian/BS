#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys


def main():
    """Run administrative tasks."""

    # 设置环境变量，指定 Django 的设置模块
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xy_compare.settings')

    try:
        # 从 Django 核心管理模块导入指令执行功能
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # 执行命令行指令
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
