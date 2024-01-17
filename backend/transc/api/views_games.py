from django.utils.decorators import method_decorator
from .decorators import login_required, check_body_syntax, check_object_exists
from django.views import View
from django.http import JsonResponse, Http404
from .models import Game
#from django.utils.decorators import method_decorator
#from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
import json
import datetime

# GET/POST  /games
@method_decorator(login_required, name='dispatch')
class GameView(View):
	def get(self, request):
		games = Game.objects.all()
		data = {
			'games': [g.serialize() for g in games],
			'count': games.count(),
		}
		return JsonResponse(data)

	@check_body_syntax(['game_id', 'player_id', 'player2_id'])
	def post(self, request):
		game_data = {
			'game_id': self.body.get('game_id'),
			'player_id': self.body.get('player_id'),
			'player2_id': self.body.get('player2_id'),
			#'status': GameStatus::CREATED - set at DB level
			#'created_at': datetime.datetime.now()
		}
		t = Game.objects.create(**game_data) # TODO: Check if creating is successful
		return JsonResponse(t.serialize(), status=201)

#games/<int:game_id>
@method_decorator(login_required, name='dispatch')
@method_decorator(check_object_exists(Game, 'game_id', 
																			'Game does not exist'), name='dispatch')
class GameDetail(View):
	def get(self, request, game_id):
		g = Game.objects.get(pk=game_id)
		return JsonResponse({'game': g.serialize()})

	# allow only update of title and description
	@check_body_syntax(['title', 'description'])
	def patch(self, request, game_id):
		g = Game.objects.get(pk=game_id)
		g.title = self.body.get('title')
		g.description = self.body.get('description')
		g.updated_at = datetime.datetime.now()
		g.save()
		return JsonResponse(g.serialize(), status=200, safe=False)

	def delete(self, request, game_id):
		g = Game.objects.get(pk=game_id)
		g.delete()
		return JsonResponse({}, status=202)
