from pathlib import Path

from webrviz import cli


def test_cli_with_httpx_and_katana(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    httpx_file = tmp_path / "httpx.txt"
    katana_file = tmp_path / "katana.txt"

    httpx_file.write_text(
        "https://example.com\n"
        "https://api.example.com\n",
        encoding="utf-8",
    )

    katana_file.write_text(
        "https://example.com/login\n"
        "https://api.example.com/v1/users\n"
        "https://www.example.com/\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "webrviz",
            "--httpx",
            str(httpx_file),
            "--katana",
            str(katana_file),
        ],
    )

    cli.main()

    output = capsys.readouterr().out

    assert "Application" in output
    assert "example.com" in output
    assert "api.example.com" in output
    assert "www.example.com" in output

    assert "/" in output
    assert "/login" in output
    assert "/v1/users" in output

    assert "Application Summary" not in output
    assert "Hosts:" not in output
    assert "Endpoints:" not in output


def test_cli_requires_input_file(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        "sys.argv",
        ["webrviz"],
    )

    try:
        cli.main()
    except SystemExit as exc:
        assert exc.code == 2
