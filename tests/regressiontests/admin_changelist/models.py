from django.db import models

class Event(models.Model):
    date = models.DateField()

class Parent(models.Model):
    name = models.CharField(max_length=128)

class Child(models.Model):
    parent = models.ForeignKey(Parent, editable=False, null=True)
    name = models.CharField(max_length=30, blank=True)
    age = models.IntegerField(null=True, blank=True)

class Genre(models.Model):
    name = models.CharField(max_length=20)

class Band(models.Model):
    name = models.CharField(max_length=20)
    nr_of_members = models.PositiveIntegerField()
    genres = models.ManyToManyField(Genre)

class Musician(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=30)
    members = models.ManyToManyField(Musician, through='Membership')

    def __unicode__(self):
        return self.name

class Membership(models.Model):
    music = models.ForeignKey(Musician)
    group = models.ForeignKey(Group)
    role = models.CharField(max_length=15)

class Quartet(Group):
    pass

class ChordsMusician(Musician):
    pass

class ChordsBand(models.Model):
    name = models.CharField(max_length=30)
    members = models.ManyToManyField(ChordsMusician, through='Invitation')

class Invitation(models.Model):
    player = models.ForeignKey(ChordsMusician)
    band = models.ForeignKey(ChordsBand)
    instrument = models.CharField(max_length=15)

class Swallow(models.Model):
    origin = models.CharField(max_length=255)
    load = models.FloatField()
    speed = models.FloatField()

    class Meta:
        ordering = ('speed', 'load')


class UnorderedObject(models.Model):
    """
    Model without any defined `Meta.ordering`.
    Refs #17198.
    """
    bool = models.BooleanField(default=True)


class OrderedObjectManager(models.Manager):
    def get_query_set(self):
        return super(OrderedObjectManager, self).get_query_set().order_by('number')

class OrderedObject(models.Model):
    """
    Model with Manager that defines a default order.
    Refs #17198.
    """
    name = models.CharField(max_length=255)
    bool = models.BooleanField(default=True)
    number = models.IntegerField(default=0, db_column='number_val')

    objects = OrderedObjectManager()
