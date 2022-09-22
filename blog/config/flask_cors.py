from flask_cors import CORS

cors = CORS(resources={
    r"/blog/*": {
        "origins": "*",
        "methods": ["GET", "HEAD", "POST", "OPTIONS", "PUT", "PATCH", "DELETE"],
        "allow_headers": "*"  
    }
})


