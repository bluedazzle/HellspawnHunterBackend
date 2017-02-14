from __future__ import unicode_literals

from django.db import models


# Create your models here.
class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Hellspawn(BaseModel):
    rarity_choice = [(1, 'SSR'),
                     (2, 'SR'),
                     (3, 'R'),
                     (4, 'N')]

    name = models.CharField(max_length=20)
    rarity = models.IntegerField(choices=rarity_choice, default=4)
    picture = models.CharField(max_length=128, null=True, blank=True)
    icon = models.CharField(max_length=128, null=True, blank=True)

    def __unicode__(self):
        return '{0}-{1}'.format(self.name, self.rarity_choice[self.rarity - 1][1])


class Scene(BaseModel):
    name = models.CharField(max_length=20)
    icon = models.CharField(max_length=128, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Team(BaseModel):
    name = models.CharField(max_length=20)
    monsters = models.ManyToManyField(Hellspawn, related_name='hellspawn_teams', through='Membership',
                                      through_fields=('team', 'hellspawn'))
    belong = models.ForeignKey(Scene, related_name='scene_teams')

    def __unicode__(self):
        return '{0}: {1}'.format(self.belong.name, self.name)


class Secret(BaseModel):
    secret = models.CharField(max_length=256, unique=True)
    remark = models.CharField(default='web', max_length=10)

    def __unicode__(self):
        return self.remark


class Membership(BaseModel):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    hellspawn = models.ForeignKey(Hellspawn, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)

    def __unicode__(self):
        return '{0}X{1} - {2}{3}'.format(self.hellspawn.name, self.count, self.team.belong.name, self.team.name)


class Clue(BaseModel):
    value1 = models.CharField(max_length=30)
    value2 = models.CharField(max_length=30, null=True, blank=True)
    hellspawn = models.ForeignKey(Hellspawn, related_name='hellspawn_clues', on_delete=models.SET_NULL, null=True,
                                  blank=True)

    def __unicode__(self):
        return self.value1
