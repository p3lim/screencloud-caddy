import os
import ScreenCloud
import pycaddy as caddy

from PythonQt.QtCore import QSettings, QFile, QStandardPaths
from PythonQt.QtUiTools import QUiLoader

class CaddyUpload():
	def __init__(self):
		self.uil = QUiLoader()
		self.loadSettings()

	def upload(self, screenshot, name):
		path = QStandardPaths.writableLocation(QStandardPaths.TempLocation)
		path = os.path.join(path, name)

		try:
			screenshot.save(QFile(path), ScreenCloud.getScreenshotFormat())
		except Exception as e:
			raise

		if not path:
			ScreenCloud.setError('Failed to save screenshot')
			return False

		try:
			if self.auth_enable and len(self.auth_key) > 0 and len(self.auth_secret) > 0:
				url = caddy.upload(self.url_address, path, self.auth_key, self.auth_secret)
			else:
				url = caddy.upload(self.url_address, path)
		except Exception as e:
			ScreenCloud.setError('\n' + str(e))
			return False

		if self.copy_link:
			ScreenCloud.setUrl(url)

		return True

	def getFilename(self):
		return ScreenCloud.formatFilename(self.name_format)

	def showSettingsUI(self, parentWidget):
		self.parentWidget = parentWidget

		self.settingsDialog = self.uil.load(QFile(workingDir + '/settings.ui'), parentWidget)
		self.settingsDialog.group_url.check_auth.connect('stateChanged(int)', self.updateUI)
		self.settingsDialog.group_screenshot.input_name.connect('textChanged(QString)', self.nameFormatEdited)
		self.settingsDialog.connect('accepted()', self.saveSettings)

		self.loadSettings()

		self.settingsDialog.group_url.input_url.text = self.url_address
		self.settingsDialog.group_url.check_auth.checked = self.auth_enable
		self.settingsDialog.group_url.input_key.text = self.auth_key
		self.settingsDialog.group_url.input_secret.text = self.auth_secret
		self.settingsDialog.group_url.check_copylink.checked = self.copy_link

		self.settingsDialog.group_screenshot.input_name.text = self.name_format

		self.updateUI()

		self.settingsDialog.open()

	def loadSettings(self):
		settings = QSettings()
		settings.beginGroup('uploaders')
		settings.beginGroup('caddy')

		self.url_address = settings.value('url-address', '')
		self.auth_enable = settings.value('auth-enable', 'False') == 'True'
		self.auth_key = settings.value('auth-key', '')
		self.auth_secret = settings.value('auth-secret', '')
		self.copy_link = settings.value('copy-link', 'True') == 'True'

		self.name_format = settings.value('name-format', '%Y-%m-%d_%H-%M-%S')

		settings.endGroup()
		settings.endGroup()

	def saveSettings(self):
		settings = QSettings()
		settings.beginGroup('uploaders')
		settings.beginGroup('caddy')

		settings.setValue('url-address', self.settingsDialog.group_url.input_url.text)
		settings.setValue('auth-enable', str(self.settingsDialog.group_url.check_auth.checked))
		settings.setValue('auth-key', self.settingsDialog.group_url.input_key.text)
		settings.setValue('auth-secret', self.settingsDialog.group_url.input_secret.text)
		settings.setValue('copy-link', str(self.settingsDialog.group_url.check_copylink.checked))

		settings.setValue('name-format', self.settingsDialog.group_screenshot.input_name.text)

		settings.endGroup()
		settings.endGroup()

	def isConfigured(self):
		self.loadSettings()

		if len(self.url_address) > 0:
			if self.auth_enable:
				if len(self.auth_key) > 0 and len(self.auth_secret) > 0:
					return True
			else:
				return True

	def nameFormatEdited(self, name_format):
		self.settingsDialog.group_screenshot.label_example.setText(ScreenCloud.formatFilename(name_format))

	def updateUI(self):
		auth_enabled = self.settingsDialog.group_url.check_auth.checked

		self.settingsDialog.group_url.label_key.setVisible(auth_enabled)
		self.settingsDialog.group_url.input_key.setVisible(auth_enabled)

		self.settingsDialog.group_url.label_secret.setVisible(auth_enabled)
		self.settingsDialog.group_url.input_secret.setVisible(auth_enabled)