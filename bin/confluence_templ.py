

STRUCTURED_MACRO = '''
<ac:structured-macro ac:name="status">
    <ac:parameter ac:name="colour">{colour}</ac:parameter>
    <ac:parameter ac:name="title">{title}</ac:parameter>
</ac:structured-macro>
'''

UPDATE_MESSAGE = '''
<p>Page automatically updated by {login} on {datetime}<br/>
    Columns marked with (*) has been filled automatically and will be overwritten if edited manually.<br/>
</p>
'''


PARAGRAPH = '''
    <p>{content}</p>
'''


def update_message(login, datetime):
    return UPDATE_MESSAGE.format(login=login, datetime=datetime)


def structured_macro(colour, title):
    return STRUCTURED_MACRO.format(colour=colour, title=title)


def paragraph(content):
    return PARAGRAPH.format(content=content)
