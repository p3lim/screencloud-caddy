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
		self.settingsDialog.group_screenshot.input_name.connect('textChanged(QString)', self.nameFormatEdited)
		self.settingsDialog.connect('accepted()', self.saveSettings)

		self.loadSettings()

		self.settingsDialog.group_url.input_url.text = self.url_address
		self.settingsDialog.group_url.check_copylink.checked = self.copy_link
		self.settingsDialog.group_screenshot.input_name.text = self.name_format

		self.updateUI()

		self.settingsDialog.open()

	def loadSettings(self):
		settings = QSettings()
		settings.beginGroup('uploaders')
		settings.beginGroup('caddy')

		self.url_address = settings.value('url-address', '')
		self.copy_link = settings.value('copy-link', 'True') == 'True'
		self.name_format = settings.value('name-format', '%Y-%m-%d_%H-%M-%S')

		settings.endGroup()
		settings.endGroup()

	def saveSettings(self):
		settings = QSettings()
		settings.beginGroup('uploaders')
		settings.beginGroup('caddy')

		settings.setValue('url-address', self.settingsDialog.group_url.input_url.text)
		settings.setValue('copy-link', str(self.settingsDialog.group_url.check_copylink.checked))
		settings.setValue('name-format', self.settingsDialog.group_screenshot.input_name.text)

		settings.endGroup()
		settings.endGroup()

	def isConfigured(self):
		self.loadSettings()

		if len(self.url_address) > 0:
			return True

	def nameFormatEdited(self, name_format):
		self.settingsDialog.group_screenshot.label_example.setText(ScreenCloud.formatFilename(name_format))
