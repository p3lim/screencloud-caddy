import ScreenCloud

from PythonQt.QtCore import QSettings
from PythonQt.QtUiTools import QUiLoader

class CaddyUpload():
	def __init__(self):
		self.uil = QUiLoader()
		self.loadSettings()

	def upload(self, screenshot, name):
		return True

	def getFilename(self):
		return ScreenCloud.formatFilename('temp')

	def showSettingsUI(self, parentWidget):
		self.parentWidget = parentWidget

		self.settingsDialog = self.uil.load(QFile(workingDir + '/settings.ui'), parentWidget)
		self.settingsDialog.group_screenshot.input_name.connect('textChanged(QString)', self.nameFormatEdited)
		self.settingsDialog.connect('accepted()', self.saveSettings)

		self.loadSettings()

		self.settingsDialog.group_url.input_url.text = self.url_address
		self.settingsDialog.group_screenshot.input_name.text = self.name_format

		self.settingsDialog.open()

	def loadSettings(self):
		settings = QSettings()
		settings.beginGroup('uploaders')
		settings.beginGroup('caddy')

		self.url_address = settings.value('url-address', '')
		self.name_format = settings.value('name-format', '%Y-%m-%d_%H-%M-%S')

		settings.endGroup()
		settings.endGroup()

	def saveSettings(self):
		settings = QSettings()
		settings.beginGroup('uploaders')
		settings.beginGroup('caddy')

		settings.setValue('url-address', self.settingsDialog.group_url.input_url.text)
		settings.setValue('name-format', self.settingsDialog.group_screenshot.input_name.text)

		settings.endGroup()
		settings.endGroup()

	def isConfigured(self):
		self.loadSettings()

		if len(self.url_address) > 0:
			return True

	def nameFormatEdited(self, name_format):
		self.settingsDialog.group_screenshot.label_example.setText(ScreenCloud.formatFilename(name_format))
