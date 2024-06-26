from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from django.views import View
from django.http import JsonResponse, HttpResponse
from .decorators import *
from .models import Game, Tournament, User
#from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from .helpers_games import update_tournament_status
#import logging
#logging.basicConfig(level=logging.INFO)
#logger = logging.getLogger(__name__)

# Endpoint: /games
@method_decorator(check_structure("/games"), name='dispatch')
class GameView(View):
	def post(self, request):
		try:
			player1 = User.objects.get(id=request.json.get('player1_id'))
			player2 = User.objects.get(id=request.json.get('player2_id'))
			if player1.id is player2.id:
				return JsonResponse({ERROR_FIELD: "You can't play against yourself"}, status=400)
			game = Game(player1=player1, player2=player2)
			#game.full_clean()
			game.save()
		except ValidationError as e:
			return JsonResponse({"type": "object", ERROR_FIELD: e.message_dict}, status=400)
		except Exception as e:
			return JsonResponse({ERROR_FIELD: str(e)}, status=500)

		return JsonResponse(game.serialize(), status=201)

# Endpoint: /tournaments/TOURNAMENT_ID/games
@method_decorator(check_structure("/tournaments/TOURNAMENT_ID/games"), name='dispatch')
@method_decorator(check_object_exists(Tournament, 'tournament_id', TOURNAMENT_404), name='dispatch')
class TournamentGameCollection(View):

	def get(self, request, tournament_id):
		tournament = Tournament.objects.get(id=tournament_id)
		games = Game.objects.filter(tournament=tournament)
		return JsonResponse([g.serialize() for g in games], safe=False)

# Endpoint: /tournaments/TOURNAMENT_ID/games/GAME_ID
@method_decorator(check_structure("/tournaments/TOURNAMENT_ID/games/GAME_ID"), name='dispatch')
@method_decorator(check_object_exists(Tournament, 'tournament_id', TOURNAMENT_404), name='dispatch')
@method_decorator(check_object_exists(Game, 'game_id', GAME_404), name='dispatch')
class TournamentGameSingle(View):

	def get(self, request, tournament_id, game_id):
		game = Game.objects.get(id=game_id)
		return JsonResponse(game.serialize())

	def patch(self, request, tournament_id, game_id):
		game = Game.objects.get(id=game_id)
		# verify the user is one of the players - skipped for now
		#if game.player1_id != request.user.id and game.player2_id != request.user.id:
		#	return JsonResponse({ERROR_FIELD: "You are not a player in this game"}, status=400)
		if game.status == Game.MatchStatus.CREATED and game.tournament.status == Tournament.TournamentStatus.ONGOING:
			player1_score = int(request.json.get('player1_score', 0))
			player2_score = int(request.json.get('player2_score', 0))
			if (player1_score == 11 or player2_score == 11) and (player1_score + player2_score < 22):
				game.player1_score = player1_score
				game.player2_score = player2_score
				game.status = Game.MatchStatus.DONE
				game.save()
				#if all tournament games are done and/or cancelled then update the tournament.status to DONE
				update_tournament_status(game.tournament)
				return JsonResponse(game.serialize())
			else:
				return JsonResponse({ERROR_FIELD: "Invalid player(s) score"}, status=400)
		else:
			return JsonResponse({ERROR_FIELD: "Change not allowed"}, status=400)

	def delete(self, request, tournament_id, game_id):
		game = Game.objects.get(id=game_id)
		# verify the user is the creator of the tournament
		if game.tournament.creator_id != request.user.id:
			return JsonResponse({ERROR_FIELD: "You are not the creator of this tournament"}, status=400)
		# verify if the game is not already done
		if game.status == Game.MatchStatus.DONE:
			return JsonResponse({ERROR_FIELD: "You can't delete a game that is done"}, status=400)
		game.status = Game.MatchStatus.CANCELLED
		game.save()
		return JsonResponse(game.serialize())

# Endpoint: /games/GAME_ID
@method_decorator(check_structure("/games/GAME_ID"), name='dispatch')
@method_decorator(check_object_exists(Game, 'game_id', GAME_404), name='dispatch')
class GameDetail(View):

	def get(self, request, game_id):
		g = Game.objects.get(id=game_id)
		return JsonResponse(g.serialize())

	def patch(self, request, game_id):
		try:
			game = Game.objects.get(id=game_id, tournament_id=None, status=Game.MatchStatus.CREATED)
			# verify the user is one of the players
			if game.player1_id != request.user.id and game.player2_id != request.user.id:
				return JsonResponse({ERROR_FIELD: "You are not a player in this game"}, status=400)

			player1_score = int(request.json.get('player1_score', 0))
			player2_score = int(request.json.get('player2_score', 0))
			if (player1_score == 11 or player2_score == 11) and (player1_score + player2_score < 22):
				game.player1_score = player1_score
				game.player2_score = player2_score
				game.status = Game.MatchStatus.DONE
				game.save()
				return JsonResponse(game.serialize())
			else:
				return JsonResponse({ERROR_FIELD: "Invalid player(s) score"}, status=400)
		except Exception as e:
			return JsonResponse({ERROR_FIELD: str(e)}, status=500)


	@method_decorator(staff_required, name='dispatch')
	def delete(self, request, game_id):
		Game.objects.get(id=game_id).delete()

		# TODO: Implement websocket notification?

		return HttpResponse(status=204)
