from schemas.user_schema import User

users_db = [User(id=1,name="Laura",surname="De Feo",age=23,url="google.com"),
         User(id=2,name="Guido",surname="Movia",age=24,url="google.com")]

users_db_auth_basic = {
    "mouredev": {
        "username": "mouredev",
        "full_name": "Brais Moure",
        "email": "braismoure@gmail.com",
        "disabled": True,
        "password": "123456" #---> porque aca si necesito que se autentique
    },
    "ldefeo": {
        "username": "ldefeo",
        "full_name": "Laura De Feo",
        "email": "ldefeo@fi.uba.ar",
        "disabled": False,
        "password": "41800179"
    }
}

users_db_auth = {
    "mouredev": {
        "username": "mouredev",
        "full_name": "Brais Moure",
        "email": "braismoure@gmail.com",
        "disabled": True,
        "password": "$2a$12$GWF1Sj0NTDtTbi8VfZwWjuiRFkH.nThJxzzS8N8.bffJC0l55MCzO" #---> porque aca si necesito que se autentique
    },
    "ldefeo": {
        "username": "ldefeo",
        "full_name": "Laura De Feo",
        "email": "ldefeo@fi.uba.ar",
        "disabled": False,
        "password": "$2a$12$S2jSMOyTSyKgHOeZ4mSA9ux6slmhVIrN/QUHnwLPWN4mGuGFB64ge"
    }
}