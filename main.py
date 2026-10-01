from fastapi import FastAPI
<<<<<<< HEAD
from mysite.admin.setup import setup_admin
from mysite.api import user, auth, agent, file
import uvicorn


ai_app = FastAPI(title="AI DataCheck")

ai_app.include_router(auth.auth_router)
ai_app.include_router(user.user_router)
ai_app.include_router(agent.agent_router)
ai_app.include_router(file.file_router)
setup_admin(ai_app)

if __name__ == "__main__":
    uvicorn.run(ai_app, host='127.0.0.1', port=8000)
=======
import uvicorn
from mysite.api import order, auth, product, ai
from mysite.admin.setup import setup_admin


delivery_app = FastAPI(title='Delivery with LLM')
delivery_app.include_router(auth.auth_router)
delivery_app.include_router(product.product_router)
delivery_app.include_router(order.order_router)
delivery_app.include_router(ai.ai_router)
setup_admin(delivery_app)


if __name__ == "__main__":
    uvicorn.run(delivery_app, host='127.0.0.1', port=8000)
>>>>>>> 79752a4 (chain)
