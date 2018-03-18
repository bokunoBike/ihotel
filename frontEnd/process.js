{
  "apps": [{
    "name" : "teckmicro",
    "script": "./bin/www",
    "cwd": "./",
    "watch":[
                "bin",
                "common",
                "configs",
                "public",
                "routes",
                "views"
        ],
    "error_file":"./logs/app-err.log",
    "out_file":"./logs/app-out.log",
    "log_date_format":"YYYY-MM-DD HH:mm Z"
    }]
}

