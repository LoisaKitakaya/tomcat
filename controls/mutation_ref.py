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
        $workspace_name: String!
        $password: String!
        $password2: String!
    ) {
        createUser(
            email: $email
            first_name: $first_name
            last_name: $last_name
            workspace_name: $workspace_name
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
        $account_balance: Float!
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
                phone_number
                is_employee
                is_paid_user
            }
            workspace {
                id
                name
                workspace_uid
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
        $account_balance: Float!
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
                phone_number
                is_employee
                is_paid_user
            }
            workspace {
                id
                name
                workspace_uid
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
        $budget_amount: Float!
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
            workspace {
                id
                name
                workspace_uid
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
        $budget_amount: Float!
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
            workspace {
                id
                name
                workspace_uid
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
        $target_amount: Float!
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
            workspace {
                id
                name
                workspace_uid
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
        $target_amount: Float!
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
            workspace {
                id
                name
                workspace_uid
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
        $transaction_amount: Float!
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
        $transaction_amount: Float!
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

update_workspace = gql(
    """
    mutation updateWorkspace($name: String!) {
        updateWorkspace(name: $name) {
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

create_team_member = gql(
    """
    mutation createTeamMember(
        $email: String!
        $first_name: String!
        $last_name: String
        $password: String!
    ) {
        createTeamMember(
            email: $email
            first_name: $first_name
            last_name: $last_name
            password: $password
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

delete_team_member = gql(
    """
    mutation deleteTeamMember($member_id: ID!) {
        deleteTeamMember(member_id: $member_id)
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
        $buying_price: Float!
        $selling_price: Float!
        $current_stock_level: Int!
        $units_sold: Int!
        $reorder_level: Int!
        $supplier_name: String!
        $supplier_phone_number: String!
        $supplier_email: String!
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
            reorder_level: $reorder_level
            supplier_name: $supplier_name
            supplier_phone_number: $supplier_phone_number
            supplier_email: $supplier_email
        ) {
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
        $buying_price: Float!
        $selling_price: Float!
        $current_stock_level: Int!
        $units_sold: Int!
        $reorder_level: Int!
        $supplier_name: String!
        $supplier_phone_number: String!
        $supplier_email: String!
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
            reorder_level: $reorder_level
            supplier_name: $supplier_name
            supplier_phone_number: $supplier_phone_number
            supplier_email: $supplier_email
        ) {
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
