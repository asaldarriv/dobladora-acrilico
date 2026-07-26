from tdg import config


def test_carga_documentos():
    conf = config.load()
    assert "anteproyecto" in conf.documents
    assert conf.documents["anteproyecto"].max_content_pages == 5


def test_anteproyecto_existe():
    conf = config.load()
    assert conf.documents["anteproyecto"].tex.is_file()
