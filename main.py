#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from datetime import datetime
import json
from google.appengine.api import urlfetch


def unix_time(dt):
    epoch = datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()

list_url = "https://slack.com/api/channels.list?token=XXXXXXXX"
bot_url = "https://tokbox.slack.com/services/hooks/slackbot?token=YYYYYYYY&channel=%23new-channels"

class MainHandler(webapp2.RequestHandler):
    def get(self):
        result = urlfetch.fetch(list_url)

        if result.status_code != 200:
            self.error(result.status_code)

        channels = json.loads(result.content).get('channels', [])
        for channel in channels:
            age_mins = (unix_time(datetime.utcnow()) - channel['created']) / (60)

            if age_mins < 5:
                urlfetch.fetch(url=bot_url,
                               payload="@channel New channel created #" + channel['name'],
                               method=urlfetch.POST)

        self.response.write('ok')


app = webapp2.WSGIApplication([
    ('/tasks/summary', MainHandler)
], debug=True)
