from django.http import JsonResponse


def googleAuth(request):
    # user = User.objects.get()
    return JsonResponse({'provider': 'Google'})
