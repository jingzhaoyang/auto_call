#/usr/bin/python

from application.notification import NotificationCenter
from sipsimple.account import AccountManager
from sipsimple.application import SIPApplication
from sipsimple.core import SIPURI, ToHeader
from sipsimple.lookup import DNSLookup, DNSLookupError
from sipsimple.storage import FileStorage
from sipsimple.session import Session
from sipsimple.streams import AudioStream
from sipsimple.configuration.settings import SIPSimpleSettings
from sipsimple.threading.green import run_in_green_thread
from sipsimple.audio import WavePlayer
from threading import Event

class SimpleCallApplication(SIPApplication):

    def __init__(self):
        SIPApplication.__init__(self)
        self.ended = Event()
        self.callee = None
        self.session = None
        notification_center = NotificationCenter()
        notification_center.add_observer(self)

    def call(self, callee):
        self.callee = callee
        self.start(FileStorage('config'))

    @run_in_green_thread
    def _NH_SIPApplicationDidStart(self, notification):
        settings = SIPSimpleSettings()
        # We don't need speakers or microphone
        settings.audio.input_device = None
        settings.audio.output_device = None
        settings.save()
        self.callee = ToHeader(SIPURI.parse(self.callee))
        self.player = WavePlayer(SIPApplication.voice_audio_mixer, 'test.wav', loop_count=0, initial_delay=False)
        try:
            routes = DNSLookup().lookup_sip_proxy(self.callee.uri, ['udp']).wait()
        except DNSLookupError, e:
            print 'DNS lookup failed: %s' % str(e)
        else:
            account = AccountManager().default_account
            self.session = Session(account)
            self.session.connect(self.callee, routes, [AudioStream()])

    def _NH_SIPSessionGotRingIndication(self, notification):
        print 'Ringing!'

    def _NH_SIPSessionDidStart(self, notification):
        audio_stream = notification.data.streams[0]
        audio_stream.bridge.add(self.player)
        print 'play wav file'
        self.player.play()
        print 'Audio session established using "%s" codec at %sHz' % (audio_stream.codec, audio_stream.sample_rate)

    def _NH_SIPSessionDidFail(self, notification):
        print 'Failed to connect'
        self.stop()

    def _NH_SIPSessionDidEnd(self, notification):
        print 'Session ended'
        self.stop()

    def _NH_SIPApplicationDidEnd(self, notification):
        self.ended.set()
# place an audio call to the specified SIP URI in user@domain format
target_uri="sip:1000@192.168.1.50"
application = SimpleCallApplication()
application.call(target_uri)
print "Placing call to %s, press Enter to quit the program" % target_uri
raw_input()
application.session.end()
application.ended.wait()
