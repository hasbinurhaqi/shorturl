from pydantic import BaseSettings

class Global(BaseSettings):
    token: str = '0RpCJO6yad6cbpnmCoa8RCXyM1GHSxciyFgXjbUf6DFvFDjHhyG'
    env_name: str = "Local"
    base_url: str = "http://localhost:2024"
    db_url: str = "sqlite:///./shortener.db"