"""Rebuilds the "GNU Terry Pratchett" Wiki space/page on this site from the
content and screenshots that ship alongside this script.

Requires the `wiki` app (frappe/wiki) to already be installed on the target
site. Screenshots aren't committed to the repo — copy screenshots/*.png from
the lab site into this same wiki_docs/screenshots/ folder before running.

Usage, from the target bench:
    bench --site <site> execute gnu_terry_pratchett.wiki_docs.import_wiki_posts.run

Safe to re-run: it finds-or-creates the space and page by their fixed route,
and always overwrites the content and screenshots with the current ones on
disk, so re-running is how you rebuild/refresh the page.
"""

import os

import frappe
from frappe.utils.file_manager import save_file

HERE = os.path.dirname(__file__)
SCREENSHOT_DIR = os.path.join(HERE, "screenshots")
CONTENT_FILE = os.path.join(HERE, "content.md")

SPACE_ROUTE = "clacks"
SPACE_NAME = "GNU Terry Pratchett"
PAGE_TITLE = "GNU Terry Pratchett"

# placeholder in content.md -> screenshot file name in screenshots/
SCREENSHOTS = {
	"AWESOME_BAR_SCREENSHOT": "awesome-bar-search.png",
	"SETTINGS_SCREENSHOT": "settings-page.png",
}


def _get_or_create_space():
	existing = frappe.db.get_value("Wiki Space", {"route": SPACE_ROUTE})
	if existing:
		return frappe.get_doc("Wiki Space", existing)

	space = frappe.new_doc("Wiki Space")
	space.space_name = SPACE_NAME
	space.route = SPACE_ROUTE
	space.insert(ignore_permissions=True)
	return space


def _get_or_create_page(space):
	existing = frappe.db.get_value(
		"Wiki Document", {"wiki_space": space.name, "title": PAGE_TITLE, "is_group": 0}
	)
	if existing:
		return frappe.get_doc("Wiki Document", existing)

	page = frappe.new_doc("Wiki Document")
	page.parent_wiki_document = space.root_group
	page.title = PAGE_TITLE
	page.content = "_(rebuilding...)_"
	page.insert(ignore_permissions=True)
	return page


def _replace_screenshot(page, filename):
	local_path = os.path.join(SCREENSHOT_DIR, filename)
	if not os.path.exists(local_path):
		frappe.throw(
			f"Missing {local_path} -- copy the screenshot from the lab site into "
			"wiki_docs/screenshots/ before running this import."
		)

	for existing_file in frappe.get_all(
		"File",
		filters={"attached_to_doctype": "Wiki Document", "attached_to_name": page.name, "file_name": filename},
		pluck="name",
	):
		frappe.delete_doc("File", existing_file, ignore_permissions=True, delete_permanently=True)

	with open(local_path, "rb") as f:
		file_doc = save_file(filename, f.read(), "Wiki Document", page.name, is_private=0)
	return file_doc.file_url


def run():
	if not frappe.db.exists("DocType", "Wiki Space"):
		frappe.throw("The wiki app isn't installed on this site -- run `bench install-app wiki` first.")

	with open(CONTENT_FILE) as f:
		content = f.read()

	space = _get_or_create_space()
	page = _get_or_create_page(space)

	for placeholder, filename in SCREENSHOTS.items():
		file_url = _replace_screenshot(page, filename)
		content = content.replace(f"{{{{{placeholder}}}}}", file_url)

	page.content = content
	page.is_published = 1
	page.save(ignore_permissions=True)

	# Wiki Space.insert() mutates itself (assigns root_group) after our copy was
	# read, so save() against the stale timestamp would raise a conflict --
	# set_value sidesteps that instead of re-fetching just to flip one flag.
	if not frappe.db.get_value("Wiki Space", space.name, "is_published"):
		frappe.db.set_value("Wiki Space", space.name, "is_published", 1)

	frappe.db.commit()
	# The reader is a client-side SPA (see wiki/frontend/src/router.js); there is
	# no server-rendered route at page.route, only this /wiki-app/... shell URL.
	print(f"Wiki page ready at /wiki-app/spaces/{space.name}/page/{page.name}")
