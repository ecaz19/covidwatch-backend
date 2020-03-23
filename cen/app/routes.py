from flask import Blueprint, request
from app.models import CEN
from datetime import datetime
cens_blueprint = Blueprint('cens', __name__)
from config import CEN_LENGTH, API_VERSION
from typing import List
import json

PREFIX = "/api/v" + API_VERSION + '/cens'


@cens_blueprint.route(PREFIX + '/', methods=['GET', 'POST'])
def cens():
  if request.method == 'GET':
    since: str = request.args.get('since')
    if since is None:
      return ({
          'msg':
              'Missing ?since=<datetime> (utc datetime, i.e. "2020-03-22 16:40:31.989538"'
      }, 400)
    cens = CEN.query.filter(CEN.created >= since).all()
    return ({'cens': [cen.to_json() for cen in cens]}, 200)

  elif request.method == 'POST':
    cens: List[str] = request.args.get('cens')
    if cens is None:
      return ({
          'msg':
              'Missing ?cens=<cen>, <cen>, ... (comma separated list of strings)'
      }, 400)
    cens = cens.split(',')
    print(cens)
    for cen in cens:
      if len(cen) != CEN_LENGTH:
        return ({
            'msg': f'cen {cen} is not of expected length {CEN_LENGTH}'
        }, 400)
      cen = CEN(uuid=cen)
      cen.save()
    return ('', 201)