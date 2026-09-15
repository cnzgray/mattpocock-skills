#!/usr/bin/env python3
# Render every committed *.tmpl in this repo into its target file.
#
# The convention is one rule wide: beside any file, a file named X.tmpl renders
# to X. Inside a template, a line that is exactly
#
#     {{include:path/relative/to/repo/root}}
#
# is replaced, newline and all, by the full contents of that file; every other
# line is copied through untouched. The placeholder must occupy the whole line
# (nothing before it, nothing after it), and the included file must end with a
# newline. Both are errors otherwise.
#
# Inclusion is one level deep and verbatim: an included file that itself
# contains a placeholder line is injected as-is, not re-rendered.
#
# Targets are committed. Plugin distribution reads the rendered files straight
# off disk and runs no build step, so after editing a template or anything it
# includes, run this script and commit the rendered files.
#
# Each target is rendered beside itself and compared with the bytes already on
# disk: identical means nothing is written and the target's mtime is left
# alone; different means a write to a temp file next to the target followed by
# an atomic rename over the old file. Every target prints "generated <path>" or
# "unchanged <path>". Any error names the template and the line number and
# exits non-zero.
#
# Python 3 standard library only. Every file is read and written in binary
# mode, so the bytes are preserved exactly: no newline or encoding
# normalization anywhere.

import os
import sys

PROG = os.path.basename(sys.argv[0])
PREFIX = b"{{include:"
SUFFIX = b"}}"


def fail(message):
	sys.stderr.buffer.write(message + b"\n")
	sys.stderr.buffer.flush()
	raise SystemExit(1)


def error_prefix(tmpl_rel, lineno):
	return os.fsencode("%s: %s:%d: " % (PROG, tmpl_rel, lineno))


def collect_templates(root):
	# The repo's own .git directory is pruned: nothing inside it is a template.
	# Sort order is the byte order of the path (what `LC_ALL=C sort` produced).
	templates = []
	for dirpath, dirnames, filenames in os.walk(root):
		dirnames[:] = [name for name in dirnames if name != ".git"]
		for name in filenames:
			if not name.endswith(".tmpl"):
				continue
			full = os.path.join(dirpath, name)
			if os.path.islink(full) or not os.path.isfile(full):
				continue
			templates.append(os.path.relpath(full, root).replace(os.sep, "/"))
	templates.sort(key=os.fsencode)
	return templates


def iter_records(data):
	# awk's records: every b"\n" ends one, and a final run of bytes that no
	# newline terminates is still a record. Splitting and dropping the phantom
	# element the trailing newline leaves behind reproduces that exactly, so a
	# template whose last line has no newline still renders with one.
	if not data:
		return []
	lines = data.split(b"\n")
	if data.endswith(b"\n"):
		lines.pop()
	return lines


def render(tmpl_rel, root):
	with open(os.path.join(root, tmpl_rel), "rb") as handle:
		records = iter_records(handle.read())

	# A record that is not a placeholder is copied through with the newline awk
	# would have printed after it, so the output is byte-identical either way.
	out = []
	for lineno, line in enumerate(records, 1):

		# A whole-line placeholder: the prefix, at least one path byte, and the
		# closing braces as the last two bytes of the line.
		if (
			line.startswith(PREFIX)
			and line.endswith(SUFFIX)
			and len(line) > len(PREFIX) + len(SUFFIX)
		):
			path = line[len(PREFIX) : -len(SUFFIX)]
			# An absolute path is used as given; a relative one is resolved
			# against the repo root.
			include = os.fsdecode(path)
			if not path.startswith(b"/"):
				include = os.path.join(root, include)

			try:
				with open(include, "rb") as handle:
					content = handle.read()
			except OSError:
				fail(
					error_prefix(tmpl_rel, lineno)
					+ b"cannot read include target "
					+ path
				)

			if not content or not content.endswith(b"\n"):
				fail(
					error_prefix(tmpl_rel, lineno)
					+ b"include target "
					+ path
					+ b" does not end with a newline"
				)

			# The included bytes land verbatim, trailing newline and all.
			out.append(content)
		elif PREFIX in line:
			fail(
				error_prefix(tmpl_rel, lineno)
				+ b"placeholder must occupy the whole line: "
				+ line
			)
		else:
			out.append(line + b"\n")

	return b"".join(out)


def write_target(target_abs, target_rel, data):
	try:
		with open(target_abs, "rb") as handle:
			current = handle.read()
	except OSError:
		current = None

	if current == data:
		print("unchanged %s" % target_rel)
		return

	# The temp file sits next to its target, so the rename stays on one
	# filesystem and is atomic. Its mode matches what a shell redirect would
	# have produced (0666 masked by the umask).
	tmp = "%s.tmp.%d" % (target_abs, os.getpid())
	try:
		descriptor = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o666)
		with os.fdopen(descriptor, "wb") as handle:
			handle.write(data)
		os.replace(tmp, target_abs)
	except BaseException:
		try:
			os.unlink(tmp)
		except OSError:
			pass
		raise

	print("generated %s" % target_rel)


def main():
	# Locate the repo root from this script's own path, so the script can be run
	# from anywhere. Placeholders are resolved relative to it.
	here = os.path.dirname(os.path.realpath(os.path.abspath(__file__)))
	root = os.path.dirname(here)

	templates = collect_templates(root)
	if not templates:
		fail(os.fsencode("%s: no *.tmpl templates found under %s" % (PROG, root)))

	for tmpl_rel in templates:
		target_rel = tmpl_rel[: -len(".tmpl")]
		data = render(tmpl_rel, root)
		write_target(os.path.join(root, target_rel), target_rel, data)

	return 0


if __name__ == "__main__":
	sys.exit(main())
