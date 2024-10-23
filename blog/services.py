from django.views.decorators.cache import cache_page
from config.settings import CACHED_ENABLED

def set_cache_controller(controller):
    """
    Кэширование контроллера
    :param controller: контроллер Controller.as_view()
    """
    if CACHED_ENABLED:
        return cache_page(200)(controller)
    return controller