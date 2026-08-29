# Double-Entry General Ledger: Formal Mathematical Proofs & Invariants

## 1. Fundamental Accounting Equation
$$\text{Assets} = \text{Liabilities} + \text{Equity} + (\text{Revenues} - \text{Expenses})$$

## 2. Invariant Proofs
For every Journal Entry $J = \{ L_1, L_2, \dots, L_n \}$:

$$\sum_{i=1}^{n} \text{Debit}(L_i) - \sum_{i=1}^{n} \text{Credit}(L_i) = 0$$

If any journal entry attempts to persist where $\Delta \neq 0$, the database transaction is immediately aborted with `ERR_PAYMENT_LEDGER_UNBALANCED`.
