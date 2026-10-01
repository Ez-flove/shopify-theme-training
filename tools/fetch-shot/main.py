#!/usr/bin/env python3
# Description: download screenshots from prnt.sc links or direct image URLs into .local/shoot/
"""
A Lightshot link (https://prnt.sc/<id>) is an HTML page, not an image. This finds the image the
page shows, downloads it, and saves it under .local/shoot/ so it can be read and cited.

    tools/run fetch-shot https://prnt.sc/wyq2moKuoeul
    tools/run fetch-shot "any text — every http(s) link in every argument is fetched"
    tools/run fetch-shot <link> --force          download again over the saved file
    tools/run fetch-shot <link> --out <dir>      save somewhere else inside the project

Nothing is saved unless the bytes really are an image. Three ways Lightshot answers without one,
each measured on 2026-10-01 and each refused by name rather than saved:

  no browser User-Agent   HTTP 520
  unknown id              302 to https://prnt.sc/
  removed or expired id   200 with a placeholder image served from st.prntscr.com

Other sites' pages are refused rather than guessed: the og:image of an arbitrary page is as often
a logo as a screenshot. Add a site here once its page has been measured.

.local/shoot/index.tsv records which file came from which link.
"""
import datetime
import html.parser
import os
import re
import struct
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib  # noqa: E402

USER_AGENT = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
LIGHTSHOT_HOSTS = {"prnt.sc", "www.prnt.sc", "prntscr.com", "www.prntscr.com"}
PLACEHOLDER_HOSTS = {"st.prntscr.com"}
DEFAULT_OUT = ".local/shoot"
INDEX_NAME = "index.tsv"
INDEX_COLUMNS = ["file", "source", "image", "fetched_at", "bytes", "size"]
TIMEOUT = 30
LINK = re.compile(r"https?://[^\s<>\"'`)\]]+")


class Refused(Exception):
    """The link did not lead to an image. The message says why, in the reader's terms."""


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as resp:
            return resp.geturl(), resp.headers.get_content_type(), resp.read()
    except urllib.error.HTTPError as exc:
        raise Refused("HTTP %d from %s" % (exc.code, url))
    except urllib.error.URLError as exc:
        raise Refused("cannot reach %s (%s)" % (url, exc.reason))


class ScreenshotTag(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.img = None
        self.og = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "img" and attrs.get("id") == "screenshot-image":
            self.img = attrs.get("src")
        elif tag == "meta" and attrs.get("property") == "og:image":
            self.og = attrs.get("content")


def lightshot_image(link):
    """The image URL a Lightshot page shows, or Refused."""
    shot_id = urllib.parse.urlsplit(link).path.strip("/")
    if not re.fullmatch(r"[A-Za-z0-9_-]+", shot_id):
        raise Refused("not a screenshot link — no id in the path")
    final, _, body = fetch(link)
    if urllib.parse.urlsplit(final).path.strip("/") != shot_id:
        raise Refused("no such screenshot — Lightshot redirected to %s" % final)
    tag = ScreenshotTag()
    tag.feed(body.decode("utf-8", "replace"))
    src = tag.img or tag.og
    if not src:
        raise Refused("the page shows no screenshot image — Lightshot may have changed its page")
    src = urllib.parse.urljoin(final, src)
    if urllib.parse.urlsplit(src).hostname in PLACEHOLDER_HOSTS:
        raise Refused("removed or expired — Lightshot serves its placeholder image instead (%s)" % src)
    return shot_id, src


def jpeg_size(data):
    i = 2
    while i + 9 < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            height, width = struct.unpack(">HH", data[i + 5:i + 9])
            return width, height
        i += 2 + struct.unpack(">H", data[i + 2:i + 4])[0]
    return None


def sniff(data):
    """(extension, (width, height) or None) from the bytes themselves — never from a header."""
    if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24:
        return "png", struct.unpack(">II", data[16:24])
    if data.startswith(b"\xff\xd8"):
        return "jpg", jpeg_size(data)
    if data[:6] in (b"GIF87a", b"GIF89a"):
        return "gif", struct.unpack("<HH", data[6:10])
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "webp", None
    return None, None


def links_in(args):
    seen = []
    for arg in args:
        for match in LINK.findall(arg):
            link = match.rstrip(".,;:!?")
            if link not in seen:
                seen.append(link)
    return seen


def read_index(path):
    rows = {}
    if os.path.exists(path):
        lines = _lib.read(path).splitlines()
        for line in lines[1:]:
            cells = line.split("\t")
            if len(cells) == len(INDEX_COLUMNS):
                rows[cells[0]] = dict(zip(INDEX_COLUMNS, cells))
    return rows


def write_index(path, rows):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\t".join(INDEX_COLUMNS) + "\n")
        for name in sorted(rows):
            fh.write("\t".join(rows[name][c] for c in INDEX_COLUMNS) + "\n")


def free_name(out_dir, stem, ext, rows, source):
    """stem.ext, unless that file already holds a different link's image."""
    n = 1
    while True:
        name = "%s.%s" % (stem if n == 1 else "%s-%d" % (stem, n), ext)
        taken = os.path.exists(os.path.join(out_dir, name))
        if not taken or rows.get(name, {}).get("source") == source:
            return name
        n += 1


def save_one(link, out_dir, rows, force):
    """(status, name, row) for one link, or Refused."""
    for name, row in rows.items():
        if row["source"] == link and os.path.exists(os.path.join(out_dir, name)) and not force:
            return "exists", name, row

    host = urllib.parse.urlsplit(link).hostname or ""
    if host in LIGHTSHOT_HOSTS:
        stem, image_url = lightshot_image(link)
    else:
        stem = os.path.splitext(os.path.basename(urllib.parse.urlsplit(link).path))[0]
        stem = re.sub(r"[^A-Za-z0-9_.-]", "_", stem)[:80] or "shot"
        image_url = link

    _, content_type, data = fetch(image_url)
    ext, size = sniff(data)
    if not ext:
        if content_type == "text/html":
            raise Refused("an HTML page, not an image. Pages are understood only for: %s"
                          % ", ".join(sorted(LIGHTSHOT_HOSTS)))
        raise Refused("downloaded %d bytes of %s, which is not a PNG, JPEG, GIF or WebP image"
                      % (len(data), content_type))

    name = free_name(out_dir, stem, ext, rows, link)
    target = os.path.join(out_dir, name)
    fd, tmp = tempfile.mkstemp(dir=out_dir, prefix=".fetch-shot-")
    with os.fdopen(fd, "wb") as fh:
        fh.write(data)
    os.replace(tmp, target)

    row = {
        "file": name,
        "source": link,
        "image": image_url,
        "fetched_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "bytes": str(len(data)),
        "size": "%dx%d" % size if size else "?",
    }
    return "saved", name, row


def main():
    argv = sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__.strip())
        sys.exit(0)
    force = "--force" in argv
    out_rel = DEFAULT_OUT
    if "--out" in argv:
        i = argv.index("--out")
        if i + 1 >= len(argv):
            _lib.die("--out needs a directory")
        out_rel = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    argv = [a for a in argv if a != "--force"]

    root = _lib.project_root()
    out_dir = os.path.abspath(os.path.join(root, out_rel))
    if not out_dir.startswith(root + os.sep):
        _lib.die("--out must stay inside the project (%s is not)" % out_dir)

    links = links_in(argv)
    if not links:
        _lib.die("no http(s) link in the arguments")

    os.makedirs(out_dir, exist_ok=True)
    index_path = os.path.join(out_dir, INDEX_NAME)
    rows = read_index(index_path)
    shown = os.path.relpath(out_dir, root)

    rep = _lib.Reporter("fetch-shot")
    for link in links:
        try:
            status, name, row = save_one(link, out_dir, rows, force)
        except Refused as exc:
            rep.fail(link, "%s\nnothing saved" % exc)
            continue
        rows[name] = row
        rep.note("%-6s %s/%s  %s  %s B  <- %s"
                 % (status, shown, name, row["size"], row["bytes"], link))
    write_index(index_path, rows)
    sys.exit(rep.finish())


if __name__ == "__main__":
    main()
