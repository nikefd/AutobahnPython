###############################################################################
##
# Copyright (C) 2014 Tavendo GmbH
##
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
##
# http://www.apache.org/licenses/LICENSE-2.0
##
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##
###############################################################################

from twisted.internet.defer import inlineCallbacks

from autobahn.wamp.types import RegisterOptions, PublishOptions
from autobahn.twisted.wamp import ApplicationSession


class Component(ApplicationSession):

    """
    An application component providing procedures with
    different kinds of arguments.
    """

    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")

        def square(val, details=None):
            print("square called from: {}".format(details.caller))

            if val < 0:
                self.publish('com.myapp.square_on_nonpositive', val)
            elif val == 0:
                if details.caller:
                    options = PublishOptions(exclude=[details.caller])
                else:
                    options = None
                self.publish('com.myapp.square_on_nonpositive', val, options=options)
            return val * val

        yield self.register(square, 'com.myapp.square', RegisterOptions(details_arg='details'))

        print("procedure registered")


if __name__ == '__main__':
    from autobahn.twisted.wamp import ApplicationRunner
    runner = ApplicationRunner("ws://127.0.0.1:8080/ws", "realm1")
    runner.run(Component)
