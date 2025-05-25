FROM python:3.10-slim

# Create non-root user
RUN groupadd -r snmpsim && useradd -r -g snmpsim snmpsim

# Install snmpsim
RUN pip install --no-cache-dir snmpsim

# Setup work directory
WORKDIR /app
RUN mkdir -p /app/data
COPY data/mock.snmprec /app/data/mock.snmprec
RUN chown -R snmpsim:snmpsim /app

# Switch to non-root user
USER snmpsim

# Run the simulator
CMD snmpsim-command-responder --data-dir=./data --agent-udpv4-endpoint=0.0.0.0:16161