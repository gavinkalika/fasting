class UserSettingEnum:
    __settings = {
        'timezone': {
            'default_value': 'America/New_York',
            'setting_id': 1,
        }
    }

    @classmethod
    def get_default_value(cls, enum_type_label):
        return cls.__settings[enum_type_label]['default_value']

    @classmethod
    def get_setting_id_by_label(cls, enum_type_label):
        return cls.__settings[enum_type_label]['setting_id']
