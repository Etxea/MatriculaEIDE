docker build -t matricula-eide . ; docker rm -f matricula-eide;  docker run -d
--restart=always --name matricula-eide -p 8000 matricula-eide
