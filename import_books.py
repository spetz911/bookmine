#!/usr/bin/env python

import subprocess
import sys
import os.path
import shutil
import urllib.parse

from xml.etree import ElementTree as ET

from pprint import pprint
import datetime

convert_script = "/Applications/calibre.app/Contents/MacOS/ebook-convert"

update_meta_script = "/Applications/calibre.app/Contents/MacOS/fetch-ebook-metadata"


fb2_formats = {
'none':                    "Прочее",
'mystery':                 "Детективный роман",
'romance_fantasy':         "Фэнтезийный роман",
'sf_history':              "Альтернативная история",
'sf_action':               "Боевая Фантастика",
'sf_epic':                 "Эпическая Фантастика",
'sf_heroic':               "Героическая фантастика",
'sf_detective':            "Детективная Фантастика",
'sf_cyberpunk':            "Киберпанк",
'sf_space':                "Космическая Фантастика",
'sf_social':               "Социальная фантастика",
'sf_horror':               "Ужасы и Мистика",
'sf_humor':                "Юмористическая фантастика",
'sf_fantasy':              "Фэнтези",
'sf':                      "Научная Фантастика",
'child_sf':                "Детская Фантастика",
'det_classic':             "Классический Детектив",
'det_police':              "Полицейский Детектив",
'det_action':              "Боевики",
'det_irony':               "Иронический Детектив",
'det_history':             "Исторический Детектив",
'det_espionage':           "Шпионский Детектив",
'det_crime':               "Криминальный Детектив",
'det_political':           "Политический Детектив",
'det_maniac':              "Маньяки",
'det_hard':                "Крутой Детектив",
'thriller':                "Триллеры",
'detective':               "Детектив",
'sf_detective':            "Детективная Фантастика",
'child_det':               "Детские Остросюжетные",
'love_detective':          "Остросюжетные Любовные Романы",
'prose':                   "Проза",
'prose_classic':           "Классическая Проза",
'prose_history':           "Историческая Проза",
'prose_contemporary':      "Современная Проза",
'prose_counter':           "Контркультура",
'prose_rus_classic':       "Русская Классика",
'prose_su_classics':       "Советская Классика",
'humor_prose':             "Юмористическая Проза",
'child_prose':             "Детская Проза",
'love':                    "Любовные романы",
'love_contemporary':       "Современные Любовные Романы",
'love_history':            "Исторические Любовные Романы",
'love_detective':          "Остросюжетные Любовные Романы",
'love_short':              "Короткие Любовные Романы",
'love_erotica':            "Эротика",
'adv_western':             "Вестерны",
'adv_history':             "Исторические Приключения",
'adv_indian':              "Приключения: Индейцы",
'adv_maritime':            "Морские Приключения",
'adv_geo':                 "Путешествия и География",
'adv_animal':              "Природа и Животные",
'adventure':               "Приключения",
'child_adv':               "Детские Приключения",
'children':                "Детское",
'child_tale':              "Сказки",
'child_verse':             "Детские Стихи",
'child_prose':             "Детская Проза",
'child_sf':                "Детская Фантастика",
'child_det':               "Детские Остросюжетные",
'child_adv':               "Детские Приключения",
'child_education':         "Детская Образовательная литература",
'children':                "Детское",
'poetry':                  "Поэзия",
'dramaturgy':              "Драматургия",
'humor_verse':             "Юмористические Стихи",
'child_verse':             "Детские Стихи",
'antique_ant':             "Античная Литература",
'antique_european':        "Европейская Старинная Литература",
'antique_russian':         "Древнерусская Литература",
'antique_east':            "Древневосточная Литература",
'antique_myths':           "Мифы. Легенды. Эпос",
'antique':                 "Старинная Литература",
'sci_history':             "История",
'sci_psychology':          "Психология",
'sci_culture':             "Культурология",
'sci_religion':            "Религиоведение",
'sci_philosophy':          "Философия",
'sci_politics':            "Политика",
'sci_business':            "Деловая литература",
'sci_juris':               "Юриспруденция",
'sci_linguistic':          "Языкознание",
'sci_medicine':            "Медицина",
'sci_phys':                "Физика",
'sci_math':                "Математика",
'sci_chem':                "Химия",
'sci_biology':             "Биология",
'sci_tech':                "Технические",
'science':                 "Научно-образовательная",
'adv_animal':              "Природа и Животные",
'comp_www':                "Интернет",
'comp_programming':        "Программирование",
'comp_hard':               "Компьютерное Железо",
'comp_soft':               "Программы",
'comp_db':                 "Базы Данных",
'comp_osnet':              "ОС и Сети",
'computers':               "Компьютеры",
'ref_encyc':               "Энциклопедии",
'ref_dict':                "Словари",
'ref_ref':                 "Справочники",
'ref_guide':               "Руководства",
'reference':               "Справочная Литература",
'nonf_biography':          "Биографии и Мемуары",
'nonf_publicism':          "Публицистика",
'nonf_criticism':          "Критика",
'nonfiction':              "Документальное",
'design':                  "Искусство, Дизайн",
'adv_animal':              "Природа и Животные",
'religion':                "Религия",
'religion_rel':            "Религия",
'religion_esoterics':      "Эзотерика",
'religion_self':           "Самосовершенствование",
'religion':                "Религия и духовность",
'sci_religion':            "Религиоведение",
'humor_anecdote':          "Анекдоты",
'humor_prose':             "Юмористическая Проза",
'humor_verse':             "Юмористические Стихи",
'humor':                   "Юмор",
'home_cooking':            "Кулинария",
'home_pets':               "Домашние Животные",
'home_crafts':             "Хобби, Ремесла",
'home_entertain':          "Развлечения",
'home_health':             "Здоровье",
'home_garden':             "Сад и Огород",
'home_diy':                "Сделай Сам",
'home_sport':              "Спорт",
'home_sex':                "Эротика, Секс",
'home':                    "Дом и Семья"
}

def find_sentence(data, idx):
	i1 = idx
	while not(data[i1].tag == "p" and data[i1].text and
		(data[i1].text[:1].isupper() or data[i1].text in ['#', '$'])):
		i1 += 1
	i2 = i1
	while data[i2].tag == "p" and data[i2].text and data[i2].text.strip():
		# test internal of sentence
		txt = data[i2].text.rstrip()
		if txt[:1] in ['#', '$']:
			return i1, i2
		if txt[-1:] in ['.', ';', ':', '!', '?'] or txt[-2:] in ['.”', '."', ".'", '!"']:
			return i1, i2+1
		else:
			i2 += 1
	return i1, None


def calibre_clean(data):
	for el in data:
		if 'class' in el.attrib:
			del(el.attrib['class'])
		calibre_clean(el)


def process_pdf(pdf_str):
	data = ET.fromstring(pdf_str)
	calibre_clean(data)
	idx = 0
	try:
		while idx < len(data):
			i1,i2 = find_sentence(data, idx)
			if not i2:
				idx = i1 + 1
				continue
			txts = [x.text for x in data[i1 : i2]]
			txts = [(s[:-1] if s[-1:] == '-' else s) for s in txts]
			data[i1].text = "\n".join(txts)
						       
			for el in data[i1+1:i2]:
				data.remove(el)
			idx = i1 + 1
	except IndexError as e:
		print("end of document")
	except Exception as e:
		print("err in paragraph %d %s: %s" % (idx, str(type(e)), str(e)))
	return ET.tostring(data, encoding="utf-8", method="html").decode("utf-8")



# TODO:

# update_meta_script -t 'real world haskell' -o tmp -c tmp.png

cat_count = [
	'Haskell',
	'Erlang',
	'JavaScript',
	'Python',
	'Ruby',
	'C++',
	'PHP',
	'NodeJS',
	'Scala',
	'OCaml',
	'Clojure',
	'Racket',
	'Java ']

def check_cat(full_name):
	path = "./categories/%s.html" % full_name.lower()
	if os.path.exists(path):
		return
	s = """---
layout: category_list
title: "%s"
description: " description "
group: cat
category_id: %s
---
""" % (full_name, full_name.lower())
	s = s + "{%  include JB/setup %}\n"
	with open(path, 'w') as f:
		f.write(s)
	return


def make_tags():
	for tag,tit in fb2_formats.items():
		path = "./tags/%s.html" % tag
		if os.path.exists(path):
			continue
		s = """---
layout: tag_list
title: "%s"
description: " description "
group: tag_list
tag_id: %s
---
""" % (tit, tag)
		s = s + "{%  include JB/setup %}\n"
		with open(path, 'w') as f:
			f.write(s)
	return

def get_category(metrics):
	# print(metrics)
	mm = max(metrics.values())
	if mm < 22:
		check_cat("None")
		return "none"
	# else
	for k,v in metrics.items():
		if v == mm:
			check_cat(k)
			return k.lower()


def count_local_meter(body):
	metrics = dict((x,0) for x in cat_count)
	for cc in cat_count:
		metrics[cc] += body.count(cc)
		metrics[cc] += body.count(cc.lower())
	return metrics


def process_html(path, prev, next, meta, is_pdf):
	data = ""
	with open(path) as f:
		data = f.read()
	if data.startswith("---"):
		return count_local_meter(data)
	pos1 = data.index("<body")
	pos2 = data.index(">", pos1)
	pos3 = data.index("</body>")
	body = "<div>\n" + data[pos2+1 : pos3] + "</div>\n"
	if is_pdf:
		body = process_pdf(body)
	with open(path,'w') as f:
		f.write("---\n")
		f.write("layout: page\n")
		f.write('title: %s\n' % meta.get('title'))
		# f.write("tagline: %s\n" % (", ".join(meta.get('title', [])) and []))
		f.write("prev: %s\n" % prev)
		f.write("next: %s\n" % next)
		f.write("book_path: %s\n" % meta['book_path'])
		f.write("---\n")
		f.write("{% include JB/setup %}\n")
		f.write("{% raw %}\n")
		f.write(body)
		f.write("\n")
		f.write("{% endraw %}\n")
		f.write("\n")
	# find best category
	return count_local_meter(body)

def process_meta(book_path):
	res = ET.parse(book_path + "/content.opf")
	root = res.getroot()
	
	ns = '{http://www.idpf.org/2007/opf}'
	metadata = root.find(ns + 'metadata')
	manifest = root.find(ns + 'manifest')
	spine    = root.find(ns + 'spine')
	guide    = root.find(ns + 'guide')

	ns = '{http://purl.org/dc/elements/1.1/}'
	meta = dict((x.tag[len(ns):], x.text) for x in metadata)
	data = dict((x.attrib['id'], x.attrib['href']) for x in manifest)
	styles = [x.attrib['href'] for x in manifest if x.attrib['media-type'] == "text/css"]
	content = [data[x.attrib['idref']] for x in spine]
	cover = [x.attrib['href'] for x in guide if x.attrib['type'] == 'cover']
	toc   = [x.attrib['href'] for x in guide if x.attrib['type'] == 'toc']
	if toc and toc[0] in content:
		content.remove(toc[0])
	meta['creator'] = [x.strip() for x in meta.get('creator', []).split(',')]
	if cover:
		meta['cover'] = cover[0]
	if 'title' in meta:
		meta['title'] = '"%s"' % meta['title'].replace('"', "'")
	if 'subject' in meta:
		meta['tags'] = '["%s"]' % meta['subject']
	else:
		meta['tags'] = '[none]'
	if 'date' in meta:
		meta['book_date'] = meta['date']
		del(meta['date'])
	if 'description' in meta:
		meta['perface'] = meta['description']
		del(meta['description'])
	return meta, content

def mega_replace(ss):
	return ''.join([(x if x.isalpha() else '-') for x in ss])

def process_book(src_path, book_name, is_pdf, export_paths):
	book_name = mega_replace(book_name.lower())
	book_name = book_name.replace('---', '-').replace('--', '-')
	book_path = os.path.join("books/", book_name + '_oeb/')
	if os.path.exists(book_path):
		print("exists: %s" % book_name)
		# shutil.rmtree(book_path)
	else:
		subprocess.call([convert_script, src_path, book_path])
	meta, manifest = process_meta(book_path)

	dd = datetime.date.today().isoformat()
	meta['book_path'] = urllib.parse.quote(book_path)

	metrics = dict((x,0) for x in cat_count)
	for i,curr in enumerate(manifest):
		prev = (manifest[i-1] if i != 0 else None)
		next = (manifest[i+1] if i != len(manifest)-1 else None)
		tmp = process_html(os.path.join(book_path, curr), prev, next, meta, is_pdf)
		for cc in cat_count:
			metrics[cc] += tmp[cc]

	# add table_of_content
	title, nav = parse_table_of_content(book_path)

	meta_path = os.path.join("./_posts/", "%s-%s.html" % (dd, book_name))
	meta_path = urllib.parse.quote(meta_path)
	print("saved: " + meta_path)
	with open(meta_path, 'w') as f:
		f.write("---\n")
		f.write("layout: book\n")
		for k,v in meta.items():
			if k and v:
				if k == 'perface':
					f.write("%s: |\n    %s\n" % (k, v.replace('\n', '\n    ')))
				else:
					f.write("%s: %s\n" % (k,v))
		f.write("category: %s\n" % get_category(metrics))
		# f.write("tags: [good, anytag]\n")
		f.write("formats:\n")
		for x in export_paths.items():
			f.write("    %s: %s\n" % x)
		f.write("manifest:\n")
		for x in manifest:
			f.write("  - %s\n" % x)
		f.write("---\n\n")
		f.write("<h3>%s</h3>\n" % title)
		make_list_toc(f, nav, meta['book_path'])
		f.write("\n")

def html_escape(text):
    """Returns the given HTML with ampersands, quotes and carets encoded."""
    res = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return res.replace('"', '&quot;').replace("'", '&#39;')

def make_media_toc(f, nav, book_path):
	if not nav:
		return
	f.write('<ul class="media-list">\n')
	for x in nav:
		f.write('<li class="media">\n')
		f.write('<i class="media-object icon-folder-open"></i>\n')
		f.write('<div class="media-body">\n')
		f.write('\n')
		f.write('<h4 class="media-heading"><a href="%s">\n' % x['link'])
		f.write('  %s\n' % html_escape(x['label']))
		f.write('</a></h4>\n')
		f.write('<p> ... </p>\n')
		# <!-- Nested media object -->
		make_media_toc(f, x['childs'], book_path)
		f.write('</div>\n')
		f.write('</li>\n')
	f.write('</ul>\n')

def make_list_toc(f, nav, book_path):
	if not nav:
		return
	f.write('<ul>\n')
	for x in nav:
		f.write('<li>\n')
		f.write('<i class="icon-folder-open"></i>\n')
		f.write('<a href="../../%s/%s">\n' % (book_path, x['link']))
		f.write('%s\n' % html_escape(x['label']))
		f.write('</a>\n')
		# <!-- Nested media object -->
		make_list_toc(f, x['childs'], book_path)
		f.write('</li>\n')
	f.write('</ul>\n')
    


def parse_table_of_content(book_path):
	if not os.path.exists("./_posts/"):
		return "", []
	root = ET.parse(book_path + "/toc.ncx").getroot()
	ns = '{http://www.daisy.org/z3986/2005/ncx/}'
	title = root.find(ns+'docTitle')
	if title:
		title = title.find(ns+'text').text
	nav = [make_toc_tree(x) for x in root.find(ns+'navMap').findall(ns+"navPoint")]
	return title, nav


def make_toc_tree(root):
	ns = '{http://www.daisy.org/z3986/2005/ncx/}'
	res = dict()
	res['label'] = root.find(ns+'navLabel').find(ns+'text').text
	res['link'] =  root.find(ns+'content').attrib['src']
	res['childs'] = [make_toc_tree(x) for x in root.findall(ns+"navPoint")]
	return res

good_formats = ['.epub', '.mobi', '.fb2']

def export_another_formats(book_name, src_path):
	if not os.path.exists("./export/"):
		os.mkdir("./export/")
	book_name = book_name.replace('.', '_')
	book_paths = dict()
	for ff in good_formats:
		book_path = os.path.join("./export/", book_name + ff)
		if not os.path.exists(book_path):
			subprocess.call([convert_script, src_path, book_path])
		book_paths[ff] = urllib.parse.quote(book_path)
	return book_paths


def main():
	for path in sys.argv[1:]:
		pref, suf = os.path.split(path)
		name, ex = os.path.splitext(suf)
		if not os.path.exists("./books/"):
			os.mkdir("./books/")
		if not os.path.exists("./_posts/"):
			os.mkdir("./_posts/")
		if not os.path.exists("./categories/"):
			os.mkdir("./categories/")
		if not os.path.exists("./tags/"):
			os.mkdir("./tags/")
		make_tags()
		# if ex in good_formats:
		# 	export_paths = export_another_formats(name, path)
		# else:
		export_paths = dict()
		process_book(path, name, ex == '.pdf', export_paths)

main()

