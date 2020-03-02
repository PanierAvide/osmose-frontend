#! /usr/bin/env python
#-*- coding: utf-8 -*-
###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2009                       ##
##                                                                       ##
## This program is free software: you can redistribute it and/or modify  ##
## it under the terms of the GNU General Public License as published by  ##
## the Free Software Foundation, either version 3 of the License, or     ##
## (at your option) any later version.                                   ##
##                                                                       ##
## This program is distributed in the hope that it will be useful,       ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of        ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         ##
## GNU General Public License for more details.                          ##
##                                                                       ##
## You should have received a copy of the GNU General Public License     ##
## along with this program.  If not, see <http://www.gnu.org/licenses/>. ##
##                                                                       ##
###########################################################################

from bottle import route, template
from tools import utils

from api_issue import _get, _expand_tags, t2l


@route('/error/<uuid:uuid>')
def display(db, lang, user, uuid):
    marker = _get(db, uuid=uuid)

    data_type = { 'N': 'node', 'W': 'way', 'R': 'relation', 'I': 'infos'}

    for e in marker['elems'] or []:
        e['tags'] = _expand_tags(e.get('tags', {}), t2l.checkTags(e.get('tags', {})))

    for fix_group in marker['fixes'] or []:
        for f in fix_group:
            f['create'] = _expand_tags(f['create'], t2l.checkTags(f['create']))
            f['modify'] = _expand_tags(f['modify'], t2l.checkTags(f['modify']))
            f['delete'] = _expand_tags(f['delete'], {}, True)

    return template(
        'error/index',
        translate=utils.translator(lang),
        uuid=uuid,
        marker=marker,
        user=user,
        main_website=utils.main_website,
        data_type=data_type,
    )
