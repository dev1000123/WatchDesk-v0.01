import firebase_admin
from firebase_admin import credentials, firestore
from flask import request
cred = credentials.Certificate("MISC/fb.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
profile_struct = {
    "name": "",
    "password": "",
    # "bio":""
}
post_struct = {
    "heading":"",
    "content":"",
    "author":""
}

# -----DEFAULTS-----#


def signup(uname: str, Name: str, password: str):
    profile = profile_struct
    profile["name"] = Name
    profile["password"] = password

    profile_db = db.collection("user").document(uname)
    profile_db.set(profile)


def login(uname: str, password: str):
    target_db = db.collection("user").document(uname)
    target = target_db.get()
    target = target.to_dict()
    if target["password"] == password:
        return True
    else:
        return False


def get_user_data(Uname: str):
    udb = db.collection("user").document(Uname)
    print(udb.get().to_dict())

    return udb.get().to_dict()


def CheckIfUserExists(Name: str):
    check_db = db.collection("user").document(Name).get()
    if check_db.exists:
        return True
    else:
        return False


def get_all_data(collection: str):
    list1 = []
    posts_db = db.collection(collection).stream()
    for doc in posts_db:
        list1.append(doc.to_dict())
    return list1
def make_post(form_data:dict):
    post = post_struct
    post_struct["heading"] = form_data["heading"]
    post_struct["content"] = form_data["content"]
    post_struct["author"] = get_user_data(request.cookies.get("uname"))["name"]
    post_send = db.collection("posts").document(post_struct["heading"]).set(post_struct)
