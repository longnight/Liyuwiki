#coding=utf-8
from models import Terms, Definitions
import simplejson as json
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime


def api(request):
    if request.method == 'POST':
        return HttpResponse(json.dumps({"error":"sorry, post method not yet ready"}),\
         content_type="application/json", status=404)

    api_dict = {
    "collection" : {
    "href" : "http://liyuwiki.com/api/v1/",
    "terms" : [],
    "add_term_template" : {
        "term" : "",
        "definition" : "",
        "author" : "",
        "author_email" : "",
        "homepage" : ""
            }
        }
    }

    t = Terms.objects.order_by('-id').filter(terms_definitions__show=True).distinct()    
    for i in t[:10]:
        term_dict = {}
        term_dict['term'] = i.term
        term_dict['href'] = 'http://liyuwiki.com/api/v1/term/' + str(i.uid)
        api_dict['collection']['terms'].append(term_dict)
    return HttpResponse(json.dumps(api_dict, indent=4*' '),\
     content_type="application/json", status=200)

def api_term(request, term_uid):
    term_dict = {
    "term" : "",
    "href" : "",
    "uid" : "",
    "term_pinyin" : "",
    "created_time": "",
    "visit_times" : "",
    "definitions" : [],
    "add_definition_template" : {
        "definition" : "",
        "author" : "",
        "author_email" : "",
        "homepage" : "",
        }
    }

    t = Terms.objects.all().filter(terms_definitions__show=True).distinct()
    try:
        term = t.get(uid=term_uid)
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({"error":"no this term"}),\
         content_type="application/json", status=404)

    term_dict['term'] = term.term
    term_dict['uid'] = term_uid
    term_dict['href'] = 'http://liyuwiki.com/api/v1/term/' + term_uid
    term_dict['term_pinyin'] = term.term_pinyin
    term_dict['created_time'] = term.created_time.isoformat()
    term_dict['visit_times'] = term.visit_times    

    definition = Definitions.objects.all().filter(show=True)
    deflist = definition.filter(Terms_id=term.id).order_by('-vote_rank2', 'created_time')

    for i in deflist:
        def_dict = {}
        def_dict['author'] = i.author
        def_dict['definition'] = i.definition
        def_dict['created_time'] = i.created_time.isoformat()
        def_dict['homepage'] = i.homepage
        def_dict['score'] = i.vote_rank2
        def_dict['up_vote'] = i.total_upvotes
        def_dict['down_vote'] = i.total_downvotes
        def_dict['img_url'] = str(i.docfile)

        term_dict['definitions'].append(def_dict)
    return HttpResponse(json.dumps(term_dict, indent=4*' '),\
     content_type="application/json", status=200)



