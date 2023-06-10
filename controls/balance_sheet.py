class GenerateBSReport:
    """
    Generates a Balance Sheet report (BS).

    NOTE: This class is strictly meant to be used to generate only Balance Sheet reports.
    """

    def __init__(
        self,
        assets: list,
        liabilities: list,
        equity: list,
        account_balance: float,
    ) -> None:
        self.assets = assets
        self.liabilities = liabilities
        self.equity = equity
        self.account_balance = account_balance

        self.record_uid = ""

    @property
    def balance_sheet_uid(self):
        """
        Returns the uid (unique identifier).

        NOTE: This uid will be used to identify the balance sheet records.
        """

        return self.record_uid

    @balance_sheet_uid.setter
    def balance_sheet_uid(self, uid: str):
        """
        Setter method to change the uid (unique identifier).
        """

        self.record_uid = uid

    def process_assets(self) -> float:
        """
        Returns a total worth of the assets provided.
        """

        total_worth = 0.0

        for item in self.assets:
            total_worth += float(item["net_worth"])

        total_worth += self.account_balance

        return total_worth

    def process_liabilities(self) -> float:
        """
        Returns a total worth of the liabilities provided.
        """

        total_worth = 0.0

        for item in self.liabilities:
            total_worth += float(item["net_worth"])

        return total_worth

    def process_equity(
        self, assets_net_worth: float, liabilities_net_worth: float
    ) -> float:
        """
        Setter method to change the uid (unique identifier).

        NOTE: Consider methods: process_assets(), process_liabilities().
        """

        total_worth = 0.0

        if self.equity:
            for item in self.equity:
                total_worth += float(item["net_worth"])

        total_worth += assets_net_worth - liabilities_net_worth

        return total_worth
