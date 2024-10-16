from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from database import db

app = FastAPI()
security = HTTPBasic()

@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
    
async def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password
    
    async with db.pool.acquire() as connection:
        user = await connection.fetchrow(
            """
            SELECT users.id, users.username, users.password, roles.name AS role_name
            FROM users
            JOIN roles ON users.role_id = roles.id
            WHERE users.username = $1
            """,
            username
        )

        if user and secrets.compare_digest(password, user['password']):
            return {'id': user['id'], 'username': user['username'], 'role': user['role_name']}
        else:
            raise HTTPException(status_code=401, detail="Неверное имя пользователя или пароль")

def role_required(required_role: str):
    async def role_checker(user=Depends(get_current_user)):
        if user['role'] != required_role:
            raise HTTPException(status_code=403, detail="Доступ запрещен")
        return user
    return role_checker



@app.get('/news/')
async def get_news():
    async with db.pool.acquire() as connection:
        rows = await connection.fetch("""
            SELECT news.*, users.username AS author_username
            FROM news
            JOIN users ON news.author_id = users.id
            ORDER BY created_at DESC
        """)
        news_list = [dict(row) for row in rows]
        return news_list


@app.post('/news/', dependencies=[Depends(role_required('editor'))])
async def delete_news(title: str, content: str,user=Depends(get_current_user)):
    async with db.pool.acquire() as connection:
        await connection.execute(
            """
            INSERT INTO news (title, content, author_id) VALUES ($1,$2,$3)
            """,
            title, content, user['id']
            )
        return {'message': 'Новость успешно создана'}


@app.delete('/news/{news_id}', dependencies=[Depends(role_required('admin'))])
async def delete_news(news_id: int):
    async with db.pool.acquire() as connection:
        await connection.execute(
            "DELETE FROM news WHERE id = $1",
            news_id
            )
        return {'message': 'Новость успешно удалена'}
    

@app.get('/users/', dependencies=[Depends(role_required('admin'))])
async def get_users():
    async with db.pool.acquire() as connection:
        rows = await connection.fetch("""
            SELECT users.id, users.username, role.name AS role_name
            FROM users
            JOIN roles ON users.role_id = roles.id
            """)
        users_list = [dict(row) for row in rows]
        return users_list


@app.post('/register/')
async def register(username: str, password: str, role_name: str = 'viewer'):
    async with db.pool.acquire() as connection:
        role = await connection.fetchrow(
            "SELECT id FROM roles WHERE name = $1",
            role_name
        )
        if not role:
            raise HTTPException(status_code=400,detail='Указанная роль не существует')
        
        
        
        existing_user = await connection.fetchrow(
            "SELECT id FROM users WHERE username = $1",
            username
        )
        if existing_user:
            raise HTTPException(status_code=400, detail="Имя пользователя уже занято")
        
        await connection.execute("""
            INSERT INTO users (username, password, role_id) VALUES ($1,$2,$3)
            """,
            username,password,role['id']
        )
        return {'message': 'Пользователь успешного зарегистрирован'}
    
    

@app.post('/login/')
async def login(credentials: HTTPBasicCredentials = Depends(security)):
    user = await get_current_user(credentials)
    return {'message': 'Успешный вход', 'user_id': user['id'],'role':user['role']}

@app.get("/news/{news_id}")
async def get_news_item(news_id: int):
    async with db.pool.acquire() as connection:
        row = await connection.fetchrow("""                
            SELECT news.id, news.title, news.content, news.created_at, news.author_id,
                    users.username AS author_username
            FROM news,
            JOIN users ON news.author_id = users.id
            WHERE news.id = $1                                                                             
        """, news_id)
        if row:
            return dict(row)
        else:
            raise HTTPException(status_code=404, detail= "Новость не найдена")