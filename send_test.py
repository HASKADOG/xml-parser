import re
from mechanize import Browser

br = Browser()
br.set_handle_robots( False )
br.open("https://bitrix24public.com/alterate.bitrix24.ru/form/18_test_parser/vyya8z/")
br.select_form(id="bxform")
# Browser passes through unknown attributes (including methods)
# to the selected HTMLForm (from ClientForm).
br.form['DEAL_TITLE'] = 'cheese'
# (the method here is __setitem__)
response = br.submit()  # submit current form