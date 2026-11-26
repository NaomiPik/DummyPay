from playwright.sync_api import expect
import uuid




def create_bank_account(bank_accounts_page):
    account_number = str(uuid.uuid4().int)[:10]
    bank_name = "Test Bank" + account_number


    bank_accounts_page.click_add_account()
    bank_accounts_page.fill_account_details(
        "Naomi Pik", bank_name, account_number
    )
    bank_accounts_page.select_country("Israel")
    bank_accounts_page.select_currency("ILS")


    bank_accounts_page.button_add_bank_account.click()


    expect(bank_accounts_page.dialog).to_be_hidden(timeout=15000)


    bank_account = bank_accounts_page.get_bank_account_by_name(bank_name)
    expect(bank_account).to_be_visible()


    return bank_account, bank_name