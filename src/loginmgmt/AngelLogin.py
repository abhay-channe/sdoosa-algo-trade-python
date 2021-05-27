import logging
from smartapi import SmartConnect
from pathlib import Path
from config.Config import getSystemConfig
from loginmgmt.BaseLogin import BaseLogin

class AngelLogin(BaseLogin):
  def __init__(self, brokerAppDetails):
    BaseLogin.__init__(self, brokerAppDetails)

  def login(self, args):
    logging.info('==> AngelLogin .args => %s', args);
    systemConfig = getSystemConfig(Path(__file__).parent.parent.parent)
    brokerHandle = SmartConnect(api_key=self.brokerAppDetails.appKey)
    redirectUrl = None
    if 'request_token' in args:
      requestToken = args['request_token']
      logging.info('Angel requestToken = %s', requestToken)
      session = brokerHandle.generate_session(requestToken, api_secret=self.brokerAppDetails.appSecret)
      
      accessToken = session['access_token']
      accessToken = accessToken
      logging.info('Angel accessToken = %s', accessToken)
      brokerHandle.set_access_token(accessToken)
      
      logging.info('Angel Login successful. accessToken = %s', accessToken)

      # set broker handle and access token to the instance
      self.setBrokerHandle(brokerHandle)
      self.setAccessToken(accessToken)

      # redirect to home page with query param loggedIn=true
      homeUrl = systemConfig['homeUrl'] + '?loggedIn=true'
      logging.info('Angel Redirecting to home page %s', homeUrl)
      redirectUrl = homeUrl
    else:
      loginUrl = brokerHandle.login_url()
      logging.info('Redirecting to Angel login url = %s', loginUrl)
      redirectUrl = loginUrl

    return redirectUrl

