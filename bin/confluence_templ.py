

STRUCTURED_MACRO_STATUS = '''
<ac:structured-macro ac:name="status">
    <ac:parameter ac:name="colour">{colour}</ac:parameter>
    <ac:parameter ac:name="title">{title}</ac:parameter>
</ac:structured-macro>
'''

STRUCTURED_MACRO_STATUS_SUBTLE = '''
<ac:structured-macro ac:name="status">
    <ac:parameter ac:name="title">{title}</ac:parameter>
    <ac:parameter ac:name="subtle">true</ac:parameter>
</ac:structured-macro>
'''

STRUCTURED_MACRO_EXPAND = '''
<ac:structured-macro ac:name="expand">
    <ac:parameter ac:name="title">{title}</ac:parameter>
    <ac:rich-text-body>
        {body}
    </ac:rich-text-body>
</ac:structured-macro>
'''

STRUCTURED_MACRO_INFO = '''
<ac:structured-macro ac:name="info">
    <ac:parameter ac:name="title">{title}</ac:parameter>
    <ac:rich-text-body>
        {body}
    </ac:rich-text-body>
</ac:structured-macro>
'''

UPDATE_MESSAGE = '''
<p>Page automatically updated by {login} on {datetime}<br/>
    Columns marked with (*) has been filled automatically and will be overwritten if edited manually.<br/>
    BA Desk Check Status has been updated automatically only for Completed(Ready) and Accepted(Pass) issues.<br/>
</p>
'''

PARAGRAPH = '''
    <p>{content}</p>
'''

UL = '''
    <ul>{content}</ul>
'''

LI_HREF = '''
    <li><a href='{link}'>{title}</a>{comment}</li>
'''


def unordered_list_with_hrefs(items):
    list_items = ''
    for item in items:
        list_items += LI_HREF.format(link=item['link'], title=item['title'], comment=item['comment'])
    return UL.format(content=list_items)


def update_message(login, datetime):
    return UPDATE_MESSAGE.format(login=login, datetime=datetime)


def structured_macro_status(colour, title):
    return STRUCTURED_MACRO_STATUS.format(colour=colour, title=title)


def structured_macro_status_subtle(title):
    return STRUCTURED_MACRO_STATUS_SUBTLE.format(title=title)


def structured_macro_expand(title, body):
    return STRUCTURED_MACRO_EXPAND.format(title=title, body=body)


def structured_macro_info(title, body):
    return STRUCTURED_MACRO_INFO.format(title=title, body=body)


def paragraph(content):
    return PARAGRAPH.format(content=content)
