# coding=utf-8
from collections import Counter
from models import Terms, Definitions
from secretballot.models import Vote
import operator


def voted_term(term_id):
    t = Terms.objects.all()
    d = Definitions.objects.all()
    v = Vote.objects.all()

    d_qs = d.filter(Terms=term_id).filter(vote_rank2__gt=0)
    token_list = []
    for i in d_qs:
        v1 = v.filter(object_id=i.id)
        for j in v1:
            token_list.append(j.token)
    token_list = set(token_list)
    obj_id_list = []
    for i in token_list:
        v1 = v.filter(token=i)
        for j in v1:
            obj_id_list.append(j.object_id)

    terms_list = []
    for i in obj_id_list:
        try:
            t1 = t.get(terms_definitions=i)
            terms_list.append(t1)
        except:
            pass
    terms_dict = dict(Counter(terms_list))
    term_tuple_list_sorted = sorted(
        terms_dict.iteritems(), key=operator.itemgetter(1), reverse=True)
    tuple_list = term_tuple_list_sorted[:5]
    obj_list = [i[0] for i in tuple_list]
    return obj_list
