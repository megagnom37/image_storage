
from uuid import UUID, uuid4
from fastapi import FastAPI
from typing import List, Union
import asyncpg

from .models import Image
from .config import IST_DB_USER, IST_DB_PASSWORD, IST_DB_HOST, IST_DB_PORT


class PostgresDBManager:
    def __init__(self):
        self._conn = None

    async def init_db(self):
        self._conn = await asyncpg.connect(
            f'postgresql://{IST_DB_USER}:{IST_DB_PASSWORD}'
            f'@{IST_DB_HOST}:{IST_DB_PORT}/postgres'
        )

        await self._create_images_table()
        await self._create_tags_table()
        await self._create_images_to_tags_table()

        
    async def _create_images_table(self):
        row = await self._conn.fetchrow(
            "SELECT EXISTS (SELECT FROM information_schema.tables " 
                            "WHERE table_name = 'images');"
        )

        if not row['exists']:
            await self._conn.execute(
                "CREATE TABLE images ("
                "id varchar primary key, "
                "name varchar);"
            )

    async def _create_tags_table(self):
        row = await self._conn.fetchrow(
            "SELECT EXISTS (SELECT FROM information_schema.tables " 
                            "WHERE table_name = 'tags');"
        )

        if not row['exists']:
            await self._conn.execute(
                "CREATE TABLE tags ("
                "id varchar primary key, "
                "tag varchar);"
            )

    async def _create_images_to_tags_table(self):
        row = await self._conn.fetchrow(
            "SELECT EXISTS (SELECT FROM information_schema.tables " 
                            "WHERE table_name = 'images_to_tags');"
        )

        if not row['exists']:
            await self._conn.execute(
                "CREATE TABLE images_to_tags ("
                "image_id varchar, "
                "tag_id varchar);"
            )

    async def get_images_by_tags(self, tags=None) -> List[Image]:
        res = []

        if not tags:
            return await self.get_images()
        tags_str = ', '.join(map(lambda x: f"'{x}'", tags))

        img_rows = await self._conn.fetch(
            f"SELECT t3.id, t3.name, string_agg(t1.tag, ',') FROM ("
            f"(SELECT id, tag FROM tags WHERE tag IN ({tags_str})) as \"t1\" "
            f"INNER JOIN images_to_tags as \"t2\" "
            f"ON t1.id = t2.tag_id "
            f"LEFT JOIN images as \"t3\" ON t2.image_id = t3.id) GROUP BY t3.id;"
        )

        for img_row in img_rows:
            img_info = Image(id=img_row['id'], 
                             name=img_row['name'], 
                             tags=img_row['string_agg'].split(','))
            res.append(img_info)

        return res
            

    async def get_images(self) -> List[Image]:
        res = []

        img_rows = await self._conn.fetch(
            "SELECT id, name FROM images;"
        )

        for img_row in img_rows:
            image_info = Image(id=img_row['id'], name=img_row['name'])

            tags_rows = await self._conn.fetch(
                "SELECT tag FROM ("
                f"(SELECT tag_id FROM images_to_tags WHERE image_id='{image_info.id}') as \"itt\""
                f"LEFT JOIN tags as \"t\" ON itt.tag_id = t.id);"
            )

            image_info.tags = [row['tag'] for row in tags_rows]

            res.append(image_info)

        return res

    async def get_image(self, image_id: str) -> Union[Image, None]:
        img_row = await self._conn.fetchrow(
            f"SELECT id, name FROM images WHERE id='{image_id}';"
        )

        if img_row:
            image_info = Image(id=img_row['id'], name=img_row['name'])
            return image_info

        return None


    async def store_image_info(self, image_info: Image):
        await self._conn.execute(
            f"INSERT INTO images (id, name) VALUES ('{image_info.id}', '{image_info.name}');"
        )

        for tag in image_info.tags:
            tag_id = await self._conn.fetchrow(
                f"SELECT id FROM tags where tag='{tag}';"
            )

            if not tag_id:
                tag_id = uuid4()
                await self._conn.execute(
                    f"INSERT INTO tags (id, tag) VALUES ('{tag_id}', '{tag}');"
                )
            else:
                tag_id = tag_id['id']

            await self._conn.execute(
                "INSERT INTO images_to_tags (image_id, tag_id) "
                f"VALUES ('{image_info.id}', '{tag_id}');"
            )

    async def _drop_all_tables(self):
        await self._conn.execute('DROP TABLE images;')
        await self._conn.execute('DROP TABLE tags;')
        await self._conn.execute('DROP TABLE images_to_tags;')

