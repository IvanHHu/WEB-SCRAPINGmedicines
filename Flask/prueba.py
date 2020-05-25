json_obj = [ 
    [ 
        { "medicamento": "Losart\u00e1n P\u00f3tasico 100 mg Caja Con 30...", "precio": 12800 },
        { "medicamento": "Losart\u00e1n Pot\u00e1sico Hidroclorotiazida 50 /...", "precio": 50400 },
        { "medicamento": "Losart\u00e1n Pot\u00e1sico / Hidroclorotiazida 50 /...", "precio": 35650 }
    ],
    [ 
        { "medicamento": "Losart\u00e1n P\u00f3tasico 100 mg Caja Con 30...", "precio": 11800 },
        { "medicamento": "Losart\u00e1n Pot\u00e1sico Hidroclorotiazida 50 /...", "precio": 51400 },
        { "medicamento": "Losart\u00e1n Pot\u00e1sico / Hidroclorotiazida 50 /...", "precio": 31650 }
    ],
    [ 
        { "medicamento": "Losart\u00e1n P\u00f3tasico 100 mg Caja Con 30(1)...", "precio": 111111 },
        { "medicamento": "Losart\u00e1n Pot\u00e1sico Hidroclorotiazida 50(1) /...", "precio": 222222 },
        { "medicamento": "Losart\u00e1n Pot\u00e1sico / Hidroclorotiazida 50(1) /...", "precio": 333333 }
    ]
]






if json_obj[1] != []:
    newjson = []
    for i in range(1,len(json_obj)):
        print(i)
        if newjson == []:
            newjson = json_obj[0] + json_obj[i ]
            #print(newjson)
        else:
            newjson = newjson + json_obj[i]
            #print(newjson)
            if i == len(json_obj):
                newjson.append(newjson)
            
       
print(newjson)
        #print(json_obj)

sorted_obj = sorted(newjson, key=lambda x : x['precio'], reverse=False)
print(sorted_obj)