from linkedin import linkedin
from linkedin import server
from tokens import *
# https://pypi.org/project/python3-linkedin/
# https://learn.microsoft.com/en-us/linkedin/shared/authentication/postman-getting-started


# esto era una movida para conseguir el token pero al final lo hice con postman
# RETURN_URL = 'https://localhost:8000'

# authentication = linkedin.LinkedInAuthentication(
#                     KEY,
#                     SECRET,
#                     RETURN_URL,
#                     linkedin.PERMISSIONS.enums.values()
#                 )


application = linkedin.LinkedInApplication(token=TOKEN)

print(application)
