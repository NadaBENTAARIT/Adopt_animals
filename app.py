from config_db import get_db
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request,g,session,jsonify

from flask import render_template, redirect, url_for,session
from sessionManagment import UserLogged
from flask_toastr import Toastr
from flask import flash
import base64
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash
from jinja2 import Template, Environment, FileSystemLoader


app = Flask(__name__)


toastr = Toastr(app)
app.secret_key = "SecretKey"


#***************************************** Details product
@app.route('/ProductDetails/<int:id_product>', methods=['GET', 'POST'])
def ProductDetails(id_product):
    # Créez un curseur pour exécuter les commandes SQL
    logged_in = UserLogged()
    mydb = get_db()
    mycursor = mydb.cursor()

    # Exécutez une instruction SQL pour récupérer le produit spécifié par l'ID
    sql = "SELECT product.*, client.username as client_username, category.name as category_name, subcategory.name as subcategory_name FROM product \
           INNER JOIN client ON product.id_client = client.id \
           INNER JOIN category ON product.id_category = category.id \
           INNER JOIN subcategory ON product.id_subcategory = subcategory.id \
           WHERE product.id = %s"


           
    val = (id_product, )
    mycursor.execute(sql, val)

    products = []
    
    for row in mycursor.fetchall():
        product = {
            'id': row[0],
            'name': row[1],
            'description': row[2],
            'date': row[3],
            'governorate': row[4],
            'weight': row[5],
            'gender': row[6],
            'encoded_image': base64.b64encode(row[7]).decode(),
            'quantity': row[8],
            'date_expiration': row[9],
            'color': row[10],
            'size' : row[11],
            'id_client' : row[12],
            'client_name': row[15],  # Récupération de la valeur de client_name
            'category_name': row[16],
            'subcategory_name': row[17],
           
            
        }
        print("*************************************")
        test=product['client_name']
        print(test)

        products.append(product)
        
   
    mycursor.close()
    mydb.close()

    return render_template('details.html', products=products,logged_in=logged_in)


    















#***************************************** My favorits ( add and delete)

@app.route('/addfavorites/<int:id_product>', methods=['GET', 'POST'])
def addfavorites(id_product):

    logged_in = UserLogged()
    print("**************************************")
    print(logged_in)

   
  
    if 'email' not in session:
        return redirect(url_for('login'))
    else:
        email = session['id']
        print(email)        
        db = get_db()
        cursor = db.cursor()
    # Vérifier si la ligne existe déjà dans la table
        cursor.execute('SELECT id FROM favorites WHERE id_client = %s AND id_product = %s', (email, id_product))
        existing_row = cursor.fetchone()

        if existing_row is not None:
            # La ligne existe déjà dans la table, ne rien faire
            flash('Product is yet in your favorite list', 'danger')
            return redirect(url_for('ListAllProducts'))
        # La ligne n'existe pas encore dans la table, insérer les données
        cursor.execute('INSERT INTO favorites (id_client,id_product) VALUES (%s, %s)',
                    (email, id_product))
        flash('Product inserted successfully in your favorite list ', 'success')

        db.commit()

        cursor.close()
        db.close()

        return redirect(url_for('ListAllProducts'))

  






@app.route('/ListAllFavorites', methods=['GET'])
def ListAllFavorites():
    logged_in = UserLogged()
    email = session['id']
    print(email)
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
    SELECT p.* FROM product p
    INNER JOIN favorites f ON p.id = f.id_product
    WHERE f.id_client = %s
    ''', (email,))
    products = []

    for row in cursor.fetchall():
        product = {
            'id': row[0],
            'name': row[1],
            'description': row[2],
            'date': row[3],
            'governorate': row[4],
            'weight': row[5],
            'gender': row[6],
            'encoded_image': base64.b64encode(row[7]).decode(),
            'quantity': row[8],
            'date_expiration': row[9],
            'color': row[10],
            'size': row[11]
        }
        products.append(product)

    cursor.close()
    db.close()

    return render_template('favorites.html', products=products, logged_in=logged_in)





@app.route('/delete_favorite/<int:id_product>', methods=['POST'])
def delete_favorite(id_product):
    # Créez un curseur pour exécuter les commandes SQL
    logged_in = UserLogged()
    email = session['id']

    mydb = get_db()
    mycursor = mydb.cursor()

    # Exécutez une instruction SQL pour supprimer le produit spécifié par l'ID
    sql = "DELETE FROM favorites WHERE id_product = %s AND id_client= %s"
    val = (id_product, email)
    mycursor.execute(sql, val)

    # Enregistrez les modifications dans la base de données
    mydb.commit()

    # Vérifiez si le produit a été supprimé
    if mycursor.rowcount > 0:
        flash('Product deleted successfully from your favorite list ', 'success')
    else:
        flash('Product not deleted successfully from your favorite list', 'danger')

    # Rediriger vers la page des favoris avec un message de confirmation
    return redirect(url_for('ListAllFavorites'))



#***************************************** Send message
#***************************************** My messages







#***************************************** Products for index

@app.route('/ListAllProducts', methods=['GET'])
def ListAllProducts():
    logged_in = UserLogged()
    db = get_db()
    animals = []
    foods = []
    accessories = []

    cursor = db.cursor()
    cursor.execute('''
        SELECT * FROM product p
        JOIN category c ON p.id_category = c.id
        WHERE c.name = "animals"
        ORDER BY p.date DESC
    ''')

    for row in cursor.fetchall():
        animal = {
            'id': row[0],
            'name': row[1],
            'description': row[2],
            'date': row[3],
            'governorate': row[4],
            'weight': row[5],
            'gender': row[6],
            'encoded_image': base64.b64encode(row[7]).decode() ,
            'id_client': row[12],
    
        }
        animals.append(animal)

    cursor.execute('''
        SELECT * FROM product p
        JOIN category c ON p.id_category = c.id
        WHERE c.name = "food"
        ORDER BY p.date DESC
    ''')

    for row in cursor.fetchall():
        food = {
            'id': row[0],
            'name': row[1],
            'description': row[2],
            'date': row[3],
            'governorate': row[4],
            'quantity': row[8],
            'date_expiration': row[9],
            'encoded_image': base64.b64encode(row[7]).decode(),
            'id_client': row[12],
     
        }
        foods.append(food)

    cursor.execute('''
        SELECT * FROM product p
        JOIN category c ON p.id_category = c.id
        WHERE c.name = "accessories"
        ORDER BY p.date DESC
    ''')    

    for row in cursor.fetchall():
        accessory = {
            'id': row[0],
            'name': row[1],
            'description': row[2],
            'date': row[3],
            'governorate': row[4],
            'color': row[10],
            'size': row[11],
            'encoded_image': base64.b64encode(row[7]).decode(),
            'id_client': row[12]
   
        }
        accessories.append(accessory)

    cursor.close()
    db.close()

    return render_template('index.html',animals=animals,foods=foods,accessories=accessories,logged_in=logged_in)






#********************************************************** My posts


# list all posts and categories list
@app.route('/ListAllPosts', methods=['GET'])
def ListAllPosts():
    logged_in = UserLogged()
    email=session['id']
    print(email)
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
    SELECT * FROM product p
    WHERE id_client = %s
    ''', (email,))
    products = []

    for row in cursor.fetchall():
        product = {
            'id': row[0],

            'name': row[1],
            'description': row[2],
            'date': row[3],
            'governorate': row[4],
            'weight': row[5],
            'gender': row[6],
            'encoded_image': base64.b64encode(row[7]).decode(),
            'quantity': row[8],
            'date_expiration': row[9],
            'color': row[10],
            'size' : row[11]



  
        }
        products.append(product)


    cursor.execute('''
        SELECT c.name FROM category c
        
    ''')
    categories = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template('posts.html', products=products, categories=categories, logged_in=logged_in)



@app.route('/ListAllPostsFiltered', methods=['GET', 'POST'])
def ListAllPostsFiltered():
    logged_in = UserLogged()
    db = get_db()
    cursor = db.cursor()

    # Récupérer les paramètres de filtrage de la requête POST
    governorate = request.form.get('location', False)
    date = request.form.get('date', False)
    category_name = request.args.get('category',False)
    keyword = request.args.get('keyword', False)

    #!!!!!!!!!!   kamel ekteb les attributs l kol

    # Construire la requête SQL en fonction des paramètres de filtrage
    query = "SELECT * FROM product p \
         JOIN category c ON p.id_category = c.id \
         WHERE p.id_client = %s"

    if category_name:
        query += f" AND c.name = '{category_name}'"
    
    if governorate and governorate != "all":
        query += f" AND governorate = '{governorate}'"
    if date is not False:
        try:
            date_form = datetime.strptime(date, '%Y-%m-%d').date()
            query += f" AND date = '{date_form}'"
        except ValueError:
            print("La date fournie n'est pas au format attendu (YYYY-MM-DD)")
    
    if keyword:
        query += f" AND (p.name LIKE '%{keyword}%' OR p.description LIKE '%{keyword}%')"
    query += " ORDER BY p.date DESC"

    cursor.execute(query, (session['id'],))

    products = []
    for row in cursor.fetchall():
        product = {
            'id': row[0],
            'name': row[1],
            'description': row[2],
            'date': row[3],
            'governorate': row[4],
            'weight': row[5],
            'gender': row[6],
            'encoded_image': base64.b64encode(row[7]).decode(),
            'id_client': row[12],
            'color': row[10],
            'size': row[11],
            'quantity': row[8],
            'date_expiration': row[9],
            
  
        }
        products.append(product)

    cursor.execute('''
        SELECT c.name FROM category c
    ''')
    categories = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template('posts.html', products=products, categories=categories, logged_in=logged_in)


@app.route('/delete_post/<int:id_product>', methods=['POST'])
def delete_post(id_product):
    # Créez un curseur pour exécuter les commandes SQL
    logged_in = UserLogged()
    mydb = get_db()
    mycursor = mydb.cursor()

    # Exécutez une instruction SQL pour supprimer le produit spécifié par l'ID
    sql = "DELETE FROM product WHERE id = %s"
    val = (id_product, )
    mycursor.execute(sql, val)

    # Enregistrez les modifications dans la base de données
    mydb.commit()

    # Vérifiez si le produit a été supprimé
    if mycursor.rowcount > 0:
        flash('Product deleted successfully from your posts', 'success')
    else:
        flash('Product not deleted successfully from your posts', 'danger')

    # Rediriger vers la page des posts avec un message de confirmation
    return redirect(url_for('ListAllPosts'))
# ********************************************************* Donate Animals


@app.route('/donateanimals', methods=['GET', 'POST'])
def donateanimals():
    logged_in = UserLogged()
    print(logged_in)

    email = session['id']
    print(email)
    if not email:
        return redirect(url_for('signin'))
    else:
       
    
            # Vérifier si la méthode HTTP est POST (utilisateur a soumis le formulaire)
            if request.method == 'POST':
                # Récupérer les données du formulaire
                name = request.form.get('name')
                gender= request.form.get('gender')
                print (name)
                description = request.form.get('description')
                governorate= request.form.get('governorate')
                date = datetime.now()

                weight = request.form.get('weight')
                #image = request.form.get('image')
                file = request.files['image']
                file_contents = file.read()
                subcategory=request.form.get('subcategory')
                
               

    # lire le contenu du fichier et le stocker dans une variable bytes


                # Établir une connexion à la base de données
                db = get_db()
                cursor = db.cursor()


                # Récupérer l'id de la sous-catégorie sélectionnée
                cursor.execute('SELECT id FROM subcategory WHERE name = %s', (subcategory,))
                id_subcategory = cursor.fetchone()[0]


                # Insérer les données dans la table de produits
                cursor.execute('INSERT INTO product (id_client,id_category,id_subcategory,name,description,weight,image,date,governorate,gender) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s,%s)',
                            (email,1,id_subcategory,name,description,weight,file_contents,date,governorate,gender))


                db.commit()
                cursor.close()
                db.close()

                # Rediriger l'utilisateur vers la page de liste des produits
                return redirect(url_for('ListAllAnimals'))

            # Si la méthode HTTP est GET, afficher le formulaire
            else:
                return render_template('donateanimals.html',logged_in=logged_in)





# ********************************************************* Donate Food


@app.route('/donatefood', methods=['GET', 'POST'])
def donatefood():
    logged_in = UserLogged()
    print(logged_in)

    email = session['id']
    print(email)
    if not email:
        return redirect(url_for('signin'))
    else:
       
    
            # Vérifier si la méthode HTTP est POST (utilisateur a soumis le formulaire)
            if request.method == 'POST':
                # Récupérer les données du formulaire
                name = request.form.get('name')
                description = request.form.get('description')
                governorate= request.form.get('governorate')
                date = datetime.now()

                quantity = request.form.get('quantity')
                date_expiration = request.form.get('date_expiration')
                #image = request.form.get('image')
                file = request.files['image']
                file_contents = file.read()
                subcategory=request.form.get('subcategory')
                
               

    # lire le contenu du fichier et le stocker dans une variable bytes


                # Établir une connexion à la base de données
                db = get_db()
                cursor = db.cursor()


                # Récupérer l'id de la sous-catégorie sélectionnée
                cursor.execute('SELECT id FROM subcategory WHERE name = %s', (subcategory,))
                id_subcategory = cursor.fetchone()[0]


                # Insérer les données dans la table de produits
                cursor.execute('INSERT INTO product (id_client,id_category,id_subcategory,name,description,quantity,image,date,governorate,date_expiration) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s,%s)',
                            (email,3,id_subcategory,name,description,quantity,file_contents,date,governorate,date_expiration))


                db.commit()
                cursor.close()
                db.close()

                # Rediriger l'utilisateur vers la page de liste des produits
                return redirect(url_for('ListAllFood'))

            # Si la méthode HTTP est GET, afficher le formulaire
            else:
                return render_template('donatefood.html',logged_in=logged_in)





# ********************************************************* Donate Accessory


@app.route('/donateaccessories', methods=['GET', 'POST'])
def donateaccessories():
    logged_in = UserLogged()
    print(logged_in)

    email = session['id']
    print(email)
    if not email:
        return redirect(url_for('signin'))
    else:
       
    
            # Vérifier si la méthode HTTP est POST (utilisateur a soumis le formulaire)
            if request.method == 'POST':
                # Récupérer les données du formulaire
                name = request.form.get('name')
                description = request.form.get('description')
                governorate= request.form.get('governorate')
                date = datetime.now()
                color = request.form.get('color')

                size = request.form.get('size')
                #image = request.form.get('image')
                file = request.files['image']
                file_contents = file.read()
                subcategory=request.form.get('subcategory')
                
               

    # lire le contenu du fichier et le stocker dans une variable bytes


                # Établir une connexion à la base de données
                db = get_db()
                cursor = db.cursor()


                # Récupérer l'id de la sous-catégorie sélectionnée
                cursor.execute('SELECT id FROM subcategory WHERE name = %s', (subcategory,))
                id_subcategory = cursor.fetchone()[0]


                # Insérer les données dans la table de produits
                cursor.execute('INSERT INTO product (id_client,id_category,id_subcategory,name,description,size,image,date,governorate,color) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s,%s)',
                            (email,2,id_subcategory,name,description,size,file_contents,date,governorate,color))


                db.commit()
                cursor.close()
                db.close()

                # Rediriger l'utilisateur vers la page de liste des produits
                return redirect(url_for('ListAllAccessories'))

            # Si la méthode HTTP est GET, afficher le formulaire
            else:
                return render_template('donateaccessories.html',logged_in=logged_in)



   
# ********************************************************* Welcome







# ********************************************************* List Animals


# list all animals and subcategories list
@app.route('/ListAllAnimals', methods=['GET'])
def ListAllAnimals():
    logged_in = UserLogged()
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        SELECT * FROM product p
        JOIN category c ON p.id_category = c.id
        WHERE c.name = "animals"
        ORDER BY p.date DESC

    ''')    
    products = []

    for row in cursor.fetchall():
        product = {
            'id':row[0],
            'name': row[1],
            'description': row[2],
            'date': row[3],
            'governorate': row[4],
            'weight': row[5],
            'gender': row[6],
            'encoded_image': base64.b64encode(row[7]).decode()     
        }
        products.append(product)

    cursor.execute('''
        SELECT s.name FROM subcategory s
        JOIN category c ON s.id_category = c.id
        WHERE c.name = "animals"
    ''')
    subcategories = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template('animals.html', products=products, subcategories=subcategories, logged_in=logged_in)




















@app.route('/ListAllAnimalsFiltered', methods=['GET', 'POST'])
def ListAllAnimalsFiltered():
    logged_in = UserLogged()
    db = get_db()
    cursor = db.cursor()

    # Récupérer les paramètres de filtrage de la requête POST
    governorate = request.form.get('location', False)
    date = request.form.get('date', False)
    subcategory = request.args.get('subcategory', '')

    # Construire la requête SQL en fonction des paramètres de filtrage
    query = "SELECT * FROM product p \
             JOIN category c ON p.id_category = c.id \
             JOIN subcategory s ON p.id_subcategory = s.id \
             WHERE c.name = 'animals'"

    if governorate and governorate != "all":
        query += f" AND governorate = '{governorate}'"
    if date is not False:
        try:
            date_form = datetime.strptime(date, '%Y-%m-%d').date()
            query += f" AND date = '{date_form}'"
        except ValueError:
            print("La date fournie n'est pas au format attendu (YYYY-MM-DD)")
    if subcategory:
        query += f" AND s.name = '{subcategory}'"
    query += " ORDER BY p.date DESC"

    
    cursor.execute(query)
    products = []
    for row in cursor.fetchall():
        product = {
            'id': row[0],

            'name': row[1],
            'description': row[2],
            'date': row[3],
            'governorate': row[4],
            'weight': row[5],
            'gender': row[6],
            'encoded_image': base64.b64encode(row[7]).decode(),
  
        }
        products.append(product)

    cursor.execute('''
        SELECT s.name FROM subcategory s
        JOIN category c ON s.id_category = c.id
        WHERE c.name = "animals"
    ''')
    subcategories = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template('animals.html', products=products, subcategories=subcategories, logged_in=logged_in)







# ********************************************************* List Food


# list all animals and subcategories list
@app.route('/ListAllFood', methods=['GET'])
def ListAllFood():
    logged_in = UserLogged()
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        SELECT * FROM product p
        JOIN category c ON p.id_category = c.id
        WHERE c.name = "food"
        ORDER BY p.date DESC

    ''')    
    products = []

    for row in cursor.fetchall():
        product = {
            'id':row[0],
            'name': row[1],
            'description': row[2],
            'date': row[3],
            'governorate': row[4],
            'quantity': row[8],
            'encoded_image': base64.b64encode(row[7]).decode(),
            'date_expiration': row[9],
    
        }
        products.append(product)

    cursor.execute('''
        SELECT s.name FROM subcategory s
        JOIN category c ON s.id_category = c.id
        WHERE c.name = "food"
    ''')
    subcategories = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template('food.html', products=products, subcategories=subcategories, logged_in=logged_in)



















@app.route('/ListAllFoodFiltered', methods=['GET', 'POST'])
def ListAllFoodFiltered():
    logged_in = UserLogged()
    db = get_db()
    cursor = db.cursor()

    # Récupérer les paramètres de filtrage de la requête POST
    governorate = request.form.get('location', False)
    date = request.form.get('date', False)
    subcategory = request.args.get('subcategory', '')

    # Construire la requête SQL en fonction des paramètres de filtrage
    query = "SELECT * FROM product p \
             JOIN category c ON p.id_category = c.id \
             JOIN subcategory s ON p.id_subcategory = s.id \
             WHERE c.name = 'food'"

    if governorate and governorate != "all":
        query += f" AND governorate = '{governorate}'"
    if date is not False:
        try:
            date_form = datetime.strptime(date, '%Y-%m-%d').date()
            query += f" AND date = '{date_form}'"
        except ValueError:
            print("La date fournie n'est pas au format attendu (YYYY-MM-DD)")
    if subcategory:
        query += f" AND s.name = '{subcategory}'"
    query += " ORDER BY p.date DESC"

    
    cursor.execute(query)
    products = []
    for row in cursor.fetchall():
        product = {
            'id':row[0],
            'name': row[1],
            'description': row[2],
            'date': row[3],
            'governorate': row[4],
            'date_expiration': row[9],
            'quantity': row[8],
           
            'encoded_image': base64.b64encode(row[7]).decode(),
  
        }
        products.append(product)

    cursor.execute('''
        SELECT s.name FROM subcategory s
        JOIN category c ON s.id_category = c.id
        WHERE c.name = "food"
    ''')
    subcategories = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template('food.html', products=products, subcategories=subcategories, logged_in=logged_in)






# ********************************************************* List Animals


# list all animals and subcategories list
@app.route('/ListAllAccessories', methods=['GET'])
def ListAllAccessories():
    logged_in = UserLogged()
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        SELECT * FROM product p
        JOIN category c ON p.id_category = c.id
        WHERE c.name = "accessories"
        ORDER BY p.date DESC

    ''')    
    products = []

    for row in cursor.fetchall():
        product = {
            'id':row[0],
            'name': row[1],
            'description': row[2],
            'date': row[3],
            'governorate': row[4],
            'color': row[10],
            'size': row[11],
            'encoded_image': base64.b64encode(row[7]).decode()



           


        }
        products.append(product)

    cursor.execute('''
        SELECT s.name FROM subcategory s
        JOIN category c ON s.id_category = c.id
        WHERE c.name = "accessories"
    ''')
    subcategories = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template('accessories.html', products=products, subcategories=subcategories, logged_in=logged_in)




















@app.route('/ListAllAccessoriesFiltered', methods=['GET', 'POST'])
def ListAllAccessoriesFiltered():
    logged_in = UserLogged()
    db = get_db()
    cursor = db.cursor()

    # Récupérer les paramètres de filtrage de la requête POST
    governorate = request.form.get('location', False)
    date = request.form.get('date', False)
    subcategory = request.args.get('subcategory', '')

    # Construire la requête SQL en fonction des paramètres de filtrage
    query = "SELECT * FROM product p \
             JOIN category c ON p.id_category = c.id \
             JOIN subcategory s ON p.id_subcategory = s.id \
             WHERE c.name = 'accessories'"

    if governorate and governorate != "all":
        query += f" AND governorate = '{governorate}'"
    if date is not False:
        try:
            date_form = datetime.strptime(date, '%Y-%m-%d').date()
            query += f" AND date = '{date_form}'"
        except ValueError:
            print("La date fournie n'est pas au format attendu (YYYY-MM-DD)")
    if subcategory:
        query += f" AND s.name = '{subcategory}'"
    query += " ORDER BY p.date DESC"

    
    cursor.execute(query)
    products = []
    for row in cursor.fetchall():
        product = {
            'id':row[0],
            'name': row[1],
            'description': row[2],
            'date': row[3],
            'governorate': row[4],
            'color': row[10],
            'size': row[11],
            'encoded_image': base64.b64encode(row[7]).decode(),
  
        }
        products.append(product)

    cursor.execute('''
        SELECT s.name FROM subcategory s
        JOIN category c ON s.id_category = c.id
        WHERE c.name = "accessories"
    ''')
    subcategories = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template('accessories.html', products=products, subcategories=subcategories, logged_in=logged_in)





# ********************************************************* Connection


# list all clients
@app.route('/listclients',methods=['GET', 'POST'])
def get_users():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''SELECT id, username, email FROM client''')
    clients = cursor.fetchall()
    cursor.close()
    db.close()

    return jsonify({'clients': clients}), 200


# Login route
@app.route('/signin',methods=['GET', 'POST'])
def login():
    errors = {}

    logged_in = UserLogged()
    if request.method == 'POST':

            email = request.form.get('email', False)
            password = request.form.get('password', False)
            
            # Check if email is valid
            db = get_db()
            cursor = db.cursor(buffered=True)

            query = "SELECT * FROM client WHERE email=%s"
            cursor.execute(query, (email,))
            result = cursor.fetchone()
            if not result:
                errors['email'] = 'The email you entered is not connected to an account.'

                return render_template('signin.html',logged_in=logged_in,errors=errors)
            
            # Check if password is valid
            query = "SELECT * FROM client WHERE email=%s AND password=%s"
            cursor.execute(query, (email, password))
            result = cursor.fetchone()
            if result:
                # Store user ID in session
                session['id'] = result[0]
                session['email'] = result[1]
                session['tel'] = result[4]

                session['username'] = result[3]
                print("******")
                print(logged_in)
                return redirect("/ListAllProducts") 
                
            
            else:
                # Return error message if password is invalid
                errors['password'] = 'The password you have entered is incorrect.'

                return render_template('signin.html',logged_in=logged_in,errors=errors)
    return render_template('signin.html',logged_in=logged_in,errors=errors)


@app.route('/signup',methods=['GET', 'POST'])
def signup():
    errors = {}

    logged_in = UserLogged()

    if request.method == 'POST':
            # Get registration data from request
            email = request.form.get('email', False)
            password = request.form.get('password', False)
            username = request.form.get('username', False)

            tel = request.form.get('tel', False)

            # Check if user already exists
            db = get_db()
            cursor = db.cursor()  
            cursor.execute('SELECT COUNT(*) FROM client WHERE email = %s', (email,))
            result = cursor.fetchone() 
            if result[0] > 0:
                print("teeeeeeeeeeest")

                cursor.close()
                db.close()

                errors['email'] = 'The email you entered is existed, try another email or'

                return render_template('signup.html',logged_in=logged_in,errors=errors)          
            # Add user to database
            print("teeeeeeeeeeest")
            cursor.execute('INSERT INTO client (username, email, password,tel) VALUES (%s, %s, %s, %s)', (username, email, password,tel))
            db.commit()
            cursor.close()
            db.close()

            flash("Account Created Successfully", 'success')

            return redirect("/signin") 
    else:
        return render_template('signup.html',logged_in=logged_in)


@app.route('/signout')
def signout():
    # remove the user's email from the session
    session.pop('email', None)
    #flash("You have been signed out", 'success')
    # redirect the user to the home page or another page
    return redirect('signin')



@app.route('/ListAllMessages')
def ListAllMessages():
    
    logged_in = UserLogged()
    print(logged_in)
    messages_recipient_count = 0
    messages_sent_count = 0


    id_session = session['id']
    if not id_session:
        return redirect(url_for('signin'))
    else:
       
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
        SELECT message.*, client.username
        FROM message
        JOIN client ON message.id_recipient = client.id
        
        WHERE id_sender = %s
        ''', (id_session,))
        messages_send= []

        for row in cursor.fetchall():
            message_send = {
                'id': row[0],
                'id_sender': row[1],
                'id_recipient': row[2],
                'body': row[3],
                'date': row[4],           
                'username': row[5]

            }
            messages_send.append(message_send)
            messages_sent_count = len(messages_send)


        print("Nombre de messages envoyés :", messages_sent_count)


        cursor.execute('''
        SELECT message.*, client.username
        FROM message
        JOIN client ON message.id_sender = client.id
        
        WHERE id_recipient = %s
        ''', (id_session,))
        messages_receivers= []

        for row in cursor.fetchall():
            message_receivers = {
                'id': row[0],
                'id_sender': row[1],
                'id_recipient': row[2],
                'body': row[3],
                'date': row[4],           
                'username': row[5]

            }
            messages_receivers.append(message_receivers)
            messages_recipient_count = len(messages_receivers)


        cursor.close()
        db.close()
        print("*************************")

        return render_template('messages.html',messages_receivers=messages_receivers,messages_send=messages_send,messages_sent_count=messages_sent_count, logged_in=logged_in,messages_recipient_count=messages_recipient_count)


@app.route('/SendMessage/<int:id_client>/<int:id_product>', methods=['GET','POST'])
def SendMessage(id_client,id_product):

    print("jellooooooooooooooooooooooooooooo")
    logged_in = UserLogged()
    print(logged_in)

    id = session['id']
    if not id:
        return redirect(url_for('signin'))
    else:
       
    
            # Vérifier si la méthode HTTP est POST (utilisateur a soumis le formulaire)
            if request.method == 'POST':
                # Récupérer les données du formulaire
                body = request.form.get('body')
                date = datetime.now()
                print(body)

                
               

    # lire le contenu du fichier et le stocker dans une variable bytes


                # Établir une connexion à la base de données
                db = get_db()
                cursor = db.cursor()

           
            

                # Insérer les données dans la table de produits
                cursor.execute('INSERT INTO message (id_sender,id_recipient,body,date) VALUES (%s, %s,%s, %s)',
                    (id, id_client,body,date))
 
                db.commit()
                cursor.close()
                db.close()

                # Rediriger l'utilisateur vers la page de liste des produits
                return redirect(url_for('ProductDetails',id_product=id_product,logged_in=logged_in))

            # Si la méthode HTTP est GET, afficher le formulaire
            else:
                return redirect(url_for('ProductDetails',id_product=id_product,logged_in=logged_in))







@app.route('/Charter')
def Charter():

    logged_in = UserLogged()
    print(logged_in)

    email = session['id']
    print(email)
   
    return render_template('charter.html',logged_in=logged_in)


@app.route('/MsgServive')
def MsgServive():

    logged_in = UserLogged()
    print(logged_in)

    email = session['id']
    print(email)
   
    return render_template('messageservice.html',logged_in=logged_in)










if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5005,debug=True)