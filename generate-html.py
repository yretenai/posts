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
    for md_file in sorted(glob('markdown/*.md')):
        with cope(md_file, 'r', 'utf8') as md:
            markdown = Markdown(extensions=['meta', 'tables', 'smarty', 'fenced_code', CodeHiliteExtension(noclasses=True, pygments_style='github-dark'), 'toc', 'admonition'])
            text = markdown.convert(md.read().strip())
            meta = markdown.Meta
            name = splitext(basename(md_file))[0]
            target = '{name}'.format(name=name)
            index_lines += '<li><a href="{url}.html">{title}</a></li>\n'.format(title=meta['title'][0], url=target)

            print(target)
            with cope('docs/{url}.html'.format(url=target), 'w', 'utf8') as html:
                html.write(POST_TEMPLATE.format(title=meta['title'][0], short=meta['short'][0], url=target, time=meta['date'][0], isotime= datetime.strptime(meta['date'][0], '%Y-%m-%d %I:%M %p').isoformat(), body=text))
    index.write(INDEX_TEMPLATE.format(body=index_lines))
