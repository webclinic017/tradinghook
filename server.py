from app import routes, app

#-----------------------------------------

if __name__ == "__main__":
  app.run(host='0.0.0.0',ssl_context=('cert.pem', 'privkey.pem'),port=443)
