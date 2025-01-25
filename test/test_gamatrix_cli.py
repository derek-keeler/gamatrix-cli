from click.testing import CliRunner

from gamatrixcli.__main__ import gcli


def test_get_r_done():
    assert True


def test_commands_exist():
    runner = CliRunner()
    result = runner.invoke(gcli, ["--help"])
    assert result.exit_code == 0
    assert "add-db" in result.output
    assert "show" in result.output
    assert "compare" in result.output
