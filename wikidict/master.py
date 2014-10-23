#coding=utf-8
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from models import *
from tasks import *
from main.private_settings import backend_url

@login_required()
def master_index(request):
    rc = RequestContext(request)
    d = Definitions.objects.all()
    deflist = d.order_by('-created_time')[:50]
    context = {'deflist': deflist}
    return render_to_response('master.html', context, rc)

@login_required
def master_del_t(request, t_uid):
    t = Terms.objects.all().get(uid=t_uid)
    deflist = Definitions.objects.filter(Terms=t.id)
    deflist.delete()
    t.delete()
    return HttpResponseRedirect(backend_url)

@login_required
def master_pass_d(request, d_uid):
    d = Definitions.objects.all().get(uid=d_uid)
    d.show = True
    d.save()
    update_db.delay()
    return HttpResponseRedirect(backend_url)

@login_required
def master_pass_d_send(request, d_uid):
    d = Definitions.objects.all().get(uid=d_uid)
    d.show = True
    d.save()
    user_pass.delay(d_uid, d.author_email, d.Terms.term, d.definition)
    update_db.delay()
    return HttpResponseRedirect(backend_url)

@login_required
def master_del_d(request, d_uid):
    d = Definitions.objects.all()
    bad_d = d.get(uid=d_uid)
    bad_d.delete()
    # update_db.delay()
    return HttpResponseRedirect(backend_url)

@login_required
def master_del_d_send(request, d_uid):
    d = Definitions.objects.all()
    bad_d = d.get(uid=d_uid)
    user_del.delay(d_uid, bad_d.author_email, bad_d.Terms.term, bad_d.definition)
    bad_d.delete()
    # update_db.delay()
    return HttpResponseRedirect(backend_url)






