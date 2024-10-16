import asyncpg

class Database:
    def __init__(self) -> None:
        self.pool = None
    
    async def connect(self):
        self.pool = await asyncpg.create_pool(
            user = "postgres",
            password = "666666",
            database = "postgres",
            host="localhost",
            port = 5432
        )

    async def disconnect(self):
        await self.pool.close()

db = Database()