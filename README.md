# mittel-discovery

Microservicio para la búsqueda de posts y usuarios.

## Cómo correr

Este microservicio no tiene una base de datos asociada, porque está diseñado para usar exclusivamente a otros microservicios ([mittel-articles](https://github.com/2rinMachin/mittel-articles), [mittel-engagement](https://github.com/2rinMachin/mittel-engagement) y [mittel-users](https://github.com/2rinMachin/mittel-users)).

| Paso | Comando |
|------|----------|
| Instalar dependencias | `pip install -r requirements.txt` |
| Iniciar servidor | `uvicorn app.main:app --reload` |

---

## Endpoints disponibles

| Método | Endpoint | Dependencias | Descripción |
|--------|----------|--------------|-------------|
| GET | `/` | Independiente | Endpoint de prueba (echo). |
| GET | `/discover/articles/recent` | mittel-articles, mittel-engagement | Obtiene toda la información de los últimos artículos. |
| GET | `/discover/articles/featured` | mittel-articles, mittel-engagement | Igual que `/recent`, pero ordenado por `engagementScore` de mayor a menor. |
| GET | `/discover/articles/{id}` | mittel-articles, mittel-engagement | Devuelve toda la información del artículo por `id`. |
| GET | `/discover/articles/tag/{tag}` | mittel-articles, mittel-engagement | Devuelve todo artículo que contenga `tag`. |
| GET | `/discover/articles/title/{title}` | mittel-articles, mittel-engagement | Devuelve todo artículo cuyo título contenga `title` como substring. |
| GET | `/discover/comments/{article_id}` | mittel-articles | Devuelve todo comentario de un artículo dado. |
| GET | `/discover/users/{user_id}` | mittel-users | Devuelve la información de un usuario por `id`. |
| GET | `/discover/users/{username}` | mittel-users | Devuelve la información de un usuario por `username`. |

