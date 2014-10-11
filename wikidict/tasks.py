#coding=utf-8

from __future__ import absolute_import
from celery import shared_task, Celery, platforms
from django.core.mail import send_mass_mail
from haystack.management.commands import update_index
from .email import new_term_msg, new_d_msg, d_pass, d_del
from time import sleep


app2 = Celery('tasks', backend='amqp', broker='amqp://')

platforms.C_FORCE_ROOT = True

@app2.task
def user_pass(d_uid, d_author_email, content1, content2):
    return d_pass(d_uid, d_author_email, content1, content2)


@app2.task
def user_del(d_uid, d_author_email, content1, content2):
    return d_del(d_uid, d_author_email, content1, content2)


@app2.task
def send_t(t, d, name, hp, mail):
    sleep(2)
    return new_term_msg(t, d, name, hp, mail)


@app2.task
def send_d(t, d, name, hp, mail):
    sleep(2)
    return new_d_msg(t, d, name, hp, mail)


@shared_task
def update_db():
    sleep(10)
    return update_index.Command().handle()

