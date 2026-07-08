#!/usr/bin/env python
"""Fake manage.py — this project never runs, it only exists to be scanned."""
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vulnapp.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
