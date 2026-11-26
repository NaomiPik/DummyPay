from pages.dummypay_base import DummyPayBase




class BankAccounts(DummyPayBase):




    def __init__(self, page):
        super().__init__(page)
        self.main_heading=self.page.get_by_role("heading", name="Bank Accounts")
        self.page_subtitle=self.page.get_by_text("Manage your simulated bank accounts.", exact=True)
        self.info_alert=self.page.get_by_role("alert").filter(has_text="Bank accounts in DummyPay are simulated. They are not connected to any bank and no real transfers take place.")
        self.button_add_account=self.page.get_by_role("button", name="Add bank account")
        self.empty_state_title=self.page.get_by_text("No bank accounts yet", exact=True)
        self.empty_state_description=self.page.get_by_text("Add a simulated bank account to see it here.", exact=True)






        self.dialog=self.page.get_by_role("dialog", name="Add a simulated bank account")
        self.main_heading_dialog=self.dialog.get_by_role("heading", name="Add a simulated bank account", level=2)
        self.second_heading=self.dialog.get_by_text("Not connected to any bank. No real transfers are made. Only a masked account number is stored.")
        self.account_holder_name = self.dialog.get_by_role("textbox", name="Account holder name")
        self.bank_name = self.dialog.get_by_role("textbox", name="Bank name")
        self.country = self.dialog.get_by_role("combobox", name="Country")
        self.currency = self.dialog.get_by_role("combobox", name="Currency")
        self.iban_or_account_number = self.dialog.get_by_role("textbox", name="IBAN or account number")
        self.iban_or_account_number_paragraph = self.dialog.get_by_text("Enter a 4–20 digit account number.")
        self.button_cancel=self.dialog.get_by_role("button", name="Cancel")
        self.button_add_bank_account=self.dialog.get_by_role("button", name="Add bank account")
        self.button_close=self.dialog.get_by_role("button", name="Close")
        self.confirm_delete_dialog = self.page.get_by_role("alertdialog")
        self.confirm_delete_button = self.confirm_delete_dialog.get_by_role("button", name="Remove")


    


    def click_add_account(self):
        self.button_add_account.click()




    def fill_account_details(self, account_holder, bank_name, iban_or_account_number):


        self.account_holder_name.fill(account_holder)


       
        self.bank_name.fill(bank_name)
        self.iban_or_account_number.fill(iban_or_account_number)




    def select_country(self, country):
        self.country.click()
        self.page.get_by_role("option", name=country, exact=True).click()


    def select_currency(self, currency):
        self.currency.click()
        self.page.get_by_role("option", name=currency, exact=True).click()




    def get_bank_account_by_name(self, bank_name):
         
         return self.page.get_by_role("listitem").filter(has_text=bank_name)




    def remove_account_bank(self, bank_account):


         remove_button = bank_account.get_by_role("button", name="Remove")
         remove_button.click()


