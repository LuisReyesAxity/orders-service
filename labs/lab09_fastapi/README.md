# Lab09 - FastAPI con JWT

## Objetivo
Cómo crear una API segura con autenticación JWT en FastAPI.

## Conceptos clave
- **FastAPI** - framework para APIs, como ASP.NET Core en C#
- **JWT** - token de acceso para autenticación, como Bearer Token en C#
- **OAuth2** - estándar de autenticación
- **Depends** - inyección de dependencias, como [Authorize] en C#
- **Swagger** - documentación automática en /docs

## Flujo de autenticación
1. Haces POST /login con usuario y contraseña
2. Recibes un token JWT
3. Mandas el token en cada petición
4. Sin token recibes error 401

## Cómo correrlo
```bash
uvicorn main:app --reload
```

Abre http://127.0.0.1:8000/docs