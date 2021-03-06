from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import Flask, jsonify, request, make_response
import math
from werkzeug.exceptions import HTTPException
from flask_cors import CORS
import requests
import gunicorn

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flaskmysql:flaskmysql@slashwebmariadb.cyuazzw9rdsu.us-east-1.rds.amazonaws.com/flaskmysql'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pass@localhost/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_TIMEOUT'] = None
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
    career_code=db.Column(db.String(3))
    def __init__(self,degree,study_plan_id,semester_num,career,number_of_assignatures,
    classroom,building,type_of_pi,even_or_odd,career_code):
        self.degree = degree
        self.study_plan_id=study_plan_id
        self.semester_num=semester_num
        self.career=career
        self.number_of_assignatures=number_of_assignatures
        self.classroom=classroom
        self.building=building
        
        self.type_of_pi=type_of_pi
        self.even_or_odd = even_or_odd
        self.career_code=career_code

class semester_student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    semester_num = db.Column(db.Integer)
    student_id= db.Column(db.Integer)
    def __init__(self,semester_id, student_id):
        self.semester_id=semester_id
        self.student_id=student_id


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
    career_code=db.Column(db.String(3))
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
        'career_name','id_study_plan','coord','number_of_semesters','career_mod','rvoe_sep','dgp','career_code')
career_schema = career_schema_model()
careers_schema = career_schema_model(many=True)

class semester_schema_model(ma.Schema):
    class Meta:
        fields = ('id','degree','study_plan_id','semester_num',
        'career','number_of_assignatures','classroom','building','type_of_pi','even_or_odd','career_code')
semester_schema = semester_schema_model()
semesters_schema = semester_schema_model(many=True)

class semester_student_schema_model(ma.Schema):
    class Meta:
        fields = ('id','semester_num','student_id')
semester_student_schema = semester_student_schema_model()
semesters_students_schema = semester_student_schema_model(many=True)
####################
#####################
#Secci??n de semester, autor: Ariel Arreola
#####################
####################
@app.route('/', methods=['GET'])
def main_api():
    return jsonify({"message":"You are in flask-mysql-api"})
#app joke y mariana... 
@app.route('/subjectcareer/name/<subject_name>', methods=['get'])
def subject_career_name(subject_name):
    mongo_res=requests.get('https://api-nodejs-mongod.herokuapp.com/subjects/name/%s'%((subject_name))).json()
    print(subject_name)
    if(len(mongo_res)!=0):
        career_list=list()
        car=list()
        for i in range(len(mongo_res)):
            career_list.append(str(mongo_res[i]['assigned_career']))
            car.append(career.query.filter_by(career_code=career_list[i]))
        resarray=list()
        if(car):
            for j in range(len(career_list)):
                aux=career_schema.dump(car[j][0])
                resarray.append(aux)
            return jsonify({"search_subject":subject_name,"data_subject":mongo_res,"its career(s)": resarray})
        else:
            return jsonify({"message":"That career doesn't exist"})
    else:
        return jsonify({"message":"This subject code doesn't exist"})


@app.route('/semesterteacher/subject/<subject_name>', methods=['get'])
def semester_teacher_name(subject_name):

    node_res0=requests.get('https://crud-nodejs-1.herokuapp.com/subject/%s/teachers/'%((subject_name))).json()
    node_res=node_res0['subjects']
    if(len(node_res)!=0):
        career_list=list()
        career_res=list()
        sem_list=list()
        sem_res=list()
        teachers=list()
        
        for i in range(len(node_res)):
            career_list.append(str(node_res[i]['assigned_career']))
            career_res.append(career.query.filter_by(career_code=career_list[i]))
            sem_list.append(int(node_res[i]['semester_num']))
            sem_res.append(semester.query.filter_by(semester_num=sem_list[i]))
            teachers.append(str(node_res[i]['teacher_id']))
        resarray=list()
        semres=list()
        if(career_res):
            for j in range(len(career_list)):
                aux=career_schema.dump(career_res[j][0])
                resarray.append(aux)
                aux2=career_schema.dump(career_res[j][0])
                semres.append(aux2)
            #jsongen
            jsongen=list()
            for e in range(len(teachers)):
                jsongen.append({"teacher_code":teachers[e],"assigned semesters":semres[e],"career in charge": resarray[e]})
            return jsonify({"search_subject":subject_name,"info":jsongen})
        else:
            return jsonify({"message":"That career doesn't exist"})
    else:
        return jsonify({"message":"This subject name doesn't exist"})


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
        career_code=request.json['career_code']
        new_semester= semester(degree,study_plan_id,semester_num,career,number_of_assignatures,classroom,building,type_of_pi,even_or_odd,career_code)

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
    limit_pag=request.args.get('limit', 3, type = int)
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

@app.route('/semester/<semester_num>', methods=['GET'])
def get_sem(semester_num):
        #car = career.query.filter(career.career_code.like('%'+career_code+'%'))
    sem= semester.query.filter_by(semester_num=semester_num).all()
    print("sem num:",semester_num)
    if(sem):
        return semesters_schema.jsonify(sem)
    return jsonify({"message":"There was an error in ID, please check"}) 

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
            career_code = request.json['career_code']
            sem.degree = degree
            sem.study_plan_id = study_plan_id
            sem.semester_num = semester_num
            sem.career = career
            sem.number_of_assignatures = number_of_assignatures
            sem.classroom  = classroom 
            sem.building  = building 
            sem.type_of_pi = type_of_pi
            sem.even_or_odd = even_or_odd
            sem.career_code=career_code

            db.session.commit()
            res= semester_schema.dump(sem)
            res_notif={"message": "This data has been updated successfully","data":res}
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
#Secci??n de career, autor: Mario Ochoa
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
        career_code = request.json['career_code']

        new_career= career(type_of_career,knowledge_area,career_name,id_study_plan,coord,number_of_semesters,career_mod,rvoe_sep,dgp,career_code)

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
    limit_pag=request.args.get('limit', 3, type = int)
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

@app.route('/career/<career_code>', methods=['GET'])
def get_career(career_code):
    #car = career.query.filter(career.career_code.like('%'+career_code+'%'))
    car = career.query.filter_by(career_code=career_code).all()
    print("CAREER CODE:",career_code)
    if(car):
        return career_schema.jsonify(car[0])
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
            career_code=request.json['career_code']
            car.type_of_career = type_of_career
            car.knowledge_area = knowledge_area
            car.career_name = career_name
            car.id_study_plan = id_study_plan
            car.coord = coord
            car.number_of_semesters  = number_of_semesters 
            car.career_mod  = career_mod 
            car.rvoe_sep = rvoe_sep
            car.dgp = dgp
            car.career_code=career_code

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
    app.run(threaded=True,host="0.0.0.0")