

```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

uv --version
uvx --version

uv python install 3.12 --default


如果 path 没生效:
uv python update-shell
```