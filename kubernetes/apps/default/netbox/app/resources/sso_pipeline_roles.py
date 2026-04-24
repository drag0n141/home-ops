from netbox.authentication import Group

class AuthFailed(Exception):
    pass

def add_groups(response, user, backend, *args, **kwargs):
    try:
        groups = response['groups']
    except KeyError:
        pass
    for group in groups:
        group, created = Group.objects.get_or_create(name=group)
        user.groups.add(group)

def remove_groups(response, user, backend, *args, **kwargs):
    try:
        groups = response['groups']
    except KeyError:
        user.groups.clear()
        pass
    user_groups = [item.name for item in user.groups.all()]
    delete_groups = list(set(user_groups) - set(groups))
    for delete_group in delete_groups:
        group = Group.objects.get(name=delete_group)
        user.groups.remove(group)

def set_roles(response, user, backend, *args, **kwargs):
    user.is_superuser = False
    user.is_staff = False
    try:
        groups = response['groups']
    except KeyError:
        user.save()
        pass
    user.is_superuser = True if 'ID-Admin' in groups else False
    user.is_staff = True if 'ID-Netbox' in groups else False
    user.save()
