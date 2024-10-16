import asyncpg 
import asyncio

async def create_tables():
    conn = await asyncpg.connect(
        user = "postgres",
        password = "666666",
        database = "postgres",
        host="localhost",
        port = 5432
    )

    
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS roles (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL
        );
    """)
    
    await conn.execute("""
        INSERT INTO roles (name) VALUES ('admin') ON CONFLICT DO NOTHING;
        INSERT INTO roles (name) VALUES ('editor') ON CONFLICT DO NOTHING;
        INSERT INTO roles (name) VALUES ('viewer') ON CONFLICT DO NOTHING;
        """)
    
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            role_id INTEGER REFERENCES roles(id)
        );
    """)
    
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS news(
            id SERIAL PRIMARY KEY,
            title VARCHAR(50) UNIQUE NOT NULL,
            content TEXT NOT NULL,
            author_id INTEGER REFERENCES users(id),
            created_at TIMESTAMP DEFAULT NOW()
        );
    """)
    await conn.close()

if __name__ == '__main__':
    asyncio.run(create_tables())
