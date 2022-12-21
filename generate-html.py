from markdown import markdown
from glob import iglob
from codecs import open as cope
from os.path import basename, splitext

HEADER = '\n<!-- could not read header -->\n'
FOOTER = '\n<!-- could not read footer -->\n'

try:
    with cope('__head.html', 'r', 'utf8') as header:
        HEADER = header.read().replace('\r\n', '\n') + '\n'
except: pass

try:
    with cope('__foot.html', 'r', 'utf8') as footer:
        FOOTER = '\n' + footer.read().replace('\r\n', '\n')
except: pass

with cope('docs/index.html', 'w', 'utf8') as index:
    index.writelines([HEADER, '\n<ol>\n'])

    for md_file in iglob('docs/markdown/*.md'):
        with cope(md_file, 'r', 'utf8') as md:
            md_text = md.read().strip()
            title = md_text.split('\n', 1)[0][1:].strip()
            text = markdown(md_text)
            name = splitext(basename(md_file))[0]
            target = '{name}.html'.format(name = name)
            print(target)
            with cope(target, 'w') as html:
                html.writelines([HEADER, '<a href="index.html">back</a> - <a href="markdown/{name}.md">markdown</a>\n\n'.format(name = name), text, FOOTER])
                index.writelines(['<a href="{url}">{title}</a>\n'.format(title = title, url = target)])

    index.writelines(['</ol>', FOOTER])
