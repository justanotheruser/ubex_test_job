from rest_framework import serializers

from player.models import Artist, Album, Track


class ArtistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = '__all__'

    def create(self, validated_data):
        return Artist.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class AlbumSerializer(serializers.ModelSerializer):

    class Meta:
        model = Album
        fields = '__all__'

    def create(self, validated_data):
        return Album.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.title = validated_data.get('title', instance.title)
        instance.release_date = validated_data.get('release_date', instance.release_date)
        instance.artist = validated_data.get('artist', instance.artist)
        instance.save()
        return instance


class TrackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Track
        fields = '__all__'

    def create(self, validated_data):
        return Track.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.title = validated_data.get('title', instance.title)
        instance.length = validated_data.get('length', instance.length)
        instance.artist = validated_data.get('artist', instance.artist)
        instance.album = validated_data.get('album', instance.album)
        instance.save()
        return instance
