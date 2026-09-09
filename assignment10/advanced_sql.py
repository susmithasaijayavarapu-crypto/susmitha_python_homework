import sqlite3

def get_first_five_order_totals():
    # Connect to SQLite database
    conn = sqlite3.connect("./db/lesson.db")
    cursor = conn.cursor()

    # SQL query to join orders, line items, and products
    sql_query = """
        SELECT 
            orders.order_id,
            SUM(products.price * line_items.quantity) AS total_price
        FROM orders
        JOIN line_items ON orders.order_id = line_items.order_id
        JOIN products ON line_items.product_id = products.product_id
        GROUP BY orders.order_id
        ORDER BY orders.order_id ASC
        LIMIT 5;
    """

    # Execute query and retrieve rows
    cursor.execute(sql_query)
    results = cursor.fetchall()

    # Print header and row results
    print(f"{'Order ID':<10} | {'Total Price':<12}")
    print("-" * 25)
    for order_id, total_price in results:
        print(f"{order_id:<10} | ${total_price:.2f}")

    # Close connection
    conn.close()

def get_customer_average_order_price():
    conn = sqlite3.connect("./db/lesson.db")
    cursor = conn.cursor()

    # Subquery calculates total price per order, main query averages it per customer
    sql_query = """
        SELECT 
            customers.customer_name,
            AVG(order_totals.total_price) AS average_total_price
        FROM customers
        LEFT JOIN (
            SELECT 
                orders.customer_id AS customer_id_b,
                SUM(products.price * line_items.quantity) AS total_price
            FROM orders
            JOIN line_items ON orders.order_id = line_items.order_id
            JOIN products ON line_items.product_id = products.product_id
            GROUP BY orders.order_id
        ) AS order_totals
        ON customers.customer_id = order_totals.customer_id_b
        GROUP BY customers.customer_id;
    """

    cursor.execute(sql_query)
    results = cursor.fetchall()

    print("\n--- Part 2: Customer Average Order Price ---")
    print(f"{'Customer Name':<20} | {'Average Order Price':<20}")
    print("-" * 43)
    for name, avg_price in results:
        formatted_price = f"${avg_price:.2f}" if avg_price is not None else "N/A"
        print(f"{name:<20} | {formatted_price:<20}")

    conn.close()


def create_perez_order():
    conn = sqlite3.connect("./db/lesson.db")
    
    # Enable foreign key constraint checking in SQLite
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()

    try:
        # Start transaction
        conn.execute("BEGIN TRANSACTION;")

        # 1. Retrieve customer_id for 'Perez and Sons'
        cursor.execute("SELECT customer_id FROM customers WHERE customer_name = ?", ('Perez and Sons',))
        customer_row = cursor.fetchone()
        if not customer_row:
            raise ValueError("Customer 'Perez and Sons' not found.")
        customer_id = customer_row[0]

        # 2. Retrieve employee_id for 'Miranda Harris'
       
        cursor.execute(
            "SELECT employee_id FROM employees WHERE first_name = 'Miranda' AND last_name = 'Harris'"
        
        )
        employee_row = cursor.fetchone()
        if not employee_row:
            raise ValueError("Employee 'Miranda Harris' not found.")
        employee_id = employee_row[0]

        # 3. Retrieve product_ids for the 5 least expensive products
        cursor.execute("""
            SELECT product_id 
            FROM products 
            ORDER BY price ASC 
            LIMIT 5;
        """)
        product_rows = cursor.fetchall()
        product_ids = [row[0] for row in product_rows]

        # 4. Insert order record and return order_id
        # Adjust date/order_date columns if required by your schema
        cursor.execute("""
            INSERT INTO orders (customer_id, employee_id)
            VALUES (?, ?)
            RETURNING order_id;
        """, (customer_id, employee_id))
        
        order_id = cursor.fetchone()[0]

        # 5. Insert 5 line_item records (quantity = 10 each)
        for prod_id in product_ids:
            cursor.execute("""
                INSERT INTO line_items (order_id, product_id, quantity)
                VALUES (?, ?, ?);
            """, (order_id, prod_id, 10))

        # Commit transaction to persist changes
        conn.commit()
        print(f"--- Transaction Successful: Order #{order_id} Created ---")

        # 6. Verify and display the created line items using JOIN
        cursor.execute("""
            SELECT 
                line_items.line_item_id,
                line_items.quantity,
                products.product_name
            FROM line_items
            JOIN products ON line_items.product_id = products.product_id
            WHERE line_items.order_id = ?;
        """, (order_id,))

        results = cursor.fetchall()

        print(f"\n{'Line Item ID':<15} | {'Quantity':<10} | {'Product Name':<30}")
        print("-" * 60)
        for item_id, qty, prod_name in results:
            print(f"{item_id:<15} | {qty:<10} | {prod_name:<30}")

    except Exception as e:
        conn.rollback()
        print(f"Transaction failed and rolled back. Error: {e}")

    finally:
        conn.close()


def get_busy_employees():
    conn = sqlite3.connect("./db/lesson.db")
    cursor = conn.cursor()

    sql_query = """
        SELECT 
            employees.employee_id,
            employees.first_name,
            employees.last_name,
            COUNT(orders.order_id) AS order_count
        FROM employees
        JOIN orders ON employees.employee_id = orders.employee_id
        GROUP BY 
            employees.employee_id,
            employees.first_name,
            employees.last_name
        HAVING COUNT(orders.order_id) > 5;
    """

    cursor.execute(sql_query)
    results = cursor.fetchall()

    print("--- Employees with More Than 5 Orders ---")
    print(f"{'ID':<6} | {'First Name':<15} | {'Last Name':<15} | {'Order Count':<12}")
    print("-" * 55)
    
    for emp_id, first_name, last_name, count in results:
        print(f"{emp_id:<6} | {first_name:<15} | {last_name:<15} | {count:<12}")

    conn.close()


if __name__ == "__main__":
    get_first_five_order_totals()
    get_customer_average_order_price()
    create_perez_order()
    get_busy_employees()