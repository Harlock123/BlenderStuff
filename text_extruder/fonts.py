import os
import sys

# Cache to prevent Blender garbage-collecting dynamic enum items.
_font_cache = {}
_enum_items = []


def _get_font_dirs():
    """Return existing system font directories for the current platform."""
    if sys.platform == "darwin":
        candidates = [
            "/System/Library/Fonts",
            "/Library/Fonts",
            os.path.expanduser("~/Library/Fonts"),
        ]
    elif sys.platform == "win32":
        windir = os.environ.get("WINDIR", r"C:\Windows")
        localappdata = os.environ.get("LOCALAPPDATA", "")
        candidates = [
            os.path.join(windir, "Fonts"),
            os.path.join(localappdata, "Microsoft", "Windows", "Fonts"),
        ]
    else:  # Linux / BSD
        candidates = [
            "/usr/share/fonts",
            "/usr/local/share/fonts",
            os.path.expanduser("~/.local/share/fonts"),
            os.path.expanduser("~/.fonts"),
        ]
    return [d for d in candidates if os.path.isdir(d)]


def scan_fonts(force_refresh=False):
    """Scan system font directories and return {display_name: file_path}.

    Results are cached; pass *force_refresh=True* to re-scan.
    """
    global _font_cache
    if _font_cache and not force_refresh:
        return _font_cache

    fonts = {}
    for font_dir in _get_font_dirs():
        for root, _, files in os.walk(font_dir):
            for filename in files:
                if filename.lower().endswith((".ttf", ".otf")):
                    path = os.path.join(root, filename)
                    display_name = os.path.splitext(filename)[0]
                    # Keep the first occurrence if duplicates exist.
                    if display_name not in fonts:
                        fonts[display_name] = path

    _font_cache = dict(sorted(fonts.items(), key=lambda kv: kv[0].lower()))
    return _font_cache


def font_enum_items(self, context):
    """Dynamic enum callback for Blender EnumProperty."""
    global _enum_items

    fonts = scan_fonts()
    items = [("__DEFAULT__", "Default (BFont)", "Use Blender's built-in font")]
    for name, path in fonts.items():
        items.append((path, name, path))

    # Keep a reference so Blender doesn't garbage-collect the strings.
    _enum_items = items
    return _enum_items
