from markdown import Markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from glob import glob
from codecs import open as cope
from datetime import datetime
from os.path import basename, splitext

with cope('post.html', 'r', 'utf8') as post_template:
    POST_TEMPLATE = post_template.read().strip().replace('\r\n', '\n') + '\n'

with cope('index.html', 'r', 'utf8') as index_template:
    INDEX_TEMPLATE = index_template.read().strip().replace('\r\n', '\n') + '\n'

with cope('docs/index.html', 'w', 'utf8') as index:
    index_lines = ''
    for md_file in reversed(sorted(glob('markdown/*.md'))):
        with cope(md_file, 'r', 'utf8') as md:
            markdown = Markdown(extensions=['meta', 'tables', 'smarty', 'fenced_code', 'codehilite', 'footnotes', 'toc', 'admonition'])
            text = markdown.convert(md.read().strip())
            meta = markdown.Meta
            name = splitext(basename(md_file))[0]

            if not 'title' in meta:
                continue

            folder = 'private/'
            rel = '../'
            if 'private' not in meta:
                index_lines += '<li><a href="{url}.html">{title}</a></li>\n'.format(title=meta['title'][0], url=name)
                folder = ''
                rel = ''

            print(name)
            with cope('docs/{folder}{url}.html'.format(folder=folder, url=name), 'w', 'utf8') as html:
                html.write(POST_TEMPLATE.format(title=meta['title'][0], short=meta['short'][0], url=name, time=meta['date'][0], isotime= datetime.strptime(meta['date'][0], '%Y-%m-%d %I:%M %p').isoformat(), body=text, rel=rel))
    index.write(INDEX_TEMPLATE.format(body=index_lines))
