# CaptureDex

CaptureDex es una aplicacion web para calcular probabilidades de captura de Pokemon segun la generacion, la version del juego, la Pokeball elegida y las condiciones del encuentro.

Proyecto online: `https://capturedex.diebyte.dev/`

## Stack

- `backend/`: Django + Django REST Framework
- `frontend/`: Next.js 16 + React 19 + TypeScript + shadcn/ui
- `db`: PostgreSQL 17
- Datos base: `PokeAPI`

## Funcionalidades

- Calculadora de captura por generacion
- Listado de Pokemon filtrable por generacion y `version_group`
- Soporte de Pokeballs clasicas, modernas y variantes de Hisui
- Importacion automatica de datos de Pokemon desde PokeAPI
- UI preparada para generaciones I a IX

## Generaciones soportadas

- Backend y frontend preparados de Generacion I a Generacion IX
- Importadores disponibles de Generacion I a Generacion IX
- `version_group` soportados:
  - Gen I: `red-blue`
  - Gen II: `gold-silver`, `crystal`
  - Gen III: `ruby-sapphire`, `emerald`, `firered-leafgreen`
  - Gen IV: `diamond-pearl`, `platinum`, `heartgold-soulsilver`
  - Gen V: `black-white`, `black-2-white-2`
  - Gen VI: `x-y`, `omega-ruby-alpha-sapphire`
  - Gen VII: `sun-moon`, `ultra-sun-ultra-moon`, `lets-go-pikachu-lets-go-eevee`
  - Gen VIII: `sword-shield`, `brilliant-diamond-shining-pearl`, `legends-arceus`
  - Gen IX: `scarlet-violet`

## Estructura

```text
capturedex/
├─ backend/        # API, dominio de captura, importadores y tests
├─ frontend/       # Aplicacion Next.js
└─ compose.dev.yml # Entorno local con Postgres, backend y frontend
```

## Levantar el proyecto en local

### Opcion recomendada: Docker Compose

Desde la raiz del repo:

```bash
docker compose -f compose.dev.yml up --build
```

Servicios disponibles:

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- API health: `http://localhost:8000/api/health/`
- PostgreSQL: `localhost:5432`

Credenciales locales de Postgres:

- Host: `localhost`
- Port: `5432`
- Database: `capturedex`
- User: `capturedex`
- Password: `capturedex`

### Pasos iniciales despues de levantar contenedores

```bash
docker compose -f compose.dev.yml exec backend python manage.py migrate
docker compose -f compose.dev.yml exec backend python manage.py import_all_generations
```

## Variables de entorno

### Backend

Referencia: `backend/.env.example`

- `POKEAPI_BASE_URL`

En Docker dev tambien se usan:

- `DATABASE_URL`
- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`

### Frontend

Referencia: `frontend/.env.example`

- `NEXT_PUBLIC_API_URL`
- `INTERNAL_API_URL`

## Ejecutar sin Docker

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Comandos utiles

### Importacion de datos

- `python manage.py import_generation_one`
- `python manage.py import_generation_two`
- `python manage.py import_generation_three`
- `python manage.py import_generation_four`
- `python manage.py import_generation_five`
- `python manage.py import_generation_six`
- `python manage.py import_generation_seven`
- `python manage.py import_generation_eight`
- `python manage.py import_generation_nine`
- `python manage.py import_all_generations`

### Testing y validacion

Backend:

```bash
cd backend
python manage.py test
```

Frontend:

```bash
cd frontend
npm run lint
npx tsc --noEmit
```

## Endpoints principales

- `GET /api/v1/pokemon/`
- `POST /api/v1/captures/calculate/`
- `GET /api/health/`

## Notas de implementacion

- La calculadora usa metadata persistida de Pokemon como peso, velocidad base, tipos y si es Ultraente.
- Algunas mecanicas especiales avanzadas estan modeladas de forma base o aproximada segun el estado actual del proyecto.
- `legends-arceus` restringe en frontend las Pokeballs a las variantes de Hisui.

## Estado actual

- Proyecto funcional y desplegado en `https://capturedex.diebyte.dev/`
- API, importadores y frontend alineados para generaciones I a IX
- README creado como documentacion base del proyecto
