# coding: utf-8
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from core.models import Membership


class Command(BaseCommand):
    def handle(self, *args, **options):
        members = Membership.objects.all()
        for mem in members:
            if mem.team.name == '第一回合' or mem.team.name == '第二回合':
                if '挑战' in mem.team.belong.name:
                    mem.count = 4
                    mem.save()

