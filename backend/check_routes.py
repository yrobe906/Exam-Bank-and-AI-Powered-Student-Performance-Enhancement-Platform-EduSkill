from app.routers import AddQuestion_router, question_router

print('AddQuestion_router routes:')
for r in AddQuestion_router.router.routes:
    print(f'  {r.path} {r.methods}')

print('\nquestion_router routes:')
for r in question_router.router.routes:
    print(f'  {r.path} {r.methods}')
