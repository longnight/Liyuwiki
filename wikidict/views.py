# coding=utf-8
from django.core.exceptions import ObjectDoesNotExist
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from models import Terms, Definitions
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from secretballot.middleware import (
    SecretBallotIpUseragentMiddleware)  # , SecretBallotMiddleware)
from secretballot.models import Vote
from script import (
    term_uid, definition_uid, confidence, term_pinyin,
    query_previous, query_next
    )
from script2 import voted_term
from forms import TermForm, DefinitionForm, SearchForm2
# from haystack.views import SearchView
# from haystack.management.commands import update_index
from datetime import datetime
import random
from django.db import IntegrityError
from tasks import send_t, send_d  # , update_db
# from django import forms
from collections import deque
from django.core.cache import get_cache
from main.settings import DEBUG
# from django.utils.encoding import force_str
is_online = not DEBUG
contributor = False


def index(request):

    contributor = request.session.get('contributor', False)
    sform = SearchForm2()
    rc = RequestContext(request)

    termlist = Terms.objects.all().filter(
        terms_definitions__show=True).distinct()
    # termlist = Terms.objects.all().filter(
    #     terms_definitions__show=True).order_by(
    #     'terms_definitions__created_time').distinct()

    if contributor:
        termlist = Terms.objects.all().distinct()

    d = Definitions.objects.all().filter(show=True)
    if contributor:
        d = Definitions.objects.all()

    anonymous_count = d.filter(author='').count()
    author_count = d.values('author').distinct().count() + anonymous_count
    terms_count = termlist.count()
    defs_count = d.count()
    latest_created = termlist.order_by('-id')[:10]
    latest_voted = termlist.order_by('-modified_time')[:10]
    context = {'sform': sform,
               'latest_created': latest_created,
               'latest_voted': latest_voted,
               'author_count': author_count, 'terms_count': terms_count,
               'defs_count': defs_count,
               'anonymous_count': anonymous_count, 'is_online': is_online}
    return render_to_response('index.html', context, rc)


def detail(request, term_uid):

    contributor = request.session.get('contributor', False)
    rc = RequestContext(request)

    t = Terms.objects.all().filter(terms_definitions__show=True).distinct()
    if contributor:
        t = Terms.objects.all().distinct()

    try:
        term = t.get(uid=term_uid)
    except ObjectDoesNotExist:
        return HttpResponseRedirect('/404.html')

    definition = Definitions.objects.all().filter(show=True)
    if contributor:
        definition = Definitions.objects.all()

    deflist = definition.filter(
        Terms_id=term.id).order_by('-vote_rank2', 'created_time')

    the_cache = get_cache('cache2')

    related_terms_cache = the_cache.get((str(term_uid) + '_' + 'related'))
    if related_terms_cache is None:
        related_terms = []
        for defs in definition:
            if term.term in defs.definition:
                try:
                    r_t = t.exclude(uid=term_uid).get(terms_definitions=defs)
                    related_terms.append(r_t)
                except ObjectDoesNotExist:
                    pass
        for defs in deflist:
            for terms in t.exclude(uid=term_uid):
                if terms.term in defs.definition:
                    related_terms.append(terms)
        related_terms = set(related_terms)
        if related_terms:
            the_cache.set(
                (str(term_uid) + '_' + 'related'), related_terms, 60 * 60 * 12)
        else:
            the_cache.set(
                (str(term_uid) + '_' + 'related'), 'no_related', 60 * 60 * 12)
    elif related_terms_cache == 'no_related':
        related_terms = []
    else:
        related_terms = related_terms_cache

    recent_kw = the_cache.get('recent_kw', deque([], 80))

    dictlist = t.order_by('term_pinyin', 'id')
    previouslist = query_previous(dictlist, term)
    nextlist = query_next(dictlist, term)
    latest_vote = t.order_by('-modified_time')[:10]

    visited_rank_cache = the_cache.get('visited_rank')
    if visited_rank_cache is None:
        visited_rank = t.order_by('-visit_times')[:10]
        the_cache.set('visited_rank', visited_rank, 60 * 60 * 24)
    else:
        visited_rank = visited_rank_cache

    score_rank_cache = the_cache.get('score_rank')
    if score_rank_cache is None:
        score_rank = definition.order_by('-vote_rank2')[:10]
        the_cache.set('score_rank', score_rank, 60 * 60 * 24)
    else:
        score_rank = score_rank_cache

    sform = SearchForm2()

    term.visit_times += 1
    term.save()

    also_voted_term_cache = the_cache.get((str(term_uid) + '_' + 'also_voted'))
    if also_voted_term_cache is None:
        v_t = voted_term(term.id)
        if term in v_t:
            v_t.remove(term)
        if v_t:
            the_cache.set(
                (str(term_uid) + '_' + 'also_voted'), v_t, 60 * 60 * 2)
        else:
            the_cache.set(
                (str(term_uid) + '_' + 'also_voted'), 'non', 60 * 60 * 2)
    elif also_voted_term_cache == 'non':
        v_t = []
    else:
        v_t = also_voted_term_cache

    context = {'related_terms': related_terms,
               'deflist': deflist, 'sform': sform, 'term': term,
               'previouslist': previouslist, 'recent_kw': list(recent_kw),
               'nextlist': nextlist, 'visited_rank': visited_rank,
               'score_rank': score_rank,
               'latest_vote': latest_vote, 'v_t': v_t, 'is_online': is_online}
    return render_to_response('detail.html', context, rc)


def detail_single(request, t_uid, d_uid):
    contributor = request.session.get('contributor', False)

    rc = RequestContext(request)

    t = Terms.objects.all().filter(terms_definitions__show=True).distinct()
    if contributor:
        t = Terms.objects.all().distinct()

    term = t.get(uid=t_uid)

    d = Definitions.objects.all().filter(show=True)
    if contributor:
        d = Definitions.objects.all()

    latest_vote = t.order_by('-modified_time')[:8]
    visited_rank = t.order_by('-visit_times')[:8]
    score_rank = d.order_by('-vote_rank2')[:8]
    definition = d.get(uid=d_uid)
    sform = SearchForm2()
    context = {'term': term,
               'sform': sform, 'definition': definition,
               'visited_rank': visited_rank,
               'score_rank': score_rank,
               'latest_vote': latest_vote, 'is_online': is_online}
    return render_to_response('detail_single.html', context, rc)


def add_term(request):
    sform = SearchForm2()
    desc = None
    if request.method == 'POST':
        form = TermForm(request.POST, request.FILES)
        if form.is_valid():
            raw_term = form.cleaned_data['term']
            raw_term = ' '.join(raw_term.split())
            raw_term_pinyin = term_pinyin(raw_term)
            clean_term_pinyin = ' '.join(raw_term_pinyin.split())
            t = Terms(term=raw_term,
                      term_pinyin=clean_term_pinyin,
                      uid=term_uid())
            try:
                t.save()
            except IntegrityError:
                return HttpResponse(u'词条已经存在!')
            request.session['new_add_term'] = t.term
            request.session['new_add_term_uid'] = t.uid
            d = Definitions(Terms_id=t.id,
                            definition=form.cleaned_data['definition'],
                            homepage=form.cleaned_data['homepage'],
                            author_email=form.cleaned_data['author_email'],
                            author=form.cleaned_data['author'],
                            uid=definition_uid(),
                            docfile=form.cleaned_data['docfile'])
            d.save()

            request.session['contributor'] = True
            request.session['has_thanked'] = False
            request.session['author'] = form.cleaned_data['author']
            request.session['author_email'] = form.cleaned_data['author_email']
            request.session['homepage'] = form.cleaned_data['homepage']
            request.session.set_expiry(60 * 30)

            if is_online:
                send_t.delay(
                    t.term, d.definition, d.author, d.homepage, d.author_email)
            return HttpResponseRedirect('/thanks.html')
    else:
        form = TermForm(
            initial={'author': request.session.get('author', None),
                     'author_email': request.session.get('author_email', None),
                     'homepage': request.session.get('homepage', None)})
    c = {'form': form, 'sform': sform}
    c.update(csrf(request))
    return render_to_response(
        'add_term.html',
        {'form': form, 'sform': sform, 'desc': desc, 'is_online': is_online},
        context_instance=RequestContext(request))


def add_search_term(request, search_term):
    sform = SearchForm2()
    desc = None
    if request.method == 'POST':
        form = TermForm(request.POST, request.FILES)
        if form.is_valid():
            raw_term = form.cleaned_data['term']
            raw_term = ' '.join(raw_term.split())
            raw_term_pinyin = term_pinyin(raw_term)
            clean_term_pinyin = ' '.join(raw_term_pinyin.split())
            t = Terms(term=raw_term,
                      term_pinyin=clean_term_pinyin,
                      uid=term_uid())
            try:
                t.save()
            except IntegrityError:
                return HttpResponse(u'词条已经存在!')
            request.session['new_add_term'] = t.term
            request.session['new_add_term_uid'] = t.uid
            import pdb
            pdb.set_trace()
            d = Definitions(Terms_id=t.id,
                            definition=definition_compact,
                            homepage=form.cleaned_data['homepage'],
                            author_email=form.cleaned_data['author_email'],
                            author=form.cleaned_data['author'],
                            uid=definition_uid(),
                            docfile=form.cleaned_data['docfile'])
            d.save()

            request.session['contributor'] = True
            request.session['has_thanked'] = False
            request.session['author'] = form.cleaned_data['author']
            request.session['author_email'] = form.cleaned_data['author_email']
            request.session['homepage'] = form.cleaned_data['homepage']
            request.session.set_expiry(60 * 30)

            if is_online:
                send_t.delay(
                    t.term, d.definition, d.author, d.homepage, d.author_email)
            return HttpResponseRedirect('/thanks.html')
    else:
        form = TermForm(
            initial={'term': search_term,
                     'author': request.session.get('author', None),
                     'author_email': request.session.get('author_email', None),
                     'homepage': request.session.get('homepage', None)})

        desc = search_term
    c = {'form': form, 'sform': sform}
    c.update(csrf(request))
    return render_to_response(
        'add_term.html',
        {'form': form, 'sform': sform, 'desc': desc, 'is_online': is_online},
        context_instance=RequestContext(request))


def add_def(request, term_uid):
    try:
        Terms.objects.get(uid=term_uid)
    except ObjectDoesNotExist:
        return HttpResponse(u'词条不存在 !')
    sform = SearchForm2()
    t = Terms.objects.get(uid=term_uid)
    if request.method == 'POST':
        form = DefinitionForm(request.POST, request.FILES)
        if form.is_valid():
            d = Definitions(Terms_id=t.id,
                            definition=form.cleaned_data['definition'],
                            homepage=form.cleaned_data['homepage'],
                            author_email=form.cleaned_data['author_email'],
                            author=form.cleaned_data['author'],
                            uid=definition_uid(),
                            docfile=form.cleaned_data['docfile'])
            d.save()
            request.session['new_add_term'] = t.term
            request.session['new_add_term_uid'] = t.uid
            request.session['contributor'] = True
            request.session['has_thanked'] = False
            request.session['author'] = form.cleaned_data['author']
            request.session['author_email'] = form.cleaned_data['author_email']
            request.session['homepage'] = form.cleaned_data['homepage']
            request.session.set_expiry(60 * 30)

            if is_online:
                send_d.delay(
                    t.term, d.definition, d.author, d.homepage, d.author_email)
            return HttpResponseRedirect('/thanks.html')
    else:
        form = DefinitionForm(
            initial={'author': request.session.get('author', None),
                     'author_email': request.session.get('author_email', None),
                     'homepage': request.session.get('homepage', None)}
            )
    return render_to_response(
        'add_def.html',
        {'form': form, 'sform': sform, 'term': t, 'is_online': is_online},
        context_instance=RequestContext(request)
        )


def add_vote(request, term_uid, def_uid):
    contributor = request.session.get('contributor', False)
    # rc = RequestContext(request)
    if contributor:
        definition = Definitions.objects.get(uid=def_uid)
    else:
        definition = Definitions.objects.filter(show=True).get(uid=def_uid)
    sb = SecretBallotIpUseragentMiddleware()
    tok = sb.generate_token(request)
    definition.add_vote(tok, '+1')
    v = Vote.objects.filter(object_id=definition.id)
    ups = v.filter(vote=1).count()
    downs = v.filter(vote=-1).count()
    rank2 = confidence(ups, downs)
    definition.vote_rank2 = rank2
    # definition.modified_time = datetime.now()
    definition.save()
    t = Terms.objects.get(uid=term_uid)
    t.modified_time = datetime.now()
    t.save()
    target = "/" + str(term_uid) + '.html'
    return HttpResponseRedirect(target)


def sub_vote(request, term_uid, def_uid):
    contributor = request.session.get('contributor', False)
    # rc = RequestContext(request)
    if contributor:
        definition = Definitions.objects.get(uid=def_uid)
    else:
        definition = Definitions.objects.filter(show=True).get(uid=def_uid)
    sb = SecretBallotIpUseragentMiddleware()
    tok = sb.generate_token(request)
    definition.add_vote(tok, '-1')
    v = Vote.objects.filter(object_id=definition.id)
    ups = v.filter(vote=1).count()
    downs = v.filter(vote=-1).count()
    rank2 = confidence(ups, downs)
    definition.vote_rank2 = rank2
    definition.save()
    t = Terms.objects.get(uid=term_uid)
    t.modified_time = datetime.now()
    t.save()
    target = "/" + str(term_uid) + '.html'
    return HttpResponseRedirect(target)


def randomview(request):
    contributor = request.session.get('contributor', False)
    t = Terms.objects.all().filter(terms_definitions__show=True)
    if contributor:
        t = Terms.objects.all()
    # uncomment this line can keep the lef side list from too short:
    # t = t.order_by('term_pinyin')[:len(t)-15]
    term = random.choice(t)
    return HttpResponseRedirect('/%s.html?from=random' % term.uid)


def thanks(request):
    rc = RequestContext(request)
    contributor = request.session.get('contributor', None)
    if not contributor:
        raise Http404()
    has_thanked = request.session.get('has_thanked', None)
    if has_thanked:
        raise Http404()
    request.session['has_thanked'] = True
    new_add_term = request.session.get('new_add_term', None)
    new_add_term_uid = request.session.get('new_add_term_uid', None)
    context = {'new_add_term': new_add_term,
               'new_add_term_uid': new_add_term_uid}
    return render_to_response('thanks.html', context, rc)
