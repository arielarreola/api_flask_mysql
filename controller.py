from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import Flask, jsonify, request
import math
from werkzeug.exceptions import HTTPException
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pass@localhost/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class semester(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    degree = db.Column(db.String(70))
    study_plan_id = db.Column(db.Integer)
    semester_num = db.Column(db.Integer)
    career = db.Column(db.String(70))
    number_of_assignatures=db.Column(db.Integer)
    classroom=db.Column(db.Integer)
    building=db.Column(db.String(70))
    type_of_pi=db.Column(db.String(70))
    even_or_odd=db.Column(db.String(70))
    def __init__(self,degree,study_plan_id,semester_num,career,number_of_assignatures,
    classroom,building,type_of_pi,even_or_odd):
        self.degree = degree
        self.study_plan_id=study_plan_id
        self.semester_num=semester_num
        self.career=career
        self.number_of_assignatures=number_of_assignatures
        self.classroom=classroom
        self.building=building
        
        self.type_of_pi=type_of_pi
        self.even_or_odd = even_or_odd

class career(db.Model):
    id_career = db.Column(db.Integer, primary_key=True)
    type_of_career = db.Column(db.String(70))
    knowledge_area = db.Column(db.String(70))
    career_name = db.Column(db.String(70))
    id_study_plan = db.Column(db.Integer)
    coord=db.Column(db.String(70))
    number_of_semesters=db.Column(db.Integer)
    career_mod=db.Column(db.String(70))
    rvoe_sep=db.Column(db.Integer)
    dgp=db.Column(db.Integer)
    def __init__(self,type_of_career,knowledge_area,career_name,id_study_plan,coord,
    number_of_semesters,career_mod,rvoe_sep,dgp):
        self.type_of_career = type_of_career
        self.knowledge_area=knowledge_area
        self.career_name=career_name
        self.id_study_plan=id_study_plan
        self.coord=coord
        self.number_of_semesters=number_of_semesters
        self.career_mod=career_mod
        self.rvoe_sep=rvoe_sep
        self.dgp = dgp

db.create_all()


class career_schema_model(ma.Schema):
    class Meta:
        fields = ('id_career','type_of_career','knowledge_area',
        'career_name','id_study_plan','coord','number_of_semesters','career_mod','rvoe_sep','dgp')
career_schema = career_schema_model()
careers_schema = career_schema_model(many=True)

class semester_schema_model(ma.Schema):
    class Meta:
        fields = ('id','degree','study_plan_id','semester_num',
        'career','number_of_assignatures','classroom','building','type_of_pi','even_or_odd')
semester_schema = semester_schema_model()
semesters_schema = semester_schema_model(many=True)

####################
#####################
#Sección de semester, autor: Ariel Arreola
#####################
####################
@app.route('/', methods=['GET'])
def main_api():
    return jsonify({"message":"You are in flask-mysql-api"})

@app.route('/semester', methods=['Post'])
def create_sem():
    try:
        degree = request.json['degree']
        study_plan_id = request.json['study_plan_id']
        semester_num = request.json['semester_num']
        career = request.json['career']
        number_of_assignatures = request.json['number_of_assignatures']
        classroom = request.json['classroom']
        building = request.json['building']
        type_of_pi= request.json['type_of_pi']
        even_or_odd = request.json['even_or_odd']


        new_semester= semester(degree,study_plan_id,semester_num,career,number_of_assignatures,classroom,building,type_of_pi,even_or_odd)

        db.session.add(new_semester)
        db.session.commit()  
        res=semester_schema.dump(new_semester)
        res_notif={"message": "This data has been added successfully","data":res}
        return jsonify(res_notif)
    except KeyError:
        return jsonify({"message":"There is a key error, please check variables"})
    


@app.route('/semester', methods=['GET'])
def get_sems():
    page_pag=request.args.get('page', 1, type = int)
    limit_pag=request.args.get('limit', 1, type = int)
    category_param_value = request.args.get('like','')
    rows=db.session.query(semester.id).count()
    total_pages=math.ceil(rows/limit_pag)
    searchlike = semester.query.filter(semester.career.like(category_param_value + "%")).paginate(page_pag,limit_pag, False)
    #all_sem= semester.query.paginate(page_pag,limit_pag, False)#.filter(semester.message.match("%{}%".format(tag))).all()
    offset=limit_pag*(page_pag-1)
    #result = semesters_schema.dump(all_sem.items)
    search = semesters_schema.dump(searchlike.items)
    return jsonify({"limit":limit_pag,"current_page":page_pag,"data":search,"total_elements":rows,"total_pags":total_pages,
    "offset":offset})

@app.route('/semester/<id>', methods=['GET'])
def get_sem(id):
    sem1 = semester.query.get(id)
    if(sem1):
        return semester_schema.jsonify(sem1)
    else:
        response= {
        "message":"There was an error in ID, please check"
    }   
        return jsonify(response) 
@app.errorhandler(400)
def handle_exception(e):
    response= {
        "message":"It seems that was a bad request, please check"
    }        
@app.errorhandler(404)
def handle_exception(e):
    response= {
        "message":"The resource wasn't found, please check"
    }
    
    return jsonify(response) 
@app.errorhandler(405)
def handle_exception(e):
    response= {
        "message":"There was an error in HTTP Method, please check"
    }  
    return jsonify(response) 
@app.errorhandler(500)
def handle_exception2(e):
    """Return JSON instead of HTML for HTTP errors."""
    response= {
        "message":"There was an error in server, We will repair it soon"
    }
    
    return jsonify(response) 

@app.route('/semester/<id>', methods=['PUT'])
def update_sem(id):
    try:
        sem = semester.query.get(id)
        if sem:
            degree = request.json['degree']
            study_plan_id = request.json['study_plan_id']
            semester_num = request.json['semester_num']
            career = request.json['career']
            number_of_assignatures = request.json['number_of_assignatures']
            classroom = request.json['classroom']
            building = request.json['building']
            type_of_pi = request.json['type_of_pi']
            even_or_odd = request.json['even_or_odd']

            sem.degree = degree
            sem.study_plan_id = study_plan_id
            sem.semester_num = semester_num
            sem.career = career
            sem.number_of_assignatures = number_of_assignatures
            sem.classroom  = classroom 
            sem.building  = building 
            sem.type_of_pi = type_of_pi
            sem.even_or_odd = even_or_odd

            db.session.commit()
            res= semester_schema.dump(sem)
            res_notif={"message": "This data has been added successfully","data":res}
            return jsonify(res_notif)
        else:
            response= {
            "message":"There was an error in ID, please check"
        }
            return jsonify(response) 
    except KeyError:
        return jsonify({"message":"There is a key error, please check variables"})

@app.route('/semester/<id>', methods=['DELETE'])
def delete_sem(id):
    sem = semester.query.get(id)
    if(sem):
        db.session.delete(sem)
        db.session.commit()
        res=semester_schema.dump(sem)
        res_notif={"message": "This data has been deleted successfully","data":res}
        return jsonify(res_notif)
    else:
        response= {
        "message":"There was an error in ID, please check"
    }
    
        return jsonify(response) 

####################
#####################
#Sección de career, autor: Mario Ochoa
#####################
####################



@app.route('/career', methods=['POST'])
def create_career():
    try:
        type_of_career = request.json['type_of_career']
        knowledge_area = request.json['knowledge_area']
        career_name = request.json['career_name']
        id_study_plan = request.json['id_study_plan']
        coord = request.json['coord']
        number_of_semesters = request.json['number_of_semesters']
        career_mod = request.json['career_mod']
        rvoe_sep= request.json['rvoe_sep']
        dgp = request.json['dgp']

        new_career= career(type_of_career,knowledge_area,career_name,id_study_plan,coord,number_of_semesters,career_mod,rvoe_sep,dgp)

        db.session.add(new_career)
        db.session.commit()
        res=career_schema.dump(new_career)
        res_notif={"message": "This data has been added successfully","data":res}
    
        return jsonify(res_notif)
    except KeyError:
        return jsonify({"message":"There is a key error, please check variables"})

@app.route('/career', methods=['GET'])
def get_careers():
 
    page_pag=request.args.get('page', 1, type = int)
    limit_pag=request.args.get('limit', 1, type = int)
    category_param_value = request.args.get('like','')
    rows=db.session.query(career.id_career).count()
    total_pages=math.ceil(rows/limit_pag)
    searchlike = career.query.filter(career.career_name.like("%"+ category_param_value + "%")).paginate(page_pag,limit_pag, False)

    #all_car= career.query.paginate(page_pag,limit_pag, False)
    offset=limit_pag*(page_pag-1)
    #result = careers_schema.dump(all_car.items)
    search = careers_schema.dump(searchlike.items)
    return jsonify({"limit":limit_pag,"current_page":page_pag,"data":search,"total_elements":rows,"total_pags":total_pages,
    "offset":offset})

@app.route('/career/<id>', methods=['GET'])
def get_career(id):
    car = career.query.get(id)
    if(car):
        return career_schema.jsonify(car)
    return jsonify({"message":"There was an error in ID, please check"}) 



@app.route('/career/<id>', methods=['PUT'])
def update_career(id):
    try:
        car = career.query.get(id)
        if car:
            type_of_career = request.json['type_of_career']
            knowledge_area = request.json['knowledge_area']
            career_name = request.json['career_name']
            id_study_plan = request.json['id_study_plan']
            coord = request.json['coord']
            number_of_semesters = request.json['number_of_semesters']
            career_mod = request.json['career_mod']
            rvoe_sep= request.json['rvoe_sep']
            dgp = request.json['dgp']

            car.type_of_career = type_of_career
            car.knowledge_area = knowledge_area
            car.career_name = career_name
            car.id_study_plan = id_study_plan
            car.coord = coord
            car.number_of_semesters  = number_of_semesters 
            car.career_mod  = career_mod 
            car.rvoe_sep = rvoe_sep
            car.dgp = dgp

            db.session.commit()
            res=career_schema.dump(car)
            res_notif={"message": "This data has been updated successfully","data":res}
            return jsonify(res_notif)
        else:
            return jsonify({"message":"There was an error in ID, please check"}) 
    except KeyError:
        return jsonify({"message":"There is a key error, please check variables"})

@app.route('/career/<id>', methods=['DELETE'])
def delete_career(id):
    car = career.query.get(id)
    if car:
        db.session.delete(car)
        db.session.commit()
        res=career_schema.dump(car)

        res_notif={"message": "This data has been deleted successfully","data":res}
  
        return jsonify(res_notif)
    else:
        return jsonify({"message":"There was an error in ID, please check"}) 


if __name__=="__main__":
    app.run(debug=True)