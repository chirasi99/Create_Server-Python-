# -------------------Question----------------------------------------------------

Program a simple web server according to the following criteria.

1). You can use either Python, Java or C programming language.

2). If you are using Python you cannot use the built-in HTTPServer module.

3). The server should listen to port 2728.

4). You need to clearly comment the program.

5). You should upload a zip file named with your index number. The zip file should contain the following items.

      a) sever source code.

      b) htdocs folder which contains the following items.

               - index.html file (this is the default web page the browser display when typed http://localhost:2728/

              - folders which contain web pages

      c) read-me file which contains instructions to execute the web server.

# -----------------------Answers-------------------------------------------------

# --------Web Server----------

This is a web server that carried out utilizing Python programming language. To run this server, you ought to have installed **Python 3.x** and every given files and folders ought to be in a similar directory.

This server can deal with just GET requests. It can handle with different clients simultaneously. It can deal with different requests from every single client simultaneously.

Also given simply created server supported to only html, css, js, php and images.

# ---------Python module used in the server-----------

        - Python **socket** module is used to implement the server.
        - Python **os** module is used to create file paths.
        - Python **mimetypes** module is used to find content types.

---

# --------About run the server------------

1. Export this zip file to a folder
2. Open Command Prompt and navigate to the folder
3. Run the following command in the command prompt

```bash
python server.py*
```

4. Open a browser and go to [**localhost:2728**](http:/localhost:2728)

---

# ------Files and folders structure-------

Webserver
│
├── server.py ( Main python code included file )
├── README.md ( Instructions )
└── htdocs
├── favicon.ico
   ├── index.html ( First html Page )
   ├── second.html ( Second html Page )
├── third
│   └── subpage.html ( Third html Page )
   ├── css
   │   ├── page.css (Include styles for pages )
   │   └── nav.css (Include styles for navigation bar )  
    ├── js
   │    └── index.js (Include js for index.js file )
└── images
├── homepage.jpg
   ├── secondpage.png
    └── subpage.jpg
