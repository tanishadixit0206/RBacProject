import logging
# from slack_bolt import App
from slack_sdk import WebClient
# from onboarding import OnboardingTutorial
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import user,project,secrets,role
app=FastAPI()
client=WebClient("")

app.include_router(user.router,prefix="/user")
app.include_router(project.router,prefix="/project")
app.include_router(secrets.router,prefix="/secret")
app.include_router(role.router,prefix="/role")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

