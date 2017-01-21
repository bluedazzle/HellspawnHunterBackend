# coding: utf-8
from __future__ import unicode_literals
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from core.Mixin.CheckMixin import CheckSecurityMixin
from core.Mixin.StatusWrapMixin import StatusWrapMixin
from core.dss.Mixin import MultipleJsonResponseMixin
from core.models import Hellspawn, Scene, Clue


class HellspawnListView(CheckSecurityMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    model = Hellspawn
    paginate_by = 20


class SceneListView(CheckSecurityMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    model = Scene
    many = True
    foreign = True
    paginate_by = 10
    exclude_attr = ['create_time', 'modify_time']


class ClueListView(CheckSecurityMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    model = Clue
    foreign = True
    paginate_by = 20
    exclude_attr = ['create_time', 'modify_time']
