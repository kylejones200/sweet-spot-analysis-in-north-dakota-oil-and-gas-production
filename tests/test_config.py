from bakken_sweet_spot.config import load_config, output_root, section
from bakken_sweet_spot.paths import DEFAULT_CONFIG_PATH, PROJECT_ROOT


def test_project_root_and_config():
    assert DEFAULT_CONFIG_PATH.parent == PROJECT_ROOT
    config = load_config(DEFAULT_CONFIG_PATH)
    assert section(config, "output").get("root") == "output"
    root = output_root(config)
    assert root == PROJECT_ROOT / "output"
