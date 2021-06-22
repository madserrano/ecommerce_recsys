# import libraries
from surprise import KNNBaseline, Dataset, Reader
import pandas as pd
from flask import Flask, render_template, redirect, url_for, request
app = Flask(__name__)
app.static_folder = 'static'

@app.route("/")
def main():
    return render_template('/index.html')

### Recommender py start #######################################################################
@app.route("/cars.html?user_id=<user_id>&year=<year>&model=<model>", methods=["POST", "GET"])
def get_recom(user_id, year, model):
    result = []
    car_search = model
    similar_cars = 10
    # k is the number of similar cars Surprise will output
    k = 1500
    
    # Similarity cosine type
    similarity = ['pearson_baseline', 'cosine']
    similarity_type = similarity[1]
    
    # reading the files
    path = 'files/rid_name_car_{}.csv'.format(year)
    try:
        rid_name = pd.read_csv(path, dtype = str)
    except :
        html = "Data For this year doesn't exist.<br>Try years between 1997 and 2019"
        return render_template('r_cars.html', value=html)
    rid = (rid_name['rid'].values.tolist())
    name = (rid_name['name'].values.tolist())
    rid_to_name = dict(zip(rid, name))
    name_to_rid = dict(zip(name, rid))
    ratingsPath = 'files/ratings_{}.csv'.format(year)
    reader = Reader(line_format='user item rating', sep=',', skip_lines=1)
    data = Dataset.load_from_file(ratingsPath, reader=reader)
    
    # Running the data into the algorithm
    trainset = data.build_full_trainset()
    sim_options = {'name': similarity_type,
                    'user_based': False
                  }
    algo = KNNBaseline(sim_options=sim_options)
    algo.fit(trainset)
    
    # Read the mappings raw id <-> car name
    rid_to_name = rid_to_name
    name_to_rid = name_to_rid
    
    # Retrieve inner id of the car "car_search"
    try:
        car_raw_id = name_to_rid[car_search]
    except:
        html = "Data For this carr doesn't exist.<br>Try another car"
        return render_template('r_cars.html', value=html)
    car_inner_id = algo.trainset.to_inner_iid(car_raw_id)
    
    # Retrieve inner ids of the nearest neighbors of "car_search".
    car_neighbors = algo.get_neighbors(car_inner_id, k=k)
    
    # Convert inner ids of the neighbors into names.
    car_neighbors = (algo.trainset.to_raw_iid(inner_id) for inner_id in car_neighbors)
    car_neighbors = (rid_to_name[rid] for rid in car_neighbors)
    
    # Retrieving results and storing them into a list
    car_list = []
    for car in car_neighbors:
        car_list.append(car)
    
    # Removing unique brand names to recommend cars from different brands
    list_test = []
    for car in car_list:
        car_brand = car.split(' ')
        list_test.append(car_brand[0])
    
    # Selecting the only one car per brand
    unique_cars = []
    unique_brands = pd.unique(list_test).tolist()
    for brand in unique_brands:
        for car in car_list:
            if brand in car:
                unique_cars.append(car)
                break
    
    # Retrieving the cars the user has already reviewed
    path_read = 'files/ratings_full.csv'
    df_full = pd.read_csv(path_read)
    df_user_id = df_full[(df_full['car_year']==year) & (df_full['userId']==user_id)]
    cars_reviewed = df_user_id['car'].unique().tolist()
    
    # If the user has already reviewed the car, do not show it
    # cars_reviewed = user_car_dict[user_id]
    list_to_show = []
    for car in unique_cars:
        if car not in cars_reviewed:
            list_to_show.append(car)
       
    # printing the car names
    for car in list_to_show[:similar_cars]:
        result.append([car])
        #print(car)
        #return car
#    return render_template('/<user_id>?year=<year>', user_id=user_id, year=year)

    # This part for generate HTML for return
    html = '<ul>'
    for i in result:
        html += '<li>'+i[0] +'</li>'
    html +='</ul>'    
    ## returning html page based on chosen model
    if model == "Toyota Highlander SUV":
        return render_template('car-details.html', value=html)
    elif model == "Volkswagen Passat Sedan":
        return render_template('car-details2.html', value=html)
    elif model == "Dodge Ram Pickup":
        return render_template('car-details3.html', value=html)
    elif model == "Acura TL Sedan":
        return render_template('car-details4.html', value=html)
    else:
        return render_template('r_cars.html',value=html)           
### Recommender end #############################################################################

### Initialize cars.html to request input   
@app.route("/cars.html", methods=["POST", "GET"])
def cars():
    if request.method == "POST":
        user_id = request.form["user_id"]
        year = request.form["year"]
        model = request.form["model"]
        return redirect(url_for("get_recom", user_id=user_id, year=year, model=model))
    else:
        return render_template("cars.html")

@app.route("/index.html")
def home():
    return render_template('index.html')

@app.route('/car-details.html')
def car1():
    return render_template('car-details.html')

@app.route('/car-details2.html')
def car2():
    return render_template('car-details2.html')

@app.route('/car-details3.html')
def car3():
    return render_template('car-details3.html')

@app.route('/car-details4.html')
def car4():
    return render_template('car-details4.html')

@app.route('/r_cars.html')
def car_result():
    return render_template('r_cars.html')

if __name__ == "__main__":
    app.run()