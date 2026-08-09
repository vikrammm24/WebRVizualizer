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
        "https://example.com\nhttps://api.example.com\n",
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
    assert "login" in output

    assert "v1" in output
    assert "users" in output


def test_cli_with_httpx_only(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    httpx_file = tmp_path / "httpx.txt"

    httpx_file.write_text(
        "https://example.com\nhttps://example.com/login\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "webrviz",
            "--httpx",
            str(httpx_file),
        ],
    )

    cli.main()

    output = capsys.readouterr().out

    assert "Application" in output
    assert "example.com" in output
    assert "login" in output


def test_cli_with_katana_only(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    katana_file = tmp_path / "katana.txt"

    katana_file.write_text(
        "https://example.com\nhttps://example.com/api/v1/users\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "webrviz",
            "--katana",
            str(katana_file),
        ],
    )

    cli.main()

    output = capsys.readouterr().out

    assert "Application" in output
    assert "example.com" in output
    assert "api" in output
    assert "v1" in output
    assert "users" in output


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


def test_cli_rejects_missing_httpx_file(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    missing_file = tmp_path / "missing-httpx.txt"

    monkeypatch.setattr(
        "sys.argv",
        [
            "webrviz",
            "--httpx",
            str(missing_file),
        ],
    )

    try:
        cli.main()
    except SystemExit as exc:
        assert exc.code == 1

    output = capsys.readouterr().out

    assert "HTTPX file not found." in output
    assert "Provided path" in output
    assert "Resolved path" in output


def test_cli_rejects_missing_katana_file(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    missing_file = tmp_path / "missing-katana.txt"

    monkeypatch.setattr(
        "sys.argv",
        [
            "webrviz",
            "--katana",
            str(missing_file),
        ],
    )

    try:
        cli.main()
    except SystemExit as exc:
        assert exc.code == 1

    output = capsys.readouterr().out

    assert "Katana file not found." in output
    assert "Provided path" in output
    assert "Resolved path" in output


def test_cli_help(
    monkeypatch,
    capsys,
) -> None:
    monkeypatch.setattr(
        "sys.argv",
        [
            "webrviz",
            "--help",
        ],
    )

    try:
        cli.main()
    except SystemExit as exc:
        assert exc.code == 0

    output = capsys.readouterr().out

    assert "WebRViz - Web Application Visualizer" in output
    assert "--httpx" in output
    assert "--katana" in output


def test_cli_rejects_httpx_directory(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    directory = tmp_path / "input-directory"
    directory.mkdir()

    monkeypatch.setattr(
        "sys.argv",
        [
            "webrviz",
            "--httpx",
            str(directory),
        ],
    )

    try:
        cli.main()
    except SystemExit as exc:
        assert exc.code == 1

    output = capsys.readouterr().out

    assert "HTTPX path is not a file." in output
    assert "Provided path" in output
    assert "Resolved path" in output


def test_cli_rejects_katana_directory(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    directory = tmp_path / "input-directory"
    directory.mkdir()

    monkeypatch.setattr(
        "sys.argv",
        [
            "webrviz",
            "--katana",
            str(directory),
        ],
    )

    try:
        cli.main()
    except SystemExit as exc:
        assert exc.code == 1

    output = capsys.readouterr().out

    assert "Katana path is not a file." in output
    assert "Provided path" in output
    assert "Resolved path" in output
