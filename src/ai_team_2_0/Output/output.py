# Output format should be
# [{
#     path: path
#     code: code
# }]

from pydantic import BaseModel,Field

class ResponseOutput(BaseModel):
    '''Output format for each file'''
    path: str = Field(description='Desired Path of the file')
    code: str = Field(description='Code for the file')

class devOutput(BaseModel):
    '''Output format for the developer node'''
    output: list[ResponseOutput] = Field(description='List of Dictionary which has path and code')

class testerOutput(BaseModel):
    '''Output format of the Tester Node'''
    status: str = Field("SUCCESS/FAILED, depending upon the condition")
    description: str = Field("Description/Report on Testing")
    