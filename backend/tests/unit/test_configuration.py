from backend.src.sc_config.Configuration import Configuration


def test_configuration():
    config = Configuration()
    unit, _ = config.unit('SZO')
    print('ff')