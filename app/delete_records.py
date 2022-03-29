from databases import Database
import asyncio

database = Database('sqlite:///app.db')
async def delete_records():
    await database.connect()
    await database.execute(query='DELETE FROM movies')
    await database.execute(query='DELETE FROM ratings')
asyncio.run(delete_records())