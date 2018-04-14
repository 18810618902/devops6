from django import template

register = template.Library()

@register.filter(name='userlist_str2')
def userlist_str2(user_list):
    if len(user_list) < 3:
        return ' '.join([user.name_cn for user in user_list[0:2]])
    else:
        return '%s ...' % ' '.join([user.name_cn for user in user_list[0:2]])

@register.filter(name='group_str2')
def group_str2(group_list):
    if len(group_list) < 3:
        return ' '.join([group.name for group in group_list[0:2]])
    else:
        return '%s ...' % ' '.join([group.name for group in group_list[0:2]])