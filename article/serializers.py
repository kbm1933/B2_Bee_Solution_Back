from rest_framework import serializers
from article.models import Article, Solution, Rating

class WorrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields=['category','content','mbti']

class BeeSolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = ['wise',] #solution_image로 변경할 것 
        
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields=['rating',]

        