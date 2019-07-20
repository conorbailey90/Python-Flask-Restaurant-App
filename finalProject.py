from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Return JSON

@app.route('/restaurants/JSON')
def restaurantsJSON():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    restaurantlist = session.query(Restaurant).all()
    return jsonify(restaurants=[i.serialize for i in restaurantlist])

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    menuItems = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return jsonify(Menu=[i.serialize for i in menuItems])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def MenuItemJSON(restaurant_id, menu_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem= menuItem.serialize)

@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    # This will show all restaurants
    session = DBSession()
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurants/new', methods=['GET', 'POST'])
def newRestaurant():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.method == 'POST':
        new_restaurant = Restaurant(name=request.form['name'])
        session.add(new_restaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')

@app.route('/restaurants/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    edited_restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        edited_restaurant.name = request.form['name']
        session.add(edited_restaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('editRestaurant.html', restaurant_id = restaurant_id, i = edited_restaurant)

@app.route('/restaurants/<int:restaurant_id>/delete/', methods = ['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    deletedRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        session.delete(deletedRestaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleteRestaurant.html', restaurant_id = restaurant_id, i = deletedRestaurant)

@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
    return render_template('menu.html', restaurant=restaurant, items=items)

@app.route('/restaurants/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.method == 'POST':
        new_menu_item = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
        new_menu_item.description = request.form['description']
        new_menu_item.price = request.form['price']
        new_menu_item.course = request.form['course']
        session.add(new_menu_item)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id = restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    edit_item = session.query(MenuItem).filter_by(id =menu_id).one()
    if request.method == 'POST':
        edit_item.name = request.form['name']
        edit_item.description = request.form['description']
        edit_item.price = request.form['price']
        edit_item.course = request.form['course']
        session.add(edit_item)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return (render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, i = edit_item))

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    deletedItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('deletemenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, i = deletedItem)

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)