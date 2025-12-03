from db import get_connection


# -----------------------------
# Get all departments
# -----------------------------
def get_departments():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT dept_name FROM departments")
    rows = [row["dept_name"] for row in cur.fetchall()]
    conn.close()
    return rows


# -----------------------------
# Get historical budget data
# -----------------------------
def get_budget_by_department(dept):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT month, amount
        FROM budget_data
        JOIN departments 
        ON budget_data.dept_id = departments.dept_id
        WHERE dept_name = ?
        ORDER BY month
    """, (dept,))
    rows = cur.fetchall()
    conn.close()
    return rows


# -----------------------------
# Get forecast data
# -----------------------------
def get_forecast_by_department(dept):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT month, predicted_amount
        FROM forecast_data
        JOIN departments 
        ON forecast_data.dept_id = departments.dept_id
        WHERE dept_name = ?
        ORDER BY month
    """, (dept,))
    rows = cur.fetchall()
    conn.close()
    return rows


# -----------------------------
# Get variance (actual vs forecast)
# -----------------------------
def get_variance_by_department(dept):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            f.month AS forecast_month,
            b.month AS actual_month,
            b.amount AS actual,
            f.predicted_amount AS forecast,
            (f.predicted_amount - b.amount) AS variance,
            ((f.predicted_amount - b.amount) * 100.0 / b.amount) AS variance_percent
        FROM forecast_data f
        JOIN budget_data b 
            ON SUBSTR(f.month, 6, 2) = SUBSTR(b.month, 6, 2)
            AND f.dept_id = b.dept_id
        JOIN departments d 
            ON d.dept_id = f.dept_id
        WHERE d.dept_name = ?
        ORDER BY f.month
    """, (dept,))

    rows = cur.fetchall()
    conn.close()
    return rows
