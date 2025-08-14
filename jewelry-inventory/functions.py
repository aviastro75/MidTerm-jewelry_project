"""
Jewelry Shop Inventory Management 
Functions File
"""
import sqlite3

db_path = '/var/www/flask_app/inventory.db'


def main_menu_handler():  # Menu Handler function
    print("\n   Main Menu")
    print("1️⃣  Add New Item")
    print("2️⃣  Show current inventory")
    print("3️⃣  Mark Item as Sold")
    print("4️⃣  Update item")
    print("5️⃣  Calculate profit summary")
    print("6️⃣  Get inventory summary")
    print("7️⃣  Quit")


def add_jewelry_item(item_type, category, cost_price):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        INSERT INTO inventory (type, category, cost_price, selling_price, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (item_type, category, round(cost_price, 2), None, 'available'))
    conn.commit()
    item_id = c.lastrowid
    new_item = {
        "id": item_id,
        "type": item_type,
        "category": category,
        "cost_price": round(cost_price, 2),
        "selling_price": None,
        "status": "available"
    }
    conn.close()
    return new_item


def mark_item_sold(item_id, selling_price):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT * FROM inventory WHERE id = ? AND status = ?',
              (item_id, 'available'))
    item = c.fetchone()
    if item:
        c.execute('UPDATE inventory SET status = ?, selling_price = ? WHERE id = ?',
                  ('sold', round(float(selling_price), 2), item_id))
        conn.commit()
        updated_item = {
            'id': item[0],
            'type': item[1],
            'category': item[2],
            'cost_price': item[3],
            'selling_price': round(float(selling_price), 2),
            'status': 'sold'
        }
        conn.close()
        return updated_item
    conn.close()
    return None


def calculate_profit_summary():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT * FROM inventory')
    inventory = [
        {
            'id': row[0],
            'type': row[1],
            'category': row[2],
            'cost_price': row[3],
            'selling_price': row[4],
            'status': row[5]
        } for row in c.fetchall()
    ]
    total_cost_all = sum(item['cost_price'] for item in inventory)
    total_cost_available = sum(
        item['cost_price'] for item in inventory if item['status'] == 'available')
    total_cost_sold = sum(item['cost_price']
                          for item in inventory if item['status'] == 'sold')
    total_revenue = sum(item['selling_price'] for item in inventory if item['status']
                        == 'sold' and item.get('selling_price') is not None)
    total_profit = total_revenue - total_cost_sold

    profit_per_item = [
        {
            'id': item['id'],
            'type': item['type'],
            'profit': round(item['selling_price'] - item['cost_price'], 2)
        }
        for item in inventory
        if item['status'] == 'sold' and item.get('selling_price') is not None
    ]

    conn.close()
    return {
        'total_cost_all': round(total_cost_all, 2),
        'total_cost_available': round(total_cost_available, 2),
        'total_cost_sold': round(total_cost_sold, 2),
        'total_revenue': round(total_revenue, 2),
        'total_profit': round(total_profit, 2),
        'profit_per_item': profit_per_item
    }


def update_item(item_id, updated_data):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT * FROM inventory WHERE id = ?', (item_id,))
    item = c.fetchone()
    if item:
        updated_fields = []
        values = []
        for key, value in updated_data.items():
            updated_fields.append(f"{key} = ?")
            values.append(value)
        values.append(item_id)
        if updated_fields:
            c.execute(
                f"UPDATE inventory SET {', '.join(updated_fields)} WHERE id = ?", values)
            conn.commit()
        c.execute('SELECT * FROM inventory WHERE id = ?', (item_id,))
        updated_item = c.fetchone()
        conn.close()
        return {
            'id': updated_item[0],
            'type': updated_item[1],
            'category': updated_item[2],
            'cost_price': updated_item[3],
            'selling_price': updated_item[4],
            'status': updated_item[5]
        }
    conn.close()
    return None


def show_current_inventory():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT * FROM inventory')
    inventory = [
        {
            'id': row[0],
            'type': row[1],
            'category': row[2],
            'cost_price': row[3],
            'selling_price': row[4],
            'status': row[5]
        } for row in c.fetchall()
    ]
    conn.close()
    return inventory
