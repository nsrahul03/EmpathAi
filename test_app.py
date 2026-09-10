from pathlib import Path


def test_web_files_exist():
    assert Path("web/app.py").exists()
    assert Path("web/templates/index.html").exists()


def test_app_syntax():
    source = Path("web/app.py").read_text()
    compile(source, "web/app.py", "exec")
