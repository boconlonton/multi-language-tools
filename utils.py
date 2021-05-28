from screen.models import Screen
from project.models import Project


def get_or_none(class_model, **kwargs):
    """Return object if exists, otherwise None"""
    try:
        return class_model.objects.get(**kwargs)
    except class_model.DoesNotExist:
        return None


def create_screen_from_code_only(**kwargs):
    """Create screen object with screen code only"""
    screen_code = kwargs['screen_code']
    screen_code_split = screen_code.split('_')
    screen_name = " ".join(
        word.capitalize()
        for word in screen_code_split
    )
    project_pms = Project.objects.filter(project_name__icontains='pms')
    screen = Screen.objects.create(
        screen_code=kwargs['screen_code'],
        screen_name=screen_name,
        project=project_pms,
        modified_by=kwargs['user'],
        created_by=kwargs['user']
    )
    return screen
