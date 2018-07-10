from rest_framework import serializers
from projeto.edp.models import RecursosEdp, Edp, RespostaEdp


class RecursosEdpSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecursosEdp
        fields = 'id', 'edp', 'video_embedded', 'texto', 'recebe_texto', 'recebe_video_embedded', 'recebe_video', 'recebe_imagem', 'video'


class EdpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edp
        fields = 'id', 'titulo', 'slug', 'objetivo_pedagogico', 'habilidades', 'atividades', 'metodologia', 'usuario', 'nivel'

class RespostasEdpSerializer(serializers.ModelSerializer):
    class Meta:
        model = RespostaEdp
        fields = 'id','eda', 'video_embedded', 'texto', 'video', 'usuario', 