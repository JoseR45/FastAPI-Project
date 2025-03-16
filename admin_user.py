from user.models.user_model import User  
from post.models.post_relations_model import Post
from settings.database import get_db
import asyncio
from sqlalchemy.future import select

async def create_admin():
    async for session in get_db():
        admin_email = "admin@example.com"
        admin_password = "admin123"

        existing_admin = await session.execute(select(User).where(User.email == admin_email))
        existing_admin = existing_admin.scalar_one_or_none()
        if existing_admin:
            print("Admin already exists")
            return
        
        admin_user = User(
            email=admin_email,
            is_staff=True
        )
        await admin_user.set_password(admin_password)
        
        session.add(admin_user)
        await session.commit()
        print("Admin created")
        break

if __name__ == "__main__":
    asyncio.run(create_admin())
