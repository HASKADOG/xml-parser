from mechanize import Browser

kr = Browser()
kr.set_handle_robots(False)
kr.open("https://bitrix24public.com/alterate.bitrix24.ru/form/18_test_parser/vyya8z/")
kr.select_form(id="bxform")
kr.form['DEAL_TITLE'] = "cheese"
kr.submit()