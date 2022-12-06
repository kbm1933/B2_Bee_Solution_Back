from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from similarity import make_solution
from makesolution import make_wise_image
from article.models import Solution, Article, Rating
from article.serializers import WorrySerializer,BeeSolutionSerializer, RatingSerializer, CommentSerializer, MakeSolutionSerializer


class MakeWorryView(APIView):
    def post(self, request):
        
        my_id = request.user.id
        result = make_solution(my_id)

        worry_serializer = WorrySerializer(data = request.data)
        if worry_serializer.is_valid():
            worry_serializer.save(user=request.user, solution_id= result)
            return Response(worry_serializer.data, status=status.HTTP_200_OK)
        return Response(worry_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        solution = Article.objects.filter(user_id = request.user.id).last()
        solution_serializer = WorrySerializer(solution)
        return Response(solution_serializer.data, status=status.HTTP_200_OK)
      
class BeeSolutionView(APIView):  
    def get(self,request, solution_id):
        bee_solution = Solution.objects.get(id = solution_id)
        bee_solution_serializer = BeeSolutionSerializer(bee_solution)
        return Response(bee_solution_serializer.data, status=status.HTTP_200_OK)
    
    def post(self,request,solution_id):
        rating_serializer = RatingSerializer(data = request.data)
        if rating_serializer.is_valid():
            #같은 유저가 같은 솔루션을 평가했는지 체크
            if Rating.objects.filter(user_id = request.user.id, solution_id = solution_id).exists():
                Rating.objects.filter(user_id = request.user.id, solution_id = solution_id).delete()
                rating_serializer.save(user = request.user, solution_id = solution_id)
                return Response({"message":"평가 완료"}, status=status.HTTP_200_OK)
            else:
                rating_serializer.save(user = request.user, solution_id = solution_id)
                return Response({"message":"평가 완료"}, status=status.HTTP_200_OK)
        return Response(rating_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentView(APIView):
    def get(self,request,article_id):
        article=  Article.objects.get(id=article_id)
        comments = article.comment_set.all()
        comment_serializer = CommentSerializer(comments,many=True)
        return Response(comment_serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request,article_id):
        comment_serializer = CommentSerializer(data=request.data)
        if comment_serializer.is_valid():
            comment_serializer.save(comment_user = request.user, article_id = article_id)
            return Response(comment_serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(comment_serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class MakeSolutionView(APIView):
    def get(self, request, article_id):
        pass
    
    def post(self, request, article_id):
        make_solution_serializer = MakeSolutionSerializer(data=request.data)
        if make_solution_serializer.is_valid():
            # 원본사진 저장
            make_solution_serializer.save(user=request.user)
            # solition 적용 이미지 저장
            latest_idx = Solution.objects.order_by('-pk')[0].pk
            make_wise_image(latest_idx)
            
            return Response("저장 완료", status=status.HTTP_200_OK)
        else:
            return Response("실패", status=status.HTTP_400_BAD_REQUEST)

class MainView(APIView):
    def get(self,request):
        main_articles = Article.objects.all()
        main_serializer = WorrySerializer(main_articles,many=True)
        return Response(main_serializer.data,status=status.HTTP_200_OK)

class ArticleListView(APIView):
    def get(self, request, category_id):

        if category_id == 1:
            category = '음식'
        elif category_id == 2:
            category = '취미'
        elif category_id == 3:
            category = '취업'
        elif category_id == 4:
            category = '일상'
        elif category_id == 5:
            category = '투자'
        elif category_id == 6:
            category = '연애'
        elif category_id == 7:
            category = '스포츠'
        elif category_id == 8:
            category = '연예'

        if category_id == 9:
            mbti = 'ENFP'
        elif category_id == 10:
            mbti = 'ENFJ'
        elif category_id == 11:
            mbti = 'ENTP'
        elif category_id == 12:
            mbti = 'ENTJ'
        elif category_id == 13:
            mbti = 'ESFP'
        elif category_id == 14:
            mbti = 'ESFJ'
        elif category_id == 15:
            mbti = 'ESTP'
        elif category_id == 16:
            mbti = 'ESTJ'
        elif category_id == 17:
            mbti = 'INFP'
        elif category_id == 18:
            mbti = 'INFJ'
        elif category_id == 19:
            mbti = 'INTP'
        elif category_id == 20:
            mbti = 'INTJ'
        elif category_id == 21:
            mbti = 'ISFP'
        elif category_id == 22:
            mbti = 'ISFJ'
        elif category_id == 23:
            mbti = 'ISTP'
        elif category_id == 24:
            mbti = 'ISTJ'

        if category_id >=9:
            articles = Article.objects.filter(mbti=mbti)
        else:
            articles = Article.objects.filter(category = category)
            
        article_serializer = WorrySerializer(articles, many = True)
        return Response(article_serializer.data, status=status.HTTP_200_OK)
