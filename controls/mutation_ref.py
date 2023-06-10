from ariadne import gql


verify_otp = gql(
    """
    mutation verifyOTP($otp: String!) {
        verifyOTP(otp: $otp)
    }
    """
)

token_auth = gql(
    """
    mutation tokenAuth($username: String!, $password: String!) {
        tokenAuth(username: $username, password: $password) {
            token
            refresh_token
            payload
        }
    }
    """
)

verify_token = gql(
    """
    mutation verifyToken($token: String!) {
        verifyToken(token: $token) {
            payload
        }
    }
    """
)

refresh_token = gql(
    """
    mutation refreshToken($token: String!) {
        refreshToken(token: $token) {
            token
            refresh_token
            payload
        }
    }
    """
)

create_user = gql(
    """
    mutation createUser(
        $email: String!
        $first_name: String!
        $last_name: String!
        $password: String!
        $password2: String!
    ) {
        createUser(
            email: $email
            first_name: $first_name
            last_name: $last_name
            password: $password
            password2: $password2
        ) {
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

update_user = gql(
    """
    mutation updateUser(
        $email: String!
        $first_name: String!
        $last_name: String!
    ) {
        updateUser(
            email: $email
            first_name: $first_name
            last_name: $last_name
        ) {
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

create_account = gql(
    """
    mutation createAccount(
        $account_name: String!
        $account_type: String!
        $account_balance: String!
        $currency_code: String!
    ) {
        createAccount(
            account_name: $account_name
            account_type: $account_type
            account_balance: $account_balance
            currency_code: $currency_code
        ) {
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
                is_paid_user
            }
            currency_code
            account_balance
        }
    }
    """
)

update_account = gql(
    """
    mutation updateAccount(
        $id: ID!
        $account_name: String!
        $account_type: String!
        $account_balance: String!
        $currency_code: String!
    ) {
        updateAccount(
            id: $id
            account_name: $account_name
            account_type: $account_type
            account_balance: $account_balance
            currency_code: $currency_code
        ) {
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
                is_paid_user
            }
            currency_code
            account_balance
        }
    }
    """
)

delete_account = gql(
    """
    mutation deleteAccount($id: ID!) {
        deleteAccount(id: $id)
    }
    """
)

create_budget = gql(
    """
    mutation createBudget(
        $account_id: ID!
        $budget_name: String!
        $budget_description: String!
        $budget_amount: String!
        $category: String!
        $sub_category: String!
    ) {
        createBudget(
            account_id: $account_id
            budget_name: $budget_name
            budget_description: $budget_description
            budget_amount: $budget_amount
            category: $category
            sub_category: $sub_category
        ) {
            id
            budget_name
            budget_description
            budget_amount
            budget_is_active
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

update_budget = gql(
    """
    mutation updateBudget(
        $id: ID!
        $budget_name: String!
        $budget_description: String!
        $budget_amount: String!
        $category: String!
        $sub_category: String!
    ) {
        updateBudget(
            id: $id
            budget_name: $budget_name
            budget_description: $budget_description
            budget_amount: $budget_amount
            category: $category
            sub_category: $sub_category
        ) {
            id
            budget_name
            budget_description
            budget_amount
            budget_is_active
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

budget_status = gql(
    """
    mutation budgetStatus($id: ID!, $status: Boolean!) {
        budgetStatus(id: $id, status: $status)
    }
    """
)

delete_budget = gql(
    """
    mutation deleteBudget($id: ID!) {
        deleteBudget(id: $id)
    }
    """
)

create_target = gql(
    """
    mutation createTarget(
        $account_id: ID!
        $target_name: String!
        $target_description: String!
        $target_amount: String!
        $category: String!
        $sub_category: String!
    ) {
        createTarget(
            account_id: $account_id
            target_name: $target_name
            target_description: $target_description
            target_amount: $target_amount
            category: $category
            sub_category: $sub_category
        ) {
            id
            target_name
            target_description
            target_amount
            target_is_active
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

update_target = gql(
    """
    mutation updateTarget(
        $id: ID!
        $target_name: String!
        $target_description: String!
        $target_amount: String!
        $category: String!
        $sub_category: String!
    ) {
        updateTarget(
            id: $id
            target_name: $target_name
            target_description: $target_description
            target_amount: $target_amount
            category: $category
            sub_category: $sub_category
        ) {
            id
            target_name
            target_description
            target_amount
            target_is_active
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

target_status = gql(
    """
    mutation targetStatus($id: ID!, $status: Boolean!) {
        targetStatus(id: $id, status: $status)
    }
    """
)

delete_target = gql(
    """
    mutation deleteTarget($id: ID!) {
        deleteTarget(id: $id)
    }
    """
)

create_transaction = gql(
    """
    mutation createTransaction(
        $account_id: ID!
        $transaction_type: String!
        $transaction_amount: String!
        $transaction_date: String!
        $description: String!
        $category: String!
        $sub_category: String!
    ) {
        createTransaction(
            account_id: $account_id
            transaction_type: $transaction_type
            transaction_amount: $transaction_amount
            transaction_date: $transaction_date
            description: $description
            category: $category
            sub_category: $sub_category
        ) {
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

update_transaction = gql(
    """
    mutation updateTransaction(
        $id: ID!
        $account_id: ID!
        $transaction_type: String!
        $transaction_amount: String!
        $transaction_date: String!
        $description: String!
        $category: String!
        $sub_category: String!
    ) {
        updateTransaction(
            id: $id
            account_id: $account_id
            transaction_type: $transaction_type
            transaction_amount: $transaction_amount
            transaction_date: $transaction_date
            description: $description
            category: $category
            sub_category: $sub_category
        ) {
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

delete_transaction = gql(
    """
    mutation deleteTransaction($id: ID!, $account_id: ID!) {
        deleteTransaction(id: $id, account_id: $account_id)
    }
    """
)

subscribe_to_plan = gql(
    """
    mutation subscribeToPlan($plan: String!) {
        subscribeToPlan(plan: $plan) {
            id
            customer {
                id
                username
            }
            order_tracking_id
            merchant_ref
            account_ref
            redirect_url
            plan
            currency
            amount
            payment_confirmed
        }
    }
    """
)

create_product = gql(
    """
    mutation createProduct(
        $account_id: ID!
        $name: String!
        $description: String!
        $category: String!
        $sub_category: String!
        $buying_price: String!
        $selling_price: String!
        $current_stock_level: String!
        $units_sold: String!
        $supplier_name: String!
    ) {
        createProduct(
            account_id: $account_id
            name: $name
            description: $description
            category: $category
            sub_category: $sub_category
            buying_price: $buying_price
            selling_price: $selling_price
            current_stock_level: $current_stock_level
            units_sold: $units_sold
            supplier_name: $supplier_name
        ) {
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

update_product = gql(
    """
    mutation updateProduct(
        $id: ID!
        $name: String!
        $description: String!
        $category: String!
        $sub_category: String!
        $buying_price: String!
        $selling_price: String!
        $current_stock_level: String!
        $units_sold: String!
        $supplier_name: String!
    ) {
        updateProduct(
            id: $id
            name: $name
            description: $description
            category: $category
            sub_category: $sub_category
            buying_price: $buying_price
            selling_price: $selling_price
            current_stock_level: $current_stock_level
            units_sold: $units_sold
            supplier_name: $supplier_name
        ) {
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

delete_product = gql(
    """
    mutation deleteProduct($id: ID!) {
        deleteProduct(id: $id)
    }
    """
)

create_payment_account = gql(
    """
    mutation(
        $business_name: String!
        $business_email: String!
        $business_phone_number: String!
        $bank_name: String!
        $bank_account: String!
        $mobile_payment_name: String!
        $mobile_account: String!
    ) {
        createPaymentAccount(
            business_name: $business_name
            business_email: $business_email
            business_phone_number: $business_phone_number
            bank_name: $bank_name
            bank_account: $bank_account
            mobile_payment_name: $mobile_payment_name
            mobile_account: $mobile_account
        ) {
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

update_payment_account = gql(
    """
    mutation(
        $id: ID!
        $business_name: String!
        $business_email: String!
        $business_phone_number: String!
        $bank_name: String!
        $bank_account: String!
        $mobile_payment_name: String!
        $mobile_account: String!
    ) {
        updatePaymentAccount(
            id: $id
            business_name: $business_name
            business_email: $business_email
            business_phone_number: $business_phone_number
            bank_name: $bank_name
            bank_account: $bank_account
            mobile_payment_name: $mobile_payment_name
            mobile_account: $mobile_account
        ) {
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

delete_payment_account = gql(
    """
    mutation($id: ID!) {
        deletePaymentAccount(id: $id)
    }
    """
)

create_client_information = gql(
    """
    mutation(
        $client_name: String!
        $client_email: String!
        $client_phone_number: String!
        $client_address: String!
    ) {
        createClientInformation(
            client_name: $client_name
            client_email: $client_email
            client_phone_number: $client_phone_number
            client_address: $client_address
        ) {
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

update_client_information = gql(
    """
    mutation(
        $id: ID!
        $client_name: String!
        $client_email: String!
        $client_phone_number: String!
        $client_address: String!
    ) {
        updateClientInformation(
            id: $id
            client_name: $client_name
            client_email: $client_email
            client_phone_number: $client_phone_number
            client_address: $client_address
        ) {
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

delete_client_information = gql(
    """
    mutation($id: ID!) {
        deleteClientInformation(id: $id)
    }
    """
)

create_invoice = gql(
    """
    mutation(
        $business: String!
        $client: String!
        $category: String!
        $sub_category: String!
        $item: String!
        $quantity: String!
        $amount: String!
        $additional_notes: String!
        $due_date: String!
    ) {
        createInvoice(
            business: $business
            client: $client
            category: $category
            sub_category: $sub_category
            item: $item
            quantity: $quantity
            amount: $amount
            additional_notes: $additional_notes
            due_date: $due_date
        ) {
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

update_invoice = gql(
    """
    mutation(
        $id: ID!
        $business: String!
        $client: String!
        $category: String!
        $sub_category: String!
        $item: String!
        $quantity: String!
        $amount: String!
        $additional_notes: String!
        $due_date: String!
    ) {
        updateInvoice(
            id: $id
            business: $business
            client: $client
            category: $category
            sub_category: $sub_category
            item: $item
            quantity: $quantity
            amount: $amount
            additional_notes: $additional_notes
            due_date: $due_date
        ) {
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

delete_invoice = gql(
    """
    mutation($id: ID!) {
        deleteInvoice(id: $id)
    }
    """
)

generate_cash_flow_report = gql(
    """
    mutation($account_id: ID!, $begin_date: String!, $end_date: String!) {
        generateCashFlowReport(
            account_id: $account_id
            begin_date: $begin_date
            end_date: $end_date
        ) {
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

delete_cash_flow_report = gql(
    """
    mutation($uid: String!) {
        deleteCashFlowReport(uid: $uid)
    }
    """
)

generate_income_report = gql(
    """
    mutation($account_id: ID!, $begin_date: String!, $end_date: String!) {
        generateIncomeReport(
            account_id: $account_id
            begin_date: $begin_date
            end_date: $end_date
        ) {
            id
            uid
            account {
                id
                account_name
            }
            period_start_date
            period_end_date
            revenue
            gross_profit
            operating_expenses
            net_income
        }
    }
    """
)

delete_income_report = gql(
    """
    mutation($uid: String!) {
        deleteIncomeReport(uid: $uid)
    }
    """
)

generate_balance_sheet_report = gql(
    """
    mutation(
        $account_id: ID!
        $assets: [assets!]!
        $liabilities: [liabilities!]!
        $equity: [equity!]!
    ) {
        generateBalanceSheetReport(
            account_id: $account_id
            assets: $assets
            liabilities: $liabilities
            equity: $equity
        ) {
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

delete_balance_sheet_report = gql(
    """
    mutation($uid: String!) {
        deleteBalanceSheetReport(uid: $uid)
    }
    """
)
