from atom.ext.crispy_forms.forms import BaseTableFormSet
from atom.ext.crispy_forms.views import FormSetMixin
from braces.views import (PrefetchRelatedMixin, SelectRelatedMixin,
                          SetHeadlineMixin, UserFormKwargsMixin)
from cached_property import cached_property
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, UpdateView
from django_filters.views import FilterView
from djmail.template_mail import MagicMailBuilder
from extra_views import (CreateWithInlinesView, InlineFormSet,
                         NamedFormsetsMixin, UpdateWithInlinesView)
from cases.models import Case
from users.utils import PermissionMixin
from .filters import StaffLetterFilter, UserLetterFilter

from .forms import (AddLetterForm, AttachmentForm, LetterForm, NewCaseForm,
                    SendLetterForm)
from .models import Attachment, Letter

REGISTRATION_TEXT = _("User  %(user)s registered! You will receive a password by mail. " +
                      "Log in to get access to archive")


class NewCaseCreateView(SetHeadlineMixin, FormSetMixin, UserFormKwargsMixin, CreateView):
    model = Letter
    form_class = NewCaseForm
    headline = _('Create a new case')
    template_name = 'letters/form_new.html'
    inline_model = Attachment
    inline_form_cls = AttachmentForm

    def formset_valid(self, form, formset, *args, **kwargs):
        formset.save()
        messages.success(self.request,
                         _("Case about {object} created!").format(object=self.object.name))
        if self.request.user.pk != self.object.case.client.pk:
            mail = MagicMailBuilder()

            mail.case_registered(self.object.case.client,
                                 {'case': self.object.case,
                                  'email': self.object.case.from_email},
                                 from_email=self.object.case.from_email).send()
        if self.request.user.is_anonymous():
            messages.success(self.request, _(REGISTRATION_TEXT) % {'user': self.object.created_by})
        return HttpResponseRedirect(self.object.case.get_absolute_url())


class LetterUpdateView(SetHeadlineMixin, FormSetMixin, UserFormKwargsMixin, UpdateView):
    model = Letter
    form_class = LetterForm
    headline = _('Edit')
    template_name = 'letters/form_edit.html'
    inline_model = Attachment
    inline_form_cls = AttachmentForm

    def get_context_data(self, **kwargs):
        context = super(LetterUpdateView, self).get_context_data(**kwargs)
        context['case'] = self.object.case
        return context

    def get_instance(self):
        return self.object

    def get_object(self):
        obj = super(LetterUpdateView, self).get_object()
        if obj.created_by_id == self.request.user.pk:
            obj.case.perm_check(self.request.user, 'can_change_own_record')
        else:
            obj.case.perm_check(self.request.user, 'can_change_all_record')
        return obj

    def get_formset_valid_message(self):
        return ("Letter %(object)s updated!") % {'object': self.object}

    def get_success_url(self):
        return self.object.case.get_absolute_url()

    def notification(self):
        mails = MagicMailBuilder()
        for user in (self.object.case.get_users(filters=self.object.limit_visible_to).
                     exclude(pk=self.request.user)):
            context = {"actor": self.request.user,
                       "letter": self.request.user,
                       "email": self.object.from_email}
            mails.letter_update(user, context,
                                from_email=self.object.case.get_email(self.user)).send()

    def formset_valid(self, form, formset):
        resp = super(LetterUpdateView, self).formset_valid(form, formset)
        self.notification()
        return resp


class LetterListView(PermissionMixin, SelectRelatedMixin, PrefetchRelatedMixin, FilterView):
    @property
    def filterset_class(self):
        return StaffLetterFilter if self.request.user.is_staff else UserLetterFilter

    model = Letter
    paginate_by = 5
    select_related = ['created_by', 'modified_by', 'case']
    prefetch_related = ['attachment_set', ]


class AttachmentInline(InlineFormSet):
    model = Attachment
    formset_class = BaseTableFormSet


class LetterCreateView(NamedFormsetsMixin, LoginRequiredMixin, UserFormKwargsMixin,
                       CreateWithInlinesView):
    model = Letter
    form_class = AddLetterForm
    inlines = [AttachmentInline]
    inlines_names = ['formset', ]
    template_name = 'letters/form_add.html'

    @cached_property
    def case(self):
        obj = get_object_or_404(Case, pk=self.kwargs['case_pk'])
        obj.perm_check(self.request.user, 'can_add_record')
        return obj

    def get_form_kwargs(self, *args, **kwargs):
        kw = super(LetterCreateView, self).get_form_kwargs(*args, **kwargs)
        kw['case'] = self.case
        kw['notify'] = False
        return kw

    def get_context_data(self, **kwargs):
        context = super(LetterCreateView, self).get_context_data(**kwargs)
        context['headline'] = _('Add letter')
        return context

    def forms_valid(self, form, inlines):
        self.object = form.save()
        attachments = inlines[0].save()
        form.notification(self.object, {'attachments': attachments})
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.case.get_absolute_url()


class LetterSendView(LoginRequiredMixin, UserFormKwargsMixin, UpdateView):
    model = Letter
    form_class = SendLetterForm
    template_name = 'letters/form_send.html'

    @cached_property
    def case(self):
        obj = self.object.case
        obj.perm_check(self.request.user, 'can_add_record')
        return obj

    def get_context_data(self, **kwargs):
        context = super(LetterSendView, self).get_context_data(**kwargs)
        context['headline'] = _('Send to client')
        return context

    def get_success_url(self):
        return self.case.get_absolute_url()

    # if letter.status == Letter.STATUS.done:
    #     messages.warning(request, _("It doesn't make sense."))
    #     return HttpResponseRedirect(case.get_absolute_url())
