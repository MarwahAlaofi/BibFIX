import re
import bibtexparser
import textwrap


def preprocess_title(title):
    return re.sub(r'[^a-zA-Z0-9\s+\-\"\:]', '', title).replace('\n', " ").lower()


# code below adapted from this blog post: https://kitchingroup.cheme.cmu.edu/blog/2014/02/09/Sorting-fields-in-bibtex
# -entries/
def format_bib_entry(en):
    if type(en) is not dict:
        parsed_bibtex = bibtexparser.loads(en)
        en = parsed_bibtex.entries[0]

    # field, format, wrap or not
    field_order = [('author', '{{{0}}},\n', True),
                   ('title', '{{{0}}},\n', True),
                   ('year', '{{{0}}},\n', True),
                   ('journal', '{{{0}}},\n', True),
                   ('booktitle', '{{{0}}},\n', True),
                   ('series', '{{{0}}},\n', True),
                   ('volume', '{{{0}}},\n', True),
                   ('number', '{{{0}}},\n', True),
                   ('pages', '{{{0}}},\n', True),
                   ('url', '{{{0}}},\n', False),
                   ('doi', '{{{0}}},\n', False)]
    keys = set(en.keys())

    extra_fields = keys.difference([f[0] for f in field_order])

    # we do not want these in our entry, they go in the "header"
    extra_fields.remove('ENTRYTYPE')
    extra_fields.remove('ID')
    # Now build up our entry string
    s = '@{type}{{{id},\n'.format(type=en['ENTRYTYPE'].upper(),
                                  id=en['ID'])

    # Now handle the ordered fields, then the extra fields
    for field, fmt, wrap in field_order[:-2]:
        if field in en:
            s1 = '  {0} ='.format(field.upper())
            s2 = fmt.format(en[field])
            s3 = '{0:17s}{1}'.format(s1, s2)
            if wrap:
                s3 = textwrap.fill(s3, subsequent_indent=' ' * 18, width=70) + '\n'
            s += s3

    for field in extra_fields:
        if field in en:
            s1 = '  {0} ='.format(field.upper())
            s2 = en[field]
            s3 = '{0:17s}{{{1}}}'.format(s1, s2)
            s3 = textwrap.fill(s3, subsequent_indent=' ' * 18, width=70) + '\n'
            s += s3

    # add the url and the doi to the end of the bib entry
    for field, fmt, wrap in field_order[-2:]:
        if field in en:
            s1 = '  {0} ='.format(field.upper())
            s2 = fmt.format(en[field])
            s3 = '{0:17s}{1}'.format(s1, s2)
            if wrap:
                # fill seems to remove trailing '\n'
                s3 = textwrap.fill(s3, subsequent_indent=' ' * 18, width=70) + '\n'
            s += s3
    s += '}\n\n'
    return s
