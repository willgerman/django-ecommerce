from organization.models import Category

def get_categories(request):
    global_categories = Category.objects.all()

    return {
        "GlobalCategories": global_categories
    }


