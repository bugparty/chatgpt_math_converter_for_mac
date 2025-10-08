# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-10-08

### Added
- Initial release
- Cross-platform clipboard monitoring (Windows and macOS)
- Automatic conversion of ChatGPT math notation to standard Markdown format
- Convert `\[...\]` to `$$...$$` for block equations
- Convert `\(...\)` to `$...$` for inline equations
- Convert `[...]` (multiline) to `$$...$$` for block equations
- Remove extra spaces in inline math: `$ xxx $` → `$xxx$`
- Command-line interface via `chatgpt-math-converter` command
- Platform-specific optional dependencies (pywin32 for Windows, pyobjc for macOS)

### Technical
- Built with marko for robust Markdown parsing
- Factory pattern for platform-specific clipboard implementations
- Proper Python package structure (src layout)
- Published to PyPI for easy installation

[0.1.0]: https://github.com/bugparty/chatgpt_math_converter_for_mac/releases/tag/v0.1.0
