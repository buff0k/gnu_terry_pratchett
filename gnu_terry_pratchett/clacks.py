import frappe

HEADER = "X-Clacks-Overhead"


def _is_desk_request(path: str) -> bool:
	# Mirrors frappe.website.path_resolver.PathResolver: the /desk shell is the
	# only "desk page" response; everything else goes through website rendering.
	path = (path or "").strip("/ ")
	return path == "desk" or path.startswith("desk/")


def inject_clacks_overhead_header(response=None, request=None):
	"""after_request hook: add the X-Clacks-Overhead header to rendered HTML pages.

	Runs on every request for every user (settings access is separately
	restricted to System Manager / Website Manager), so this only reads the
	cached singleton and bails out fast when there's nothing to do.
	"""
	if response is None or request is None:
		return

	if not (response.mimetype or "").startswith("text/html"):
		return

	settings = frappe.get_cached_doc("GNU Terry Pratchett Settings")
	if not settings.enabled:
		return

	names = [row.overhead_name for row in settings.overhead_names if row.overhead_name]
	if not names:
		return

	is_desk = _is_desk_request(request.path)
	if settings.scope == "Website Pages Only" and is_desk:
		return
	if settings.scope == "Desk Pages Only" and not is_desk:
		return

	response.headers[HEADER] = ", ".join(names)
