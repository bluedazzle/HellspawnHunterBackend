# coding: utf-8
from __future__ import unicode_literals

from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView

from core.Mixin.CheckMixin import CheckSecurityMixin
from core.Mixin.StatusWrapMixin import StatusWrapMixin
from core.dss.Mixin import MultipleJsonResponseMixin, JsonResponseMixin
from core.dss.Serializer import serializer
from core.models import Hellspawn, Scene, Team, Membership
from core.Mixin import StatusWrapMixin as SW


class HellspawnListView(CheckSecurityMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    model = Hellspawn
    paginate_by = 20


class HellspawnDetailView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    model = Hellspawn
    pk_url_kwarg = 'id'

    def get_object(self, queryset=None):
        obj = super(HellspawnDetailView, self).get_object(queryset)
        obj.rarity = unicode(obj.rarity_choice[obj.rarity - 1][1]).lower()
        return obj


class SceneListView(CheckSecurityMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    model = Scene
    many = True
    foreign = True
    paginate_by = 10
    exclude_attr = ['create_time', 'modify_time', 'belong']

    def get_queryset(self):
        queryset = super(SceneListView, self).get_queryset()
        map(lambda obj: setattr(obj, 'team_list', obj.scene_teams.all()), queryset)
        return queryset


class SceneDetailView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    model = Scene
    pk_url_kwarg = 'id'


class SearchListView(CheckSecurityMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    model = Hellspawn

    def get_queryset(self):
        value = self.kwargs.get('value', '')
        queryset = super(SearchListView, self).get_queryset()
        queryset = queryset.filter(Q(name__icontains=value) | Q(clue1__icontains=value) | Q(clue2__icontains=value))
        return queryset


class HellspawnSceneListView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, ListView):
    model = Scene
    many = True

    exclude_attr = ['create_time', 'modify_time']

    def get(self, request, *args, **kwargs):
        hellspawns = Hellspawn.objects.filter(id=kwargs.get('id'))
        if not hellspawns.exists():
            self.message = 'id 不存在'
            self.status_code = SW.INFO_NO_EXIST
            return self.render_to_response({})
        hellspawn = hellspawns[0]
        # queryset = self.get_queryset()
        teams = Team.objects.filter(monsters=hellspawn)
        scenes = []
        for team in teams:
            scenes.append(team.belong)
        scenes = set(scenes)
        scene_list = []
        for scene in scenes:
            teams = Team.objects.filter(belong=scene)
            setattr(scene, 'team_list', teams)
            hellspawn_count = 0
            for team in teams:
                mems = Membership.objects.filter(team=team, hellspawn=hellspawn)
                if mems.exists():
                    mem = mems[0]
                    hellspawn_count += mem.count
            setattr(scene, 'hellspawn_info', {'name': hellspawn.name, 'count': hellspawn_count})
        return self.render_to_response(
            {'scene_list': sorted(scenes, key=lambda x: x.hellspawn_info['count'], reverse=True)})
