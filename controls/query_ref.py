from ariadne import gql

generate_otp = gql(
    """
    query generateOTP($environment: String) {
        generateOTP(environment: $environment)
    }
    """
)

generate_qr_code = gql(
    """
    query generateQRCode {
        generateQRCode
    }
    """
)

get_transaction_type = gql(
    """
    query getTransactionType {
        getTransactionType {
            id
            type_name
            type_description
        }
    }
    """
)

get_transaction_category = gql(
    """
    query getTransactionCategory {
        getTransactionCategory {
            id
            category_name
            category_description
        }
    }
    """
)

get_transaction_sub_category = gql(
    """
    query getTransactionSubCategory($parent: String!) {
        getTransactionSubCategory(parent: $parent) {
            id
            parent {
                id
                category_name
            }
            category_name
            category_description
        }
    }
    """
)

get_product_category = gql(
    """
    query getProductCategory {
        getProductCategory {
            id
            category_name
            category_description
        }
    }
    """
)

get_product_sub_category = gql(
    """
    query getProductSubCategory($parent: String!) {
        getProductSubCategory(parent: $parent) {
            id
            category_name
            category_description
        }
    }
    """
)

test_standard_decorator = gql(
    """
    query testStandardDecorator {
        testStandardDecorator {
            id
            name
            accounts
            no_of_accounts
            budgets
            no_of_budgets
            targets
            no_of_targets
            invoices
            pdf_reports
            ai_assistant
        }
    }
    """
)

test_pro_decorator = gql(
    """
    query testProDecorator {
        testProDecorator {
            id
            name
            accounts
            no_of_accounts
            budgets
            no_of_budgets
            targets
            no_of_targets
            invoices
            pdf_reports
            ai_assistant
        }
    }
    """
)

get_user = gql(
    """
    query getUser {
        getUser {
            id
            first_name
            last_name
            email
            username
            is_staff
            is_active
        }
    }
    """
)

get_profile = gql(
    """
    query getProfile {
        getProfile {
            id
            user {
                id
                username
            }
            plan {
                id
                name
            }
            payment_method
            is_paid_user
        }
    }
    """
)

get_all_accounts = gql(
    """
    query getAllAccounts {
        getAllAccounts {
            id
            account_name
            account_type
            owner {
                user {
                    id
                    username
                }
                plan {
                    id
                    name
                }
            }
            currency_code
            account_balance
        }
        }
    """
)

get_account = gql(
    """
    query getAccount($id: ID!) {
        getAccount(id: $id) {
            id
            account_name
            account_type
            owner {
                user {
                    id
                    username
                }
                plan {
                    id
                    name
                }
            }
            currency_code
            account_balance
        }
    }
    """
)

get_all_budgets = gql(
    """
    query getAllBudgets {
        getAllBudgets {
            id
            budget_name
            budget_description
            budget_is_active
            budget_amount
            owner {
                user {
                    id
                    username
                }
                plan {
                    id
                    name
                }
            }
            account {
                id
                account_name
            }
            category {
                id
                category_name
            }
            sub_category {
                id
                category_name
            }
        }
    }
    """
)

get_budget = gql(
    """
    query getBudget($id: ID!) {
        getBudget(id: $id) {
            id
            budget_name
            budget_description
            budget_is_active
            budget_amount
            owner {
                user {
                    id
                    username
                }
                plan {
                    id
                    name
                }
            }
            account {
                id
                account_name
            }
            category {
                id
                category_name
            }
            sub_category {
                id
                category_name
            }
        }
    }
    """
)

get_all_targets = gql(
    """
    query getAllTargets {
        getAllTargets {
            id
            target_name
            target_description
            target_is_active
            target_amount
            owner {
                user {
                    id
                    username
                }
                plan {
                    id
                    name
                }
            }
            account {
                id
                account_name
            }
            category {
                id
                category_name
            }
            sub_category {
                id
                category_name
            }
        }
    }
    """
)

get_target = gql(
    """
    query getTarget($id: ID!) {
        getTarget(id: $id) {
            id
            target_name
            target_description
            target_is_active
            target_amount
            owner {
                user {
                    id
                    username
                }
                plan {
                    id
                    name
                }
            }
            account {
                id
                account_name
            }
            category {
                id
                category_name
            }
            sub_category {
                id
                category_name
            }
        }
    }
    """
)

get_all_transactions = gql(
    """
    query getAllTransactions($account_id: ID!) {
        getAllTransactions(account_id: $account_id) {
            id
            transaction_type {
                id
                type_name
            }
            transaction_amount
            currency_code
            description
            transaction_date
            account {
                id
                account_name
                account_balance
            }
            category {
                id
                category_name
            }
            sub_category {
                id
                category_name
            }
        }
    }
    """
)

get_transaction = gql(
    """
    query getTransaction($id: ID!) {
        getTransaction(id: $id) {
            id
            transaction_type {
                id
                type_name
            }
            transaction_amount
            currency_code
            description
            transaction_date
            account {
                id
                account_name
                account_balance
            }
            category {
                id
                category_name
            }
            sub_category {
                id
                category_name
            }
        }
    }
    """
)

get_all_products = gql(
    """
    query getAllProducts($account_id: ID!) {
        getAllProducts(account_id: $account_id) {
            id
            account {
                id
                account_name
            }
            name
            description
            category {
                id
                category_name
            }
            sub_category {
                id
                category_name
            }
            buying_price
            selling_price
            current_stock_level
            units_sold
            supplier_name
            profit_generated
        }
    }
    """
)

get_product = gql(
    """
    query getProduct($id: ID!) {
        getProduct(id: $id) {
            id
            account {
                id
                account_name
            }
            name
            description
            category {
                id
                category_name
            }
            sub_category {
                id
                category_name
            }
            buying_price
            selling_price
            current_stock_level
            units_sold
            supplier_name
            profit_generated
        }
    }
    """
)

get_all_payment_accounts = gql(
    """
    query {
        getAllPaymentAccounts {
            id
            owner {
                id
                user {
                    id
                    username
                }
                is_paid_user
            }
            business_name
            business_email
            business_phone_number
            bank_name
            bank_account
            mobile_payment_name
            mobile_account
        }
    }
    """
)

get_payment_account = gql(
    """
    query($id: ID!) {
        getPaymentAccount(id: $id) {
            id
            owner {
                id
                user {
                    id
                    username
                }
                is_paid_user
            }
            business_name
            business_email
            business_phone_number
            bank_name
            bank_account
            mobile_payment_name
            mobile_account
        }
    }
    """
)

get_all_client_information = gql(
    """
    query {
        getAllClientInformation {
            id
            owner {
                id
                user {
                    id
                    username
                }
                is_paid_user
            }
            client_name
            client_email
            client_phone_number
            client_address
        }
    }
    """
)

get_client_information = gql(
    """
    query($id: ID!) {
        getClientInformation(id: $id) {
            id
            owner {
                id
                user {
                    id
                    username
                }
                is_paid_user
            }
            client_name
            client_email
            client_phone_number
            client_address
        }
    }
    """
)

get_all_invoices = gql(
    """
    query {
        getAllInvoices {
            id
            owner {
                id
                user {
                    id
                    username
                }
                is_paid_user
            }
            business {
                id
                business_name
            }
            client {
                id
                client_name
            }
            category {
                id
                category_name
            }
            sub_category {
                id
                category_name
            }
            item
            quantity
            amount
            total
            additional_notes
            due_date
            is_paid
        }
    }
    """
)

get_invoice = gql(
    """
    query($id: ID!) {
        getInvoice(id: $id) {
            id
            owner {
                id
                user {
                    id
                    username
                }
                is_paid_user
            }
            business {
                id
                business_name
            }
            client {
                id
                client_name
            }
            category {
                id
                category_name
            }
            sub_category {
                id
                category_name
            }
            item
            quantity
            amount
            total
            additional_notes
            due_date
            is_paid
        }
    }
    """
)

get_all_cash_flow_statements = gql(
    """
    query($account_id: ID!) {
        getAllCashFlowStatements(account_id: $account_id) {
            id
            uid
            account {
                id
                account_name
            }
            period_start_date
            period_end_date
        }
    }
    """
)

get_cash_flow_statement = gql(
    """
    query($uid: String!) {
        getCashFlowStatement(uid: $uid) {
            id
            uid
            account {
                id
                account_name
            }
            record {
                id
                uid
                category
                item
                activity
                amount
                is_income
            }
        }
    }
    """
)

get_all_income_statements = gql(
    """
    query($account_id: ID!) {
        getAllIncomeStatements(account_id: $account_id) {
            id
            uid
            account {
                id
                account_name
            }
            revenue
            gross_profit
            operating_expenses
            net_income
            period_start_date
            period_end_date
        }
    }
    """
)

get_income_statement = gql(
    """
    query($uid: String!) {
        getIncomeStatement(uid: $uid) {
            id
            uid
            account {
                id
                account_name
            }
            revenue
            gross_profit
            operating_expenses
            net_income
            period_start_date
            period_end_date
        }
    }
    """
)

get_all_balance_sheet_statements = gql(
    """
    query($account_id: ID!) {
        getAllBalanceSheetStatements(account_id: $account_id) {
            id
            uid
            account {
                id
                account_name
            }
            assets
            liabilities
            equity
        }
    }
    """
)

get_balance_sheet_statement = gql(
    """
    query($uid: String!) {
        getBalanceSheetStatement(uid: $uid) {
            id
            uid
            account {
                id
                account_name
            }
            assets
            liabilities
            equity
        }
    }
    """
)
