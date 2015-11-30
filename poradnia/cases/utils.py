from djmail.template_mail import MagicMailBuilder


def notify_update_case_form(name, actor, case, form, is_staff=None, extra_context=None):
    if not form.has_changed():
        return False
    changed_labels = [form.fields[field_name].label for field_name in form.changed_data]
    context = {'case': case,
               'actor': actor,
               'changed_labels': changed_labels}
    context.update(extra_context or {})
    for user in case.get_users_with_perms(is_staff=is_staff):
        getattr(MagicMailBuilder(), name)(user,
                                          from_email=case.get_email(actor),
                                          context=context).send()
    return True
