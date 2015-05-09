# coding=utf-8
import datetime


from django.core.mail import send_mass_mail


def d_pass(d_uid, d_author_email, content1, content2):
    subject = u'您提交的内容已经发布了! '
    time = unicode(datetime.datetime.now())
    url = u"俚语维基， http://liyuwiki.com"
    message = u'恭喜您，您提交的内容已经发布在俚语维基网站上: ' + u"\n"*2 + content1 \
              + u"\n" + content2 + u"\n" + time + u"\n" + url
    from_email = 'liyuwiki_notice@liyuwiki.com'
    recipient_list = [d_author_email]
    message1 = (subject, message, from_email, recipient_list)
    send_mass_mail((message1,), fail_silently=False)


def d_del(d_uid, d_author_email, content1, content2):
    subject = u'Sorry,您提交的内容不被接受'
    time = unicode(datetime.datetime.now())
    url = u"俚语维基， http://liyuwiki.com"
    message = u'俚语维基没有接受您刚刚提交的内容: ' + u"\n"*2 + content1 + u"\n" \
              + content2 + u"\n" + \
              u"建议您先了解本站的投递指导 \n" + time + u"\n" + url
    from_email = 'liyuwiki_notice@liyuwiki.com'
    recipient_list = [d_author_email]
    message1 = (subject, message, from_email, recipient_list)
    send_mass_mail((message1,), fail_silently=False)


def new_term_msg(t, d, name, hp, mail):
    subject = u'【新条目】有人提交了新的条目!'
    message = t_msg(t, d, name, hp, mail)
    from_email = 'liyuwiki_notice@liyuwiki.com'
    recipient_list = ['admin@liyuwiki.com']
    # if mail:    # if want send a email to author, uncomment this two.
    #     recipient_list.append(mail)
    message1 = (subject, message, from_email, recipient_list)
    send_mass_mail((message1,), fail_silently=False)


def t_msg(t, d, name, hp, mail):
    msg_head = u"\n"
    msg_end = u"\n"
    if not name:
        name = u'匿名网友'
    if not hp:
        hp = u'未留下网址.'
    if not mail:
        mail = u'未留下邮箱.'
    msg1 = name + u' 贡献了一个新条目:\n' + t + u"\n" * 2
    msg2 = u"条目的定义是: \n" + d + u"\n" * 2
    msg3 = u"他的网址: \n" + hp + u"\n" * 2
    msg4 = u"他的邮箱: \n" + mail + u"\n" * 2
    return msg_head + msg1 + msg2 + msg3 + msg4 + msg_end


def new_d_msg(t, d, name, hp, mail):
    subject = u'【新释义】有人提交了新的释义!'
    message = d_msg(t, d, name, hp, mail)
    from_email = 'liyuwiki_notice@liyuwiki.com'
    recipient_list = ['admin@liyuwiki.com']
    message1 = (subject, message, from_email, recipient_list)
    send_mass_mail((message1,), fail_silently=False)


def d_msg(t, d, name, hp, mail):
    msg_head = u"\n"
    msg_end = u"\n"
    if not name:
        name = u'匿名网友'
    if not hp:
        hp = u'未留下网址.'
    if not mail:
        mail = u'未留下邮箱.'
    msg1 = name + u' 提交了1个新的释义。条目是: ' + t + ":" + u"\n" * 2
    msg2 = u"他提交的内容: \n" + d + u"\n" * 2
    msg3 = u"他的网址: \n" + hp + u"\n" * 2
    msg4 = u"他的邮箱: \n" + mail + u"\n" * 2
    return msg_head + msg1 + msg2 + msg3 + msg4 + msg_end
