# coding=utf-8

# models: all models where testcases is.
# files: all files to be tested.
collection = [
    {
        "name":"sample1",
        "models":[
            "testcases.testfile.testfile",
            "testcases.txttable.testtest"
        ],
        "files":[
            r"samples/test*.txt",
        ]
    },
    {
        "name":"sample2",
        "models":[
            "testcases.testfile.testfile",
        ],
        "files":[
            r"samples/test*.txt",
        ]
    },
]

#the base log path, such as r"E:\res\log" or r"/home/rinkky/log"
log_base_path=r"log" 
