from flask import Flask, render_template, request, redirect
import cx_Oracle

app = Flask(__name__)


cx_Oracle.init_oracle_client(lib_dir=r"instantclient-basic-windows.x64-21.12.0.0.0dbru.zip")
connection = cx_Oracle.connect("bd093", "bd093", "bd-dc.cs.tuiasi.ro:1539/orcl")

products = []
suppliers = []
productCategories = []
sales = []
paymentMethods = []
productDetails = []

@app.route('/admin/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product_name = request.form['product_name']
        product_unit_price = float(request.form['product_unit_price'])
        product_quantity = int(request.form['product_quantity'])
        product_brand = request.form['product_brand']
        product_category_name = int(request.form['product_category_name'])
        product_supplier_name = int(request.form['product_supplier_name'])
        product_expiry_date = request.form['product_expiry_date']

        cursor = connection.cursor()

        insert_query = """
            INSERT INTO Products (ProductName, Brand, CategoryName, UnitPrice, QuantityAvailable, SupplierName, ExpiryDate)
            VALUES (:name, :brand, :categoryName, :unitPrice, :quantity, :supplierName, TO_DATE(:expiryDate, 'YYYY-MM-DD'))
        """
        cursor.execute(insert_query, {
            'name': product_name,
            'brand': product_brand,
            'categoryName': product_category_name,
            'unitPrice': product_unit_price,
            'quantity': product_quantity,
            'supplierName': product_supplier_name,
            'expiryDate': product_expiry_date
        })
        connection.commit()
        
        cursor.close()

        return redirect('/admin')

    return render_template('add_product.html')

@app.route('/admin/add_supplier', methods=['GET', 'POST'])
def add_supplier():
    if request.method == 'POST':
        supplier_name = request.form ['supplier_name']
        supplier_email = request.form['supplier_email']
        supplier_phone = request.form['supplier_phone']

        cursor = connection.cursor()

        insert_query = """
            INSERT INTO Suppliers (SupplierName, Email,Phone)
            VALUES (:name, :email, :phone)
        """
        cursor.execute(insert_query,{
            'name': supplier_name,
            'email': supplier_email,
            'phone': supplier_phone
        })

        connection.commit()
        cursor.close()
        return redirect('/admin')

    return render_template('add_supplier.html')

@app.route('/admin/add_product_category', methods=['GET', 'POST'])
def add_product_category():
    if request.method == 'POST':
        category_name = request.form ['category_name']
        category_count = request.form['category_count']
        category_discount = request.form['category_discount']

        cursor = connection.cursor()

        insert_query = """
            INSERT INTO ProductCategories (CategoryName, ProductCount, Discount)
            VALUES (:name, :count, :discount)
        """
        cursor.execute(insert_query,{
            'name': category_name,
            'count': category_count,
            'discount': category_discount
        })

        connection.commit()
        cursor.close()
        return redirect('/admin')

    return render_template('add_product_category.html')
        
@app.route('/admin/add_product_details', methods=['GET', 'POST'])
def add_product_details():
    if request.method == 'POST':
        product_name = request.form['product_name']
        product_weight = request.form['product_weight']
        product_bar_code = request.form['product_bar_code']

        cursor = connection.cursor()

        insert_query = """
            INSERT INTO ProductDetails (ProductName, Weight, BarCode)
            VALUES (:product_name, :product_weight, :product_bar_code)
        """
        cursor.execute(insert_query, {
            'product_name': product_name,
            'product_weight': product_weight,
            'product_bar_code': product_bar_code
        })

        connection.commit()
        cursor.close()
        return redirect('/admin')

    else:
        cursor = connection.cursor()
        cursor.execute("SELECT ProductName FROM Products")
        products = cursor.fetchall()
        product_names = [product[0] for product in products]

        cursor.close()
        return render_template('add_product_details.html', product_names=product_names)

@app.route('/admin/delete_product', methods=['GET', 'POST'])
def delete_product():
    if request.method == 'POST':
        product_name = request.form['product_name']

        cursor = connection.cursor()
        delete_query = "DELETE FROM Products WHERE ProductName = :name"
        cursor.execute(delete_query, {'name': product_name})
        connection.commit()
        cursor.close()
        return redirect('/admin')

    return render_template('delete_product.html')

@app.route('/admin/delete_supplier', methods=['GET', 'POST'])
def delete_supplier():
    if request.method == 'POST':
        supplier_name = request.form['supplier_name']

        cursor = connection.cursor()
        delete_query = "DELETE FROM Suppliers WHERE SupplierName = :name"
        cursor.execute(delete_query, {'name': supplier_name})
        connection.commit()
        cursor.close()
        return redirect('/admin')

    return render_template('delete_supplier.html')

@app.route('/admin/delete_product_category', methods=['GET', 'POST'])
def delete_product_category():
    if request.method == 'POST':
        category_name = request.form['category_name']

        cursor = connection.cursor()
        delete_query = "DELETE FROM ProductCategories WHERE CategoryName = :name"
        cursor.execute(delete_query, {'name': category_name})
        connection.commit()
        cursor.close()
        return redirect('/admin')

    return render_template('delete_product_category.html')

@app.route('/admin/delete_product_details', methods=['GET', 'POST'])
def delete_product_details():
    if request.method == 'POST':
        product_name = request.form['product_name']

        cursor = connection.cursor()
        delete_query = "DELETE FROM ProductDetails WHERE ProductName = :name"
        cursor.execute(delete_query, {'name': product_name})
        cursor.close()
        return redirect('/admin')

    return render_template('delete_product_details.html')

@app.route('/admin/modify_product', methods=['GET', 'POST'])
def modify_product():
if request.method == 'POST':
        product_name = int(request.form['product_name'])
        fields_to_update = request.form.getlist('fields_to_update')

        update_query = "UPDATE Products SET "
        update_values = {}

        for field in fields_to_update:
            if field == 'new_name':
                update_query += "ProductName = :new_name, "
                update_values['new_name'] = request.form.get('new_name')
            elif field == 'new_unit_price':
                update_query += "UnitPrice = :new_unit_price, "
                update_values['new_unit_price'] = float(request.form.get('new_unit_price'))
            elif field == 'new_quantity':
                update_query += "QuantityAvailable = :new_quantity, "
                update_values['new_quantity'] = int(request.form.get('new_quantity'))
            elif field == 'new_brand':
                update_query += "Brand = :new_brand, "
                update_values['new_brand'] = request.form.get('new_brand')
            elif field == 'new_category_name':
                update_query += "CategoryName = :new_category_name, "
                update_values['new_category_name'] = int(request.form.get('new_category_name'))
            elif field == 'new_supplier_name':
                update_query += "SupplierName = :new_supplier_name, "
                update_values['new_supplier_name'] = int(request.form.get('new_supplier_name'))
            elif field == 'new_expiry_date':
                update_query += "ExpiryDate = TO_DATE(:new_expiry_date, 'YYYY-MM-DD'), "
                update_values['new_expiry_date'] = request.form.get('new_expiry_date')

        update_query = update_query.rstrip(', ')

        update_query += " WHERE ProductName = :name"

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Products WHERE ProductName = :name", {'name': product_name})
        product = cursor.fetchone()

        if product:
            cursor.execute(update_query, {**update_values, 'name': product_name})
            connection.commit()
            cursor.close()
            return redirect('/admin')
        else:
            return "Product not found"

    return render_template('modify_product.html')

@app.route('/admin/modify_supplier', methods=['GET', 'POST'])
def modify_supplier():
    if request.method == 'POST':
        supplier_name = int(request.form['supplier_name'])
        fields_to_update = request.form.getlist('fields_to_update')

        update_query = "UPDATE Suppliers SET "
        update_values = {}

        for field in fields_to_update:
            if field == 'new_name':
                update_query += "SupplierName = :new_name, "
                update_values['new_name'] = request.form.get('new_name')
            elif field == 'new_email':
                update_query += "Email = :new_email, "
                update_values['new_email'] = request.form.get('new_email')
            elif field == 'new_phone':
                update_query += "Phone = :new_phone, "
                update_values['new_phone'] = request.form.get('new_phone')

        update_query = update_query.rstrip(', ')

        update_query += " WHERE SupplierName = :name"

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Suppliers WHERE SupplierName = :name", {'name': supplier_name})
        supplier = cursor.fetchone()

        if supplier:
            cursor.execute(update_query, {**update_values, 'name': supplier_name})
            connection.commit()
            cursor.close()
            return redirect('/admin')
        else:
            return "Supplier not found"

    return render_template('modify_supplier.html')

@app.route('/admin/modify_product_category', methods=['GET', 'POST'])
def modify_product_category():
    if request.method == 'POST':
        category_name = int(request.form['category_name'])
        fields_to_update = request.form.getlist('fields_to_update')

        update_query = "UPDATE ProductCategories SET "
        update_values = {}

        for field in fields_to_update:
            if field == 'new_name':
                update_query += "CategoryName = :new_name, "
                update_values['new_name'] = request.form.get('new_name')
            elif field == 'new_count':
                update_query += "ProductCount = :new_count, "
                update_values['new_count'] = request.form.get('new_count')
            elif field == 'new_discount':
                update_query += "Discount = :new_discount, "
                update_values['new_discount'] = request.form.get('new_discount')

        update_query = update_query.rstrip(', ')

        update_query += " WHERE CategoryName = :name"

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM ProductCategories WHERE CategoryName = :name", {'name': category_name})
        category = cursor.fetchone()

        if category:
            cursor.execute(update_query, {**update_values, 'name': category_name})
            connection.commit()
            cursor.close()
            return redirect('/admin')
        else:
            return "Category not found"

    return render_template('modify_product_category.html')

@app.route('/admin/modify_product_details', methods=['GET', 'POST'])
def modify_product_details():
    if request.method == 'POST':
        product_name = int(request.form['product_name'])
        fields_to_update = request.form.getlist('fields_to_update')

        update_query = "UPDATE ProductDetails SET "
        update_values = {}

        for field in fields_to_update:
            if field == 'new_wight':
                update_query += "Weight = :new_wight, "
                update_values['new_wight'] = request.form.get('new_wight')
            elif field == 'new_barcode':
                update_query += "BarCode = :new_barcode, "
                update_values['new_barcode'] = request.form.get('new_barcode')

        update_query = update_query.rstrip(', ')

        update_query += " WHERE ProductName = :name"

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM ProductDetails WHERE ProductName = :name", {'name': product_name})
        category = cursor.fetchone()

        if category:
            cursor.execute(update_query, {**update_values, 'name': product_name})
            connection.commit()
            cursor.close()
            return redirect('/admin')
        else:
            return "Product not found"

    return render_template('modify_product_details.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/buyer')
def buyer():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Products")
    for result in cursor:
        product = {
            'ProductName': result[0],
            'Brand': result[1],
            'CategoryID': result[2],
            'UnitPrice': result[3],
            'QuantityAvailable': result[4],
            'SupplierID': result[5],
            'ExpiryDate': result[6]
        }

        products.append(product)
    cursor.close()

    return render_template('buyer.html', products=products)

@app.route('/admin/show_products')
def show_products():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Products")
    for result in cursor:
        product = {
            'ProductName': result[0],
            'Brand': result[1],
            'CategoryID': result[2],
            'UnitPrice': result[3],
            'QuantityAvailable': result[4],
            'SupplierID': result[5],
            'ExpiryDate': result[6]
        }

        products.append(product)
    cursor.close()

    return render_template('show_products.html', products=products)

@app.route('/admin/show_suppliers')
def show_suppliers():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Suppliers")
    for result in cursor:
        supplier = {
            'SupplierName': result[0],
            'Email': result[1],
            'Phone': result[2]
        }

        suppliers.append(supplier)
    cursor.close()

    return render_template('show_suppliers.html', suppliers=suppliers)

@app.route ('/admin/show_product_categories')
def show_product_categories():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ProductCategories")
    for result in cursor:
        productCategory = {
            'CategoryName': result[0],
            'ProductCount': result[1],
            'Discount': result[2]
        }

        productCategories.append(productCategory)
    cursor.close()

    return render_template('show_product_categories.html', productCategories=productCategories)

@app.route('/admin/show_sales')
def show_sales():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Sales")
    for result in cursor:
        sale = {
            'ProductName': result[0],
            'QuantitySold': result[1],
            'SaleDate': result[2],
            'TotalPrice': result[3]
        }

        sales.append(sale)
    cursor.close()

    return render_template('show_sales.html', sales=sales)

@app.route('/admin/show_payment_methods')
def show_payment_methods():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM PaymentMethods")
    for result in cursor:
        paymentMethod = {
            'MethodName': result[0],
            'TransactionMode': result[1],
            'TransactionStatus': result[2]
        }

        paymentMethods.append(paymentMethod)
    cursor.close()

    return render_template('show_payment_methods.html', paymentMethods=paymentMethods)

@app.route('/admin/show_product_details')
def show_product_details():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ProductDetails")
    for result in cursor:
        productDetail = {
            'ProductName': result[0],
            'Weight': result[1],
            'BarCode': result[2]
        }

        productDetails.append(productDetail)
    cursor.close()

    return render_template('show_product_details.html', productDetails=productDetails)


@app.route('/buyer/add_to_cart', methods=['POST'])
def add_to_cart():

    cursor = connection.cursor()
    product_name = request.form['product_name']
    product_quantity = int(request.form['product_quantity'])
    product_sale_date = request.form['product_sale_date']

    cursor.execute("SELECT ProductQuantity FROM Products WHERE ProductName = :product_name", {'product_name': product_name})
    available_quantity = cursor.fetchone()[0]

    if available_quantity >= product_quantity:
        cursor.execute("BEGIN")

        cursor.execute("""
            INSERT INTO Sales (ProductName, QuantitySold, SaleDate)
            VALUES(:product_name, :product_quantity, TO_DATE(:product_sale_date, 'YYYY_MM_DD'))
        """, {
            'product_name': product_name,
            'product_quantity': product_quantity,
            'product_sale_date': product_sale_date
        })

        cursor.execute("""
            UPDATE Sales
            SET TotalPrice = (
                SELECT UnitPrice * QuantitySold
                FROM Products
                WHERE Sales.ProductName = Products.ProductName
            )
        """)

        connection.commit()

        cursor.close()
        
        return render_template('buyer.html')
    else:
        cursor.close()


@app.route('/buyer/checkout', methods=['GET', 'POST'])
def checkout():

    cursor = connection.cursor()

    cursor.execute("BEGIN")
    cursor.execute("SELECT SUM(TotalPrice) AS TotalPrice FROM Sales")
    total_price = cursor.fetchone()[0] or 0
    cursor.execute("DELETE FROM Sales")
    connection.commit()
    cursor.close()

    return render_template('buyer.html', total_price=total_price)

@app.route('/buyer/purchase', methods=['POST'])
def purchase():
cursor = connection.cursor()

    cursor.execute("BEGIN")
    get_quantity_sold_query = """
        SELECT ProductName, SUM(QuantitySold) 
        FROM Sales
        GROUP BY ProductName
    """
    cursor.execute(get_quantity_sold_query)
    quantities_sold = cursor.fetchall()

    update_products_query = """
        UPDATE Products 
        SET QuantityAvailable = QuantityAvailable - :quantity_sold
        WHERE ProductName = :product_name
    """
    for product_id, quantity_sold in quantities_sold:
        cursor.execute(update_products_query, {'quantity_sold': quantity_sold, 'product_name': product_name})

    delete_sales_query = "DELETE FROM Sales"
    cursor.execute(delete_sales_query)

    connection.commit()

    cursor.close()

    return redirect(url_for('buyer'))

@app.route ('/buyer/payment_method', methods =['POST'])
def payment_method():
    payment_method = request.form['payment_method']
    payment_transaction_status = request.form['payment_transaction_status']
    cursor = connection.cursor()

    insert_query = """
        INSERT INTO PaymentMethods (MethodName, TransactionMode, TransactionStatus)
        VALUES (:method_name, :transaction_mode, :transaction_status)
    
    """
    cursor.execute(insert_query , {
        'method_name': payment_method,
        'transaction_mode': 'online',
        'transaction_status': payment_transaction_status
    })
    connection.commit()
    cursor.close()
        
    return redirect('/buyer')
    


if __name__ == '__main__':
    app.run(debug=True)
    connection.close()

