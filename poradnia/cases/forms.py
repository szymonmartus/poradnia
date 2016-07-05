# -*- coding: utf-8 -*-
import autocomplete_light.shortcuts as autocomplete_light
from atom.ext.crispy_forms.forms import (FormHorizontalMixin, HelperMixin,
                                         SingleButtonMixin)
from braces.forms import UserKwargModelFormMixin
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from djmail.template_mail import MagicMailBuilder
from guardian.shortcuts import assign_perm

from .models import Case, PermissionGroup


class CaseForm(UserKwargModelFormMixin, FormHorizontalMixin, SingleButtonMixin,
               forms.ModelForm):

    def changed_data_labels(self):
        return [self.fields[key].label for key in self.changed_data]

    def _process_new(self):
        # Update object
        self.instance.created_by = self.user

        # Send notification
        mails = MagicMailBuilder()
        context = {"actor": self.user,
                   "case": self.instance,
                   "changed_labels": self.changed_data_labels()}
        for user in self.instance.get_users_with_perms(is_staff=True).all():
            mails.case_new(user, context,
                           from_email=self.instance.get_email(self.user)).send()

    def _process_update(self):
        # Send notification
        self.instance.modified_by = self.user

        # Update object
        mails = MagicMailBuilder()
        context = {"actor": self.user,
                   "case": self.instance,
                   "changed_labels": self.changed_data_labels()}
        for user in self.instance.get_users_with_perms(is_staff=True).all():
            mails.case_update(user, context,
                              from_email=self.instance.get_email(self.user)).send()

    def save(self, commit=True, *args, **kwargs):
        is_new = self.instance.pk is None
        super(CaseForm, self).save(*args, **kwargs)
        if is_new:  # old
            self._process_new()
        else:  # new
            self._process_update()
        return self.instance

    class Meta:
        model = Case
        fields = ("name", "status", "has_project")


class CaseGroupPermissionForm(HelperMixin, forms.Form):
    action_text = _('Grant')
    user = forms.ModelChoiceField(queryset=None,
                                  required=True,
                                  widget=autocomplete_light.ChoiceWidget('UserAutocomplete'),
                                  label=_("User"))
    group = forms.ModelChoiceField(queryset=PermissionGroup.objects.all(),
                                   label=_("Permissions group"))

    def __init__(self, *args, **kwargs):
        self.case = kwargs.pop('case')
        self.user = kwargs.pop('user')
        super(CaseGroupPermissionForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = get_user_model().objects.for_user(self.user)
        self.helper.form_class = 'form-inline'
        self.helper.layout.append(Submit('grant', _('Grant')))

        self.helper.form_action = reverse('cases:permission_grant',
                                          kwargs={'pk': str(self.case.pk)})

    def assign(self):
        perms = [x.codename for x in self.cleaned_data['group'].permissions.all()]

        for perm in perms:
            assign_perm(perm, self.cleaned_data['user'], self.case)

        self.case.send_notification(actor=self.user,
                                    verb='grant_group',
                                    action_object=self.cleaned_data['user'],
                                    action_target=self.cleaned_data['group'],
                                    staff=True)


class CaseCloseForm(UserKwargModelFormMixin, HelperMixin, forms.ModelForm):
    notify = forms.BooleanField(required=False, label=_("Notify user"))

    def __init__(self, *args, **kwargs):
        super(CaseCloseForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('action', _('Close'), css_class="btn-primary"))

        if 'instance' in kwargs:
            self.helper.form_action = kwargs['instance'].get_close_url()
        self.instance.modified_by = self.user
        self.instance.status = Case.STATUS.closed

    def save(self, *args, **kwargs):
        if self.cleaned_data['notify']:
            mails = MagicMailBuilder()
            context = {"actor": self.user, 'case': self.instance}
            for user in self.instance.get_users_with_perms():
                mails.case_close(user, context).send()
        return super(CaseCloseForm, self).save(*args, **kwargs)

    class Meta:
        model = Case
        fields = ()
