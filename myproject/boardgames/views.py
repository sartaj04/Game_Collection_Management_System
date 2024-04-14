from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView
from .models import BoardGame, UserProfile, Wishlist, Library, Club
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.db.models import F
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import BoardGame, Review, CommunityMember
from .forms import ReviewForm, JoinCommunityForm
from django.db import IntegrityError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


from django.shortcuts import render, redirect
from .models import Club
from .forms import JoinClubForm

def join_club(request):
    if request.method == 'POST':
        form = JoinClubForm(request.POST)
        if form.is_valid():
            club = form.cleaned_data['club']
            club_id = club.id

            user_profile = UserProfile.objects.get(username=request.user.username)
            user_profile.clubs.add(club_id)
            user_profile.save()
            return redirect('boardgames:club_list')
    else:
        form = JoinClubForm()

    return render(request, 'boardgames/join_club.html', {'form': form})


@login_required
def user_profile(request, user_id):
    # user = request.user
    user = get_object_or_404(UserProfile, id=user_id)
    library_items = Library.objects.filter(user=user)

    wishlist_items = Wishlist.objects.filter(user=user)

    communities = CommunityMember.objects.filter(user=user)

    reviews = Review.objects.filter(user=user)

    clubs = user.clubs.all()


    context = {
        'user': user,
        'library_items': library_items,
        'wishlist_items': wishlist_items,
        'communities': communities,
        'reviews': reviews,
        'clubs': clubs,
    }
    return render(request, 'boardgames/user_profile.html', context)

class BoardGameListView(ListView):
    model = BoardGame
    template_name = 'boardgames/board_games_list.html'
    context_object_name = 'boardgames'

@login_required
def remove_from_wishlist(request, game_id):
    try:
        board_game = BoardGame.objects.get(id=game_id)
        user_profile = request.user
        print(f"Removing {board_game.title} from the wishlist of {user_profile.username}")
        user_profile.wishlist.remove(board_game)
        user_profile.save()
        user_wishlist_item = Wishlist.objects.get(user=user_profile, game=board_game)
        user_wishlist_item.delete()
        messages.success(request, f"Removed {board_game.title} from your wishlist.")
    except BoardGame.DoesNotExist:

        messages.error(request, f"Board game with ID {game_id} does not exist.")
    except Exception as e:
        messages.error(request, f"Error: {e}")

    return redirect('boardgames:wishlist')

@login_required
def add_review(request, game_id):
    game = BoardGame.objects.get(pk=game_id)
    user_profile = request.user
    existing_review = Review.objects.filter(user=user_profile, game=game).first()

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=existing_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = user_profile
            review.game = game
            review.save()
            return redirect('boardgames:detail', pk=game.pk)

    else:
        form = ReviewForm(instance=existing_review)

    return render(request, "boardgames/add_review.html", {"form": form, "game_id": game_id})



@login_required
def join_community(request, game_id):
    game = BoardGame.objects.get(pk=game_id)
    community_members = CommunityMember.objects.filter(game=game)[:6]
    users = [member.user for member in community_members]

    if request.method == "POST":
        form = JoinCommunityForm(request.POST)
        if form.is_valid():
            community_member = form.save(commit=False)
            community_member.user = request.user
            community_member.game = game

            try:
                community_member.save()
                return redirect('boardgames:detail', pk=game.pk)
            except IntegrityError:
                form.add_error(None, "You have already joined this game community.")
    else:
        form = JoinCommunityForm()

    return render(request, "boardgames/join_community.html", {"form": form, "game_id": game_id, "users": users})

def club_list(request):
    clubs = Club.objects.all()
    return render(request, 'boardgames/club_list.html', {'clubs': clubs})
def detail(request, pk):
    boardgame = BoardGame.objects.get(pk=pk)
    reviews = Review.objects.filter(game=boardgame)
    community_members = CommunityMember.objects.filter(game=boardgame)

    context = {
        'boardgame': boardgame,
        'reviews': reviews,
        'community_members': community_members
    }
    return render(request, 'boardgames/detail.html', context)





def board_games_list(request):
    boardgames = BoardGame.objects.all()

    categories = set()
    for boardgame in boardgames:
        for category in boardgame.categories[2:-2].split("', '"):
            category = category.strip()
            if "," not in category:
                categories.add(category)
    games_limit = 20
    categorized_boardgames = {
        category: sorted(
            [boardgame for boardgame in boardgames if category in boardgame.categories[2:-2].split("', '")],
            key=lambda x: x.rating,
            reverse=True
        )[:games_limit]
        for category in categories
    }

    hot_games = BoardGame.objects.order_by('-rating')[:10]

    sorted_categories = sorted(categorized_boardgames, key=lambda x: len(categorized_boardgames[x]), reverse=True)
    sorted_categorized_boardgames = {category: categorized_boardgames[category] for category in sorted_categories}
    context = {
        'categorized_boardgames': sorted_categorized_boardgames,
        'hot_games': hot_games,
    }
    return render(request, 'boardgames/board_games_list.html', context)


    # return render(request, 'boardgames/board_games_list.html', {'categorized_boardgames': sorted_categorized_boardgames})

@login_required
def recommendations_user(request, user_id):
    user = request.user
    library = user.library_items.all()
    wishlist = user.wishlist_items.all()

    print("Library:", library)
    print("Wishlist:", wishlist)

    combined_games = [lib_item.game for lib_item in library] + [wish_item.game for wish_item in wishlist]
    recommendations = []
    for game in combined_games:
        game_recommendations = game.get_recommendations(library, wishlist)
        print(f"Recommendations for {game.title}: {game_recommendations}")
        recommendations.extend(game_recommendations)

    unique_recommendations = list(set(recommendations))[:10]
    print("Final Recommendations:", unique_recommendations)

    return render(request, 'boardgames/recommendations_user.html', {'recommended_games': unique_recommendations})




def recommendations(request, pk):
    boardgame = get_object_or_404(BoardGame, pk=pk)
    current_game_categories = set(boardgame.categories[2:-2].split("', '"))
    other_boardgames = BoardGame.objects.exclude(pk=pk)
    recommended_games = []
    for other_game in other_boardgames:
        other_game_categories = set(other_game.categories[2:-2].split("', '"))
        if current_game_categories.intersection(other_game_categories):
            recommended_games.append(other_game)
            if len(recommended_games) >= 10:
                break

    return render(request, 'boardgames/recommendations.html', {'boardgame': boardgame, 'recommended_games': recommended_games})



def search(request):
    query = request.GET.get('search_input')
    if query:
        results = BoardGame.objects.filter(
            Q(title__icontains=query) |
            Q(short_description__icontains=query) |
            Q(designers__icontains=query) |
            Q(artists__icontains=query) |
            Q(publishers__icontains=query)
        ).distinct()
    else:
        results = BoardGame.objects.none()

    return render(request, 'boardgames/search_results.html', {'results': results})



# def board_games_list(request):
#     boardgames = BoardGame.objects.all()
#
#     categories1 = set()
#     for boardgame in boardgames:
#         categories = boardgame.categories
#         categories= categories.replace("[","")
#         categories = categories.replace("]", "")
#         categories = categories.replace(" ", "")
#         categories = categories.replace("'", "")
#         categories = categories.split(",")
#         for category in categories:
#             categories1.add(category)
#     # print(categories1)
#
#     return render(request, 'boardgames/board_games_list.html', {'boardgames': boardgames, 'categories': sorted(categories)})


# def boardgame_detail(request, game_id):
#     boardgame = get_object_or_404(BoardGame, pk=game_id)
#     reviews = Review.objects.filter(game=boardgame)
#     community_comments = Community.objects.filter(game=boardgame)
#     guides = Guide.objects.filter(game=boardgame)
#
#     return render(request, 'boardgames/detail.html', {
#         'boardgame': boardgame,
#         'reviews': reviews,
#         'community_comments': community_comments,
#         # 'guides': guides,
#     })
def home(request):
    return render(request, 'boardgames/home.html')
class BoardGameDetailView(DetailView):
    model = BoardGame
    template_name = 'boardgames/detail.html'

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('boardgames:home')

    else:
        form = SignUpForm()
    return render(request, 'boardgames/signup.html', {'form': form})

@login_required
def wishlist(request):
    user = request.user
    wishlist_items = user.wishlist_items.all()
    wishlist_games = [item.game for item in wishlist_items]
    return render(request, 'boardgames/wishlist.html', {'wishlist': wishlist_games})



@login_required
def library(request):
    user = request.user
    library_items = Library.objects.filter(user=user).select_related('game')
    library_games = [item.game for item in library_items]
    return render(request, 'boardgames/library.html', {'library': library_games})




@login_required
def add_to_library(request, pk):
    boardgame = get_object_or_404(BoardGame, pk=pk)
    user = request.user
    library_item, created = Library.objects.get_or_create(user=user, game=boardgame)
    return redirect('boardgames:library')





def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('boardgames:home')
        else:
            error_message = "Invalid login credentials. Please try again."
            return render(request, 'boardgames/login.html', {'error_message': error_message})
    else:
        return render(request, 'boardgames/login.html')



def password_reset_request(request):

    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if email:
                user = UserProfile.objects.get(email=email)
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                domain = request.META['HTTP_HOST']
                protocol = 'https' if request.is_secure() else 'http'
                site_name = "Your Site Name"

                context = {
                    'user': user,
                    'uid': uid,
                    'token': token,
                    'domain': domain,
                    'protocol': protocol,
                    'site_name': site_name
                }

                reset_password_email = render_to_string('boardgames/password_reset_email.html', context)
                print(reset_password_email)
            # try:
            #     send_mail(
            #         'Password Reset Request',
            #         'Here is the message.',
            #         'noreply@myapp.com',
            #         [email],
            #         fail_silently=False,
            #     )
            # except BadHeaderError:
            #     return HttpResponse('Invalid header found.')
            return redirect("boardgames:password_reset_done")
    else:
        form = PasswordResetForm()
    return render(request, "boardgames/password_reset.html", {"form": form})

class PasswordResetDoneCustomView(PasswordResetDoneView):
    template_name = 'boardgames/password_reset_done.html'

class PasswordResetConfirmCustomView(PasswordResetConfirmView):
    template_name = 'boardgames/password_reset_confirm.html'

class PasswordResetCompleteCustomView(PasswordResetCompleteView):
    template_name = 'boardgames/password_reset_complete.html'


@login_required
def add_to_wishlist(request, pk):
    boardgame = get_object_or_404(BoardGame, pk=pk)
    if request.method == 'POST':
        user = request.user
        wishlist_item, created = Wishlist.objects.get_or_create(user=user, game=boardgame)
        if created:
            wishlist_item.save()
        return redirect('boardgames:wishlist')
    return render(request, 'boardgames/detail.html', {'boardgame': boardgame})






