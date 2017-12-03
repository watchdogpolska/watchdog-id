import base64
try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO
import pyotp
import qrcode


class TOTPManager(object):

    def __init__(self, session, user):
        self.session = session
        self.user = user

    def get_totp_secret(self):
        if 'totp_token' not in self.session:
            self.session['totp_token'] = pyotp.random_base32()
        return self.session['totp_token']

    def get_totp(self):
        if not hasattr(self, 'totp'):
            self.totp = pyotp.TOTP(self.get_totp_secret())
        return self.totp

    def get_totp_uri(self):
        return self.get_totp().provisioning_uri(name=self.user.email,
                                                issuer_name=self.user.email)

    def get_totp_image(self):
        image = qrcode.make(self.get_totp_uri())

        buffer = BytesIO()
        image.save(buffer, format="JPEG")
        content = base64.b64encode(buffer.getvalue())
        return "data:image/png;base64,{}".format(content)
