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
            inventory
            teams
            no_of_teams
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
            inventory
            teams
            no_of_teams
            pdf_reports
            ai_assistant
        }
    }
    """
)

test_if_is_employee = gql(
    """
    query testIfIsEmployee {
        testIfIsEmployee
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
            phone_number
            payment_method
            is_paid_user
            is_employee
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

get_workspace = gql(
    """
    query getWorkspace {
        getWorkspace {
            id
            name
            workspace_uid
            owner {
                id
                username
            }
        }
    }
    """
)

get_team_logs = gql(
    """
    query getTeamLogs($workspace_id: ID!) {
        getTeamLogs(workspace_id: $workspace_id) {
            id
            workspace {
                id
                name
            }
            user {
                id
                username
            }
            action
        }
    }
    """
)

get_team_members = gql(
    """
    query getTeamMembers {
        getTeamMembers {
            id
            user {
                id
                username
            }
            plan {
                id
                name
            }
            phone_number
            workspace_uid
            is_paid_user
            is_employee
        }
    }
    """
)

request_billing_history = gql(
    """
    query requestBilling {
        requestBilling
    }
    """
)

cancel_plan = gql(
    """
    query cancelPlan {
        requestBilling
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
            workspace {
                id
                name
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
            reorder_level
            reorder_quantity
            supplier_name
            supplier_phone_number
            supplier_email
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
            workspace {
                id
                name
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
            reorder_level
            reorder_quantity
            supplier_name
            supplier_phone_number
            supplier_email
            profit_generated
        }
    }
    """
)

get_all_customers = gql(
    """
    query getAllCustomers($account_id: ID!) {
        getAllCustomers(account_id: $account_id) {
            id
            workspace {
                id
                name
            }
            account {
                id
                account_name
            }
            name
            email
            phone
        }
    }
    """
)

get_customer = gql(
    """
    query getCustomer($id: ID!) {
        getCustomer(id: $id) {
            id
            workspace {
                id
                name
            }
            account {
                id
                account_name
            }
            name
            email
            phone
        }
    }
    """
)

get_all_debts = gql(
    """
    query getAllDebts($account_id: ID!) {
        getAllDebts(account_id: $account_id) {
            id
            workspace {
                id
                name
            }
            account {
                id
                account_name
            }
            customer {
                id
                name
            }
            amount
            due_date
            is_paid
        }
    }
    """
)

get_debt = gql(
    """
    query getDebt($id: ID!) {
        getDebt(id: $id) {
            id
            workspace {
                id
                name
            }
            account {
                id
                account_name
            }
            customer {
                id
                name
            }
            amount
            due_date
            is_paid
        }
    }
    """
)

get_all_reports = gql(
    """
    query getAllReports($account_id: ID!) {
        getAllReports(account_id: $account_id) {
            id
            account {
                account_name
            }
            statement_uid
            begin_date
            end_date
        }
    }
    """
)

get_report = gql(
    """
    query getReport($statement_uid: String!) {
        getReport(statement_uid: $statement_uid) {
            id
            statement_uid
            amount
            item {
                name
                is_income
            }
        }
    }
    """
)
