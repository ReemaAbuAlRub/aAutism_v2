backend/
  alembic/  #data migration  models
  app/      
    
    routers/
        v1/  # first version of the routers
            - chat_router.py   #the api (endpoints) for the chatbot functions, chating and moderation 
            - user_router.py   #the api (endpoints) for the user functions, login and registration 
        base.py # base file which aggregates FastAPI v1 routers
    
    core/ 
        - config.py #contains the enviornment variables imported from .env file
        - logger.py #empty file
        - security.py  #contains the User token class, creates and decodes access tokens it also gets and verifies user passwords.
    
    services/
        llm/
            - factories.py #contains the different types of LLM providers (Google,OpenAI,etc) as classes.
     
        prompts/
            - chat_prompt.py # contains the prompt for the chatbot
            - image_prompt.py # contains the prompt for the image generation gpt
        
        - chat_service.py #chat sevice contains the logic for chatting with the bot, fetches the    chat history, adds history and generates messages.
        - image_service.py  # business logic responsible for generating images (business logic)
        - moderation_service.py #business logic for moderation service
        - sst_service.py  # business logic for speech to text service
        - tts_service.py  # business logic for text to speech service
        - user_service.py  # business logic for users (login and registration) services
    
    schemas/
        - chat.py # contains pydantic db model for the chatbot (responses and requests)
        - user.py # contains pydantic db model for the user
    
    db/
        models/
            - conversation.py # sqlalchemy orm model Describes what we store suring the convesation with the bot.
            - user.py # sqlalchemy orm model Describes what we store for each user: a unique ID, email, password, first name, last name, and their autism level.

        repository/
            - convo_repo.py # Manages conversation records: lets you add user or assistant messages and fetch a user’s chat history from the database in time order.
            - embedding_repo.py # Stores and searches embedding vectors in the index: add/update (single or batch), query by vector or ID, fetch, delete (some or all), and get index stats.
            - user.py #empty

        - base.py # Imports the tables from the models directory into a unified file
        - base_class.py # automatically provides tables with their names (mysql)
        - redis_client.py #empty file
        - session.py # returns database session
        - vectorstore.py # defines the vector database (for storing the messages)

    dependencies/
        - auth.py # Takes the login token sent with a request, looks up the matching user in the database, and only lets the request continue if that user exists and is active; otherwise it returns “Unauthorized.”

    - Dockerfile # backend dockerfile
    - main.py # main entry point for the backend 
    - requirements.txt # requirements file for teh backend

frontend/
    public/ # static files (e.g., index.html, icons) served as-is
        - crack.mp3
        - index.html
        - robot.png

    src/
        components/
            - Header.css # styling for the Header component.
            - Header.jsx # the top navigation/header UI component.
            - LeftPanel.jsx # the left-side panel/sidebar component.
        
        config/
            - api.js # API client setup (base URL and request helpers).
        
        context/
            LangaugeContext.js #React context for the current language.
        
        pages/
            - Chat.jsx # the chat screen where conversations happen.
            - HomePage.jsx # the main landing/home screen.
            - LoginPage.jsx # the login form and sign-in logic.
            - Profile.jsx # the user profile screen (view/edit details).
            - SignupPage.jsx # the user registration screen.
            - Welcome.jsx # the welcome/onboarding screen.
        
        styles/
            - Chat.css # styles specific to the Chat page.
            - Header.css # styles specific to the Header (component look & layout).
            - Profile.css # styles specific to the Profile page.
            - SignupPage.css # styles specific to the Signup page.
            - Welcome.css # styles specific to the Welcome page.
        
        translations/
            - ar.json # Arabic translation strings
            - en.json # English translation strings
        
        utils/
            - auth.js # helper functions for authentication (tokens, login/logout).
            - user.js # helper functions for user API calls (get/update profile).
        
        - App.css # global app-level styles.
        - App.js # root React component that wires routes/layout.
        - i18n.js # i18n initialization that loads translation files
        - index.js # application entry point that mounts React to the DOM

    - .dockerignore # files/folders to exclude from Docker build context.
    - .gitignore # files/folders ignored by Git.
    - dockerfile # instructions to build the frontend Docker image
    - nginx.conf # Nginx config used to serve the built frontend.
    - package-lock.json # exact, locked versions of all dependencies for reproducible installs
    - package.json # project metadata and scripts plus the list of direct dependencies.

- .env # enviornment variables
- .gitignore # files/folders ignored by Git.
- compose.yaml # docker Compose file that runs all services together (e.g., frontend, backend, DB, etc.) with their networks/volumes/env vars so you can start everything withx
- README.md # project documentation


