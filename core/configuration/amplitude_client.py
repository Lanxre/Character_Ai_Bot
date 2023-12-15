from amplitude import Amplitude

from config import amplitude_settings

amplitude_client = Amplitude(amplitude_settings.token)
amplitude_client.configuration.server_zone = 'RU'



