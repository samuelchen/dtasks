#!/usr/bin/env python
# coding: utf-8
__author__ = 'Samuel Chen <samuel.net@gmail.com>'
__date__ = '11/16/2017 10:19 PM'

'''
Network IO tasks

Created on 11/16/2017
'''

from celery import shared_task
import os
import logging
import requests

log = logging.getLogger(__name__)


@shared_task(bind=True)
def download(self, url, filename=None, folder='./', delete_if_exists=True):
    """
    Download a media file asynchronously
    If file_field specified, argument 'folder' will be IGNORED. Will use 'file_field.field.upload_to'.
    :return:
    """
    log.debug('Request: {0!r}'.format(self.request))

    rc = None
    # downloading_set = SocialClient.get_downloading_set()
    # if url in downloading_set:
    #     log.info('[IGNORED] %s is in downloading.' % url)
    #     return rc
    # else:
    #     downloading_set.add(url)

    if not filename:
        filename = url.split('/')[-1]

    try:

        fullpath = os.path.join(self.download_root, folder, filename)
        fullpath = os.path.abspath(fullpath)
        os.makedirs(os.path.dirname(fullpath), exist_ok=True)
        rc = fullpath

        # TODO: handle BIG file
        log.debug('Downloading %s to %s' % (url, fullpath))
        r = requests.get(url, stream=True, proxies=self.proxies)
        if r.status_code != requests.codes.ok:
            log.error('%d %s. Downloading %s' % (r.status_code, r.reason, url))
            rc = None

        if delete_if_exists:
            if os.path.exists(fullpath):
                try:
                    os.remove(fullpath)
                except Exception as err:
                    log.exception(err)
                    # then will auto rename

        try:
            with open(fullpath, 'wb') as f:
                f.write(r.raw)
        except Exception as err:
            log.exception(err)
            try:
                if os.path.exists(fullpath):
                    os.remove(fullpath)
            except Exception as err1:
                log.error(str(err1))
            rc = None
    except Exception as err:
        log.exception(err)
        rc = None
    finally:
        pass

    return rc