from fastapi import APIRouter,Request,HTTPException
from fastapi.responses import Response,JSONResponse
from models import usermodel
from services import firebaseService as fb
import json

router = APIRouter()

@router.post("/register")
def read_root(user_register:usermodel.register):

    try:
        user=fb.auth.create_user_with_email_and_password(user_register.email,user_register.password)
    except:
        return JSONResponse(content={"error":"Ocurrio un error al registrar el usuario."},status_code=406)
    try:
        data={"username":user_register.username,
                "email":user_register.email,
                "password":user_register.password,
                "isAdmin":False}
        fb.db.child("users").child(user["localId"]).set(data)
    except:
        return JSONResponse(content={"error":"Ocurrio un error al acceder a la base de datos."},status_code=406)
    return Response(status_code=201)


@router.post("/login")
def read_root(user_login:usermodel.login):
    try:
        user=fb.auth.sign_in_with_email_and_password(user_login.email,user_login.password)
    except:
        return JSONResponse(content={"error":"Usuario o contraseña incorrectos"},status_code=406)
    
    resp=Response(status_code=204)
    usrdata=json.loads(find_user_by_id(user["localId"]).body)

    resp.headers.append("set-cookie",f"usrnm={usrdata["data"]["username"]};"+
                                           "Max-Age=3600;"+
                                           "Path=/;"+
                                           "SameSite=None;"+
                                           "Secure;"+
                                           "Partitioned;"+
                                           "domain=.vercel.app;")                                          
    resp.headers.append("set-cookie",f"localId={user["localId"]};"+
                                           "Max-Age=3600;"+
                                           "Path=/;"+
                                           "SameSite=None;"+
                                           "Secure;"+
                                           "Partitioned;"+
                                           "domain=.vercel.app;")                                          


    resp.headers.append("set-cookie",f"idToken={user["idToken"]};"+
                                           f"Max-Age=3600;"+
                                           f"Path=/;"+
                                           f"SameSite=None;"+
                                           f"Secure;"+
                                           f"Partitioned;"+
                                           "domain=.vercel.app;")                                          

    
    # resp.set_cookie(key="usrnm",value=usrdata["data"]["username"], max_age=3600,secure=True,samesite="None")
    # resp.set_cookie(key="localId",value=user["localId"], max_age=3600,secure=True,samesite="None")
    # resp.set_cookie(key="idToken",value=user["idToken"], max_age=3600,secure=True,samesite="None")
    if user_login.remember:
        resp.headers.append("set-cookie",f"refreshToken={user["refreshToken"]};"+
                                        f"Path=/;"+
                                        f"SameSite=None;"+
                                        f"Secure;"+
                                        f"Partitioned;"+
                                        "domain=.vercel.app;")                                        

        # resp.set_cookie(key="refreshToken",value=user["refreshToken"],secure=True,samesite="None")
    return resp


@router.get("/info/{id}")
def find_user_by_id(id:str):
    try:
        # Obtener datos del usuario
        u = fb.db.child("users").child(id).get()
        print(u)
        user_data = u.val()
        if not user_data:
            return JSONResponse({"error": "User not found"}, status_code=404)
        return JSONResponse({"data": user_data}, status_code=200)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=300)


@router.get("/token")
def protected_route(request: Request):
    id_token = request.cookies.get("idToken")
    if not id_token:
        raise HTTPException(status_code=401, detail="No se encontró el token")
    try:
        user_info = fb.auth.get_account_info(id_token)
        return Response(status_code=200)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    
@router.get("/token/refresh")
def refresh_token(request:Request):
    try:
        user=fb.auth.refresh(request.cookies.get("refreshToken"))
    except:
        raise HTTPException(status_code=401, detail="Ha ocurrido un error")
    res=Response(status_code=200)
    usrdata=json.loads(find_user_by_id(user["userId"]).body)
    #res.set_cookie(key="usrnm",value=usrdata["data"]["username"], max_age=3600,secure=True,samesite="None")

    #res.set_cookie(key="localId",value=user["userId"], max_age=3600,secure=True,samesite="None")
    #res.set_cookie(key="idToken",value=user["idToken"], max_age=3600,secure=True,samesite="None")
    #res.set_cookie(key="refreshToken",value=user["refreshToken"],secure=True,samesite="None")

    return res
