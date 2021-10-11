import requests

# access
access='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjIxNDQ1ODI3LCJqdGkiOiJmYzM2OGZlMzJmNGQ0MThiYWE3ZjQ4MGY3YzNjZWU2YyIsInVzZXJfaWQiOjF9.QDmH45A6y0t4dHmZs2sa0B15dgkrrzb9sMUcqdQmu0U'

# create user
# res=requests.post('http://localhost:8000/api/auth/users/',data={
#     'username':'oliver_kwame',
#     'password':'Benzema02.',
#     'email':'admin@admin.com'

# })

# activate user
# res=requests.post('http://localhost:8000/api/auth/users/activation/',data={
#     'username':'oliver',
#     'password':'Benzema02.'
# })

# obtain jwt
# res=requests.post('http://localhost:8000/api/auth/account/jwt/create/',data={
    # 'username':'admin',
    # 'password':'admin'
# })

# refresh jwt
# res=requests.post('http://localhost:8000/api/auth/account/jwt/refresh/',data={
#     'refresh':'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxOTI3NDMxOCwianRpIjoiM2E2NTdjODQ5Y2YxNDJjMmFhMWQ5MjdjNzdiYzdiOGMiLCJ1c2VyX2lkIjoxfQ.2bCXEniOz4RarBnLZnV9B4qAEO_3UxAFbBjEaZs1878'
# })

# all folder endpoint
# res=requests.get('http://localhost:8000/api/all_folders/',headers={
#     'Authorization':'Token '+access
# })

# single folder content
# res=requests.get('http://localhost:8000/api/folder/d8f0b321-1771-4947-8bdf-b92d57526a80/',headers={
#     'Authorization':'Token '+access
# })

# create new folder
# res=requests.post('http://localhost:8000/api/new_folder/',headers={
# 'Authorization':'Token '+access
# },data={
#     'name':'oliver'
# })

#  reset password
# res=requests.post('http://localhost:8000/api/auth/users/reset_password/',
# data={
#     'email':'cally@justii.com'
# })


# update profile
res=requests.get('http://localhost:8000/api/get_user_profile/',headers={
'Authorization':'Token '+access
})
print(res.status_code)