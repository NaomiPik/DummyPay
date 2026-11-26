from playwright.sync_api import expect
from tests.bank_accounts_helpers import create_bank_account




def test_bank_accounts_heading(logged_in):
    dashboard_page=logged_in
    bank_accounts_page = dashboard_page.go_to_bank_accounts()
   
     # Assert
    expect(bank_accounts_page.main_heading).to_be_visible()
    expect(bank_accounts_page.page_subtitle).to_be_visible()
    expect(bank_accounts_page.info_alert).to_be_visible()
    expect(bank_accounts_page.button_add_account).to_be_visible()
    expect(bank_accounts_page.button_add_account).to_be_enabled()


def test_add_and_delete_bank_account(logged_in):


    dashboard_page=logged_in
    bank_accounts_page = dashboard_page.go_to_bank_accounts()
    bank_accounts_page.click_add_account()
    




    expect(bank_accounts_page.dialog).to_be_visible()
    expect(bank_accounts_page.main_heading_dialog).to_be_visible()
    expect(bank_accounts_page.second_heading).to_be_visible()
    expect(bank_accounts_page.account_holder_name).to_be_editable()
    expect(bank_accounts_page.bank_name).to_be_editable()
    expect(bank_accounts_page.country).to_be_visible()
    bank_accounts_page.country.click()
    expected_countries = [
        "Israel",
        "United States",
        "United Kingdom",
        "Germany",
        "France",
        "Spain",
        "Italy",
        "Netherlands",
        "Belgium",
        "Austria",
        "Switzerland",
        "Ireland",
        "Portugal",
        "Sweden",
        "Norway",
        "Denmark",
        "Finland",
        "Poland",
        "Canada",
        "Australia"
    ]


    for expected_country in expected_countries:
        expect(
            bank_accounts_page.page.get_by_role(
                "option", name=expected_country, exact=True
            )
        ).to_be_visible()
    bank_accounts_page.page.keyboard.press("Escape")
    expect(bank_accounts_page.currency).to_be_visible()
    bank_accounts_page.currency.click()
    expected_currencies = [
    "ILS",
    "USD",
    "EUR",
    "GBP"
    ]


    for expected_currency in expected_currencies:
        expect(
        bank_accounts_page.page.get_by_role(
            "option", name=expected_currency, exact=True
        )
    ).to_be_visible()
    bank_accounts_page.page.keyboard.press("Escape")
    expect(bank_accounts_page.iban_or_account_number).to_be_editable()
    expect(bank_accounts_page.iban_or_account_number_paragraph).to_be_visible()




    bank_account, bank_name = create_bank_account(bank_accounts_page)


    print("Created account:", bank_name)


    expect(bank_accounts_page.dialog).to_be_hidden()
    expect(bank_account).to_be_visible()
    expect(bank_account).to_contain_text(bank_name)
    expect(bank_account).to_contain_text("Israel")
    expect(bank_account).to_contain_text("ILS")
    expect(bank_account).to_contain_text("Naomi Pik")




    bank_accounts_page.remove_account_bank(bank_account)


    expect(bank_accounts_page.confirm_delete_dialog).to_be_visible()
    expect(bank_accounts_page.confirm_delete_button).to_be_visible()
    expect(bank_accounts_page.confirm_delete_button).to_be_enabled()




    with bank_accounts_page.page.expect_response(
        lambda response: response.request.method == "DELETE"
    ) as response_info:
        bank_accounts_page.confirm_delete_button.click()


    response = response_info.value


    print("Created account:", bank_name)
    print("Delete status:", response.status)
    print("Delete URL:", response.url)


    expect(bank_accounts_page.confirm_delete_dialog).to_be_hidden()
    expect(bank_account).to_be_hidden()
    # bank_accounts_page.confirm_delete_button.click()
    expect(bank_accounts_page.confirm_delete_dialog).to_be_hidden()
    expect(bank_account).to_be_hidden()




    
    


def test_other_buttons_in_dialog(logged_in):




    dashboard_page=logged_in
    bank_accounts_page = dashboard_page.go_to_bank_accounts()




    bank_accounts_page.click_add_account()


    expect(bank_accounts_page.dialog).to_be_visible()
    
    expect(bank_accounts_page.button_cancel).to_be_visible()
    expect(bank_accounts_page.button_cancel).to_be_enabled()
    bank_accounts_page.button_cancel.click()
    expect(bank_accounts_page.dialog).to_be_hidden()




    bank_accounts_page.click_add_account()
    
    expect(bank_accounts_page.dialog).to_be_visible()


    
    expect(bank_accounts_page.button_close).to_be_visible()
    expect(bank_accounts_page.button_close).to_be_enabled()
    bank_accounts_page.button_close.click()
    expect(bank_accounts_page.dialog).to_be_hidden()




def test_cancel_delete_bank_account(logged_in):


    dashboard_page=logged_in
    bank_accounts_page = dashboard_page.go_to_bank_accounts()


    bank_account, bank_name = create_bank_account(bank_accounts_page)


    bank_accounts_page.remove_account_bank(bank_account)
    expect(bank_accounts_page.confirm_delete_dialog).to_be_visible()
    bank_accounts_page.confirm_delete_dialog.get_by_role(
        "button", name="Cancel"
    ).click()
    
    expect(bank_accounts_page.confirm_delete_dialog).to_be_hidden()
    expect(bank_account).to_be_visible()






    # Cleanup - delete the test account
    bank_accounts_page.remove_account_bank(bank_account)


    expect(bank_accounts_page.confirm_delete_dialog).to_be_visible()


    with bank_accounts_page.page.expect_response(
        lambda response: response.request.method == "DELETE"
    ) as response_info:
        bank_accounts_page.confirm_delete_button.click()


    assert response_info.value.status in [200, 204]
    expect(bank_accounts_page.confirm_delete_dialog).to_be_hidden()
    expect(bank_account).to_be_hidden()