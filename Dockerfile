FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    google-adk==1.28.1 \
    python-dotenv==1.2.2 \
    pg8000==1.31.5 \
    sqlalchemy==2.0.49 \
    toolbox-core==1.0.0 \
    mcp==1.27.0 \
    fastapi==0.135.3 \
    uvicorn==0.43.0

RUN npm install -g @cocal/google-calendar-mcp @gongrzhe/server-gmail-autoauth-mcp

RUN echo "=== Confirming binary paths ===" && \
    which google-calendar-mcp && \
    which gmail-mcp

COPY mcp-toolbox/toolbox /app/toolbox
RUN chmod +x /app/toolbox

COPY mcp-toolbox/tools.yaml /app/tools.yaml
COPY study_planner_agent/ /app/study_planner_agent/
COPY calendar_credentials.json /app/calendar_credentials.json
COPY gcp-oauth.keys.json /app/gcp-oauth.keys.json
COPY calendar_tokens.json /app/calendar_tokens.json
COPY gmail_tokens.json /app/gmail_tokens.json
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

ENV GOOGLE_GENAI_USE_VERTEXAI=1
ENV GOOGLE_CLOUD_PROJECT=genaihackathon-492307
ENV GOOGLE_CLOUD_LOCATION=us-central1
ENV TOOLBOX_URL=http://127.0.0.1:5001
ENV GOOGLE_OAUTH_CREDENTIALS=/app/calendar_credentials.json
ENV GOOGLE_CALENDAR_MCP_TOKEN_PATH=/app/calendar_tokens.json
ENV GOOGLE_CALENDAR_MCP_BIN=/usr/local/bin/google-calendar-mcp
ENV GMAIL_MCP_BIN=/usr/local/bin/gmail-mcp

EXPOSE 8080
CMD ["/app/start.sh"]