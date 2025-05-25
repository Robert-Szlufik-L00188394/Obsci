# Create non-root user
RUN groupadd -r snmpsim && useradd -r -g snmpsim snmpsim

# Install snmpsim
RUN pip install --no-cache-dir snmpsim

# Copy data into the container
WORKDIR /app
COPY mock.snmprec ./data/mock.snmprec

# Change ownership
RUN chown -R snmpsim:snmpsim /app

# Switch to non-root user
USER snmpsim

# Run the SNMP simulator (now already non-root)
CMD ["snmpsim-command-responder", "--data-dir=./data", "--agent-udpv4-endpoint=0.0.0.0:161"]
