#import repl_module
#import tflearn_module
import pickle, os, subprocess
from flask import Flask, render_template, request, redirect, Response

classroom_file_list = ["classroom"]

app = Flask(__name__)

@app.route("/minecraftremake")
def minecraftremake():
  return render_template("/minecraftremake.html")

@app.route("/classroomCreation")
def classroom_creation():
  return render_template("/classroomCreation.html")

@app.route("/solarsystem")
def solarsystem():
  return render_template("/solarsystem.html")

@app.route("/classroomCreation_results", methods = ["POST"])
def classroom_creation_results():
  result = request.form
  s = dict(result)
  classroom_code = ''.join(s['classroomCode'])
  classroom_file_list.append(classroom_code)
  os.system("mkdir Server/"+classroom_code+"/")
  s = open("Server/"+classroom_code+"/classroom.pkl", "w")
  pickle.dump({}, s)
  s.close()
  return render_template("error.html")

@app.route("/")
def start():
  return render_template("start.html")

@app.route("/signup")
def signup():
	return render_template("signup.html")

@app.route('/signup_results', methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      s = dict(result)
      classroom = ''.join(s['classroom'])
      username = ''.join(s['username'])
      password = ''.join(s['password'])
      password_conf = ''.join(s['passwordConfirm'])
      if password_conf == password:
        for i in range(len(classroom_file_list)):
          if classroom_file_list[i] == classroom:
            class_room = open('Server/classroom/'+classroom_file_list[i]+'.pkl', 'rb')
            s = pickle.load(class_room)
            class_room.close()
            class_room = open('Server/classroom/'+classroom_file_list[i]+'.pkl', 'wb')
            s[username] = password
            print(s)
            pickle.dump(s, class_room)
            class_room.close()
            print(s)
            print("[+]New user: "+username)
            print('"'+username+'"')
            return render_template("home.html", username = username, classroom = classroom)
        pass
      else:
        return render_template("error.html")

@app.route("/error")
def error():
  return render_template("/error")

@app.route("/login")
def login():
  return render_template("/login.html")

@app.route("/login_results", methods = ["POST"])
def login_result():
  result = request.form
  s = dict(result)
  username = ''.join(s["username"])
  password = ''.join(s["password"])
  classroom = ''.join(s["classroom"])
  for i in range(len(classroom_file_list)):
    if classroom_file_list[i] == classroom:
      class_room = open('Server/'+classroom_file_list[i]+'/classroom.pkl', 'rb')
      s = pickle.load(class_room)
      class_room.close()
      if s[username] == password:
        return render_template("home.html", usname = username, classroom = classroom)
      else:
        return render_template("/error.html")

@app.route("/repl", methods = ["POST"])
def repl():
  result = request.form
  s = dict(result)
  username = ''.join(s['username'])
  classroom = ''.join(s['classroom'])
  print(username)
  try:
    script = ''.join(s['Script'])
    print(script)
    print("[+] User " + username + " just sent script")
    repl = open("Server/"+classroom+"/scripts/" + username + ".py", "w+")
    repl.write(script)
    repl.close()
    result = subprocess.Popen("python Server/"+classroom+"/scripts/"+username+".py", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    d = result.stdout.read()
    f = result.stderr.read()
    result1 = d.decode()+f.decode()
    print (result1)
    print (type(d.decode()))
    if d.decode() == 3:
      return render_template("error.html")
    else:
      return render_template('repl.html', username = username, classroom = classroom, result = result1)
  except:
    return render_template('repl.html', username = username, classroom = classroom)


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080)
